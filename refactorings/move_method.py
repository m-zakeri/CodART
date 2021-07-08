from antlr4.TokenStreamRewriter import TokenStreamRewriter
from refactorings.utils.utils2 import get_program, Rewriter, get_filenames_in_dir, get_objects
from refactorings.utils.utils_listener_fast import TokensInfo, SingleFileElement, Class
import subprocess
import os
import time


class MoveMethodRefactoring:
    def __init__(self, source_filenames: list, package_name: str, class_name: str, method_key: str,
                 target_class_name: str, target_package_name: str,
                 filename_mapping=lambda x: x + ".rewritten.java"):
        self.source_filenames = source_filenames
        self.package_name = package_name
        self.class_name = class_name
        self.method_key = method_key
        self.target_class_name = target_class_name
        self.target_package_name = target_package_name
        self.filename_mapping = filename_mapping
        self.formatter = os.path.abspath("assets/formatter/google-java-format-1.10.0-all-deps.jar")

    def do_refactor(self):
        program = get_program(self.source_filenames)
        objects = get_objects(self.source_filenames)
        static = 0

        if self.class_name not in program.packages[self.package_name].classes:
            return False
        if self.target_class_name not in program.packages[self.target_package_name].classes:
            return False
        if self.method_key not in program.packages[self.package_name].classes[self.class_name].methods:
            return False

        _sourceclass = program.packages[self.package_name].classes[self.class_name]
        _targetclass = program.packages[self.target_package_name].classes[self.target_class_name]
        _method = program.packages[self.package_name].classes[self.class_name].methods[self.method_key]
        method_name = self.method_key[:self.method_key.find('(')]

        if _method.is_constructor:
            return False

        # check if target class has same method
        if self.method_key in _targetclass.methods:
            return False


        Rewriter_ = Rewriter(program, lambda x: x)
        tokens_info = TokensInfo(_method.parser_context)  # tokens of ctx method
        param_tokens_info = TokensInfo(_method.formalparam_context)
        method_declaration_info = TokensInfo(_method.method_declaration_context)
        exp = []  # For saving variables declared in body of class and also used in body of method
        exps = tokens_info.get_token_index(tokens_info.token_stream.tokens, tokens_info.start, tokens_info.stop)

        # check that method is static or not
        for modifier in _method.modifiers:
            if modifier == "static":
                static = 1

        for token in exps:
            if token.text in _sourceclass.fields:
                exp.append(token.tokenIndex)

        source_object_name = str.lower(self.class_name)
        target_object_name = str.lower(self.target_class_name)

        for package_names in program.packages:
            package = program.packages[package_names]
            for class_ in package.classes:
                _class = package.classes[class_]
                import_status = False
                for method_ in _class.methods:
                    __method = _class.methods[method_]
                    for obj_or_class_ctx in __method.body_method_invocations:
                        invc = __method.body_method_invocations[obj_or_class_ctx]
                        try:
                            obj_or_class_str = obj_or_class_ctx.children[0].children[0].getText()
                            cond1 = objects[package_names][class_][method_[:method_.find('(')]].get(obj_or_class_str) == self.class_name
                            cond2 = obj_or_class_str == self.class_name
                        except:
                            continue
                        if invc[0] == method_name and (cond1 or cond2):
                            inv_tokens_info = TokensInfo(obj_or_class_ctx)
                            if static == 0:
                                Rewriter_.replace(inv_tokens_info, target_object_name)
                            elif static == 1:
                                Rewriter_.replace(inv_tokens_info, self.target_class_name)
                            if not import_status:
                                import_status = True
                                class_token_info = TokensInfo(_class.body_context)
                                class_modifier_token_info = TokensInfo(_class.modifiers_parser_contexts[0])
                                if static == 0:
                                    Rewriter_.insert_after_start(class_token_info,
                                                                 '\nstatic ' + self.target_class_name + " " + target_object_name + "=" + "new " + self.target_class_name + "();")
                                Rewriter_.insert_before_start(class_modifier_token_info, "import " + self.target_package_name + "." + self.target_class_name + ";\n")
                            Rewriter_.apply()




        class_tokens_info = TokensInfo(_targetclass.parser_context)
        package_tokens_info = TokensInfo(program.packages[self.target_package_name].package_ctx)
        singlefileelement = SingleFileElement(_method.parser_context, _method.filename)
        token_stream_rewriter = TokenStreamRewriter(singlefileelement.get_token_stream())

        # add target class (or its object) before method_invocations_without_typename in source class methods
        source_body_class_token = TokensInfo(_sourceclass.body_context)
        Rewriter_.insert_after_start(source_body_class_token, '\nstatic ' + self.target_class_name + " " + target_object_name + "=" + "new " + self.target_class_name + "();")
        Rewriter_.apply()
        for method_ in _sourceclass.methods:
            __method = _sourceclass.methods[method_]
            for inv in __method.body_method_invocations_without_typename:
                invc = __method.body_method_invocations_without_typename[inv]
                if inv.getText() == self.class_name:
                    for j in invc:
                        if j.IDENTIFIER().getText() == method_name:
                            i_tokens = TokensInfo(j)
                            if static == 0:
                                Rewriter_.insert_before_start(i_tokens, target_object_name + ".")
                            elif static == 1:
                                Rewriter_.insert_before_start(i_tokens, self.target_class_name + ".")
                            Rewriter_.apply()



        # insert class name of source file before used attributes inside the moving method
        for index in exp:
            token_stream_rewriter.insertBeforeIndex(index=index, text=source_object_name + ".")

        for inv in _method.body_method_invocations:
            if inv.getText() == self.target_class_name:
                inv_tokens_info_target = TokensInfo(inv)
                token_stream_rewriter.replaceRange(from_idx=inv_tokens_info_target.start, to_idx=inv_tokens_info_target.stop + 1, text=" ")

        # insert class name of source file before used methods inside the moving method
        for i in _method.body_method_invocations_without_typename:
            if i.getText() == self.class_name:
                ii = _method.body_method_invocations_without_typename[i]
                for j in ii:
                    i_tokens = TokensInfo(j)
                    token_stream_rewriter.insertBeforeIndex(index=i_tokens.start, text=target_object_name+ ".")

        # create source class object in target class to use source fields
        target_body_class_token = TokensInfo(_targetclass.body_context)
        if len(_method.body_method_invocations_without_typename) or exp:
            if target_body_class_token.start is not None:
                Rewriter_.insert_after_start(target_body_class_token, '\nstatic ' + self.class_name + " " + source_object_name + "=" + "new " + self.class_name + "();")


        # move main method
        strofmethod = token_stream_rewriter.getText(program_name=token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                    start=tokens_info.start,
                                                    stop=tokens_info.stop)
        Rewriter_.insert_before(tokens_info=class_tokens_info, text=strofmethod)

        # importing proprate package when method is moved to some other package
        if self.target_package_name != self.package_name:
            target_class_modifier_token = TokensInfo(_targetclass.modifiers_parser_contexts[0])
            Rewriter_.insert_before_start(target_class_modifier_token,"import " + self.package_name + "." + self.class_name + ";\n")
            Rewriter_.apply()

        Rewriter_.replace(tokens_info, "")
        Rewriter_.apply()


        # self.propagate(program.packages, Rewriter_)
        # self.__reformat(_sourceclass)
        # self.__reformat(_targetclass)
        return True

    def propagate(self, package, rewriter):
        for package_item in package:
            package_item_dic = package[package_item]
            for classes_item in package_item_dic.classes:
                class_item_dic = package_item_dic.classes[classes_item]
                if classes_item == self.class_name:  # check any method in source class use that function or not
                    sourceClass = package[self.package_name].classes[self.class_name]
                    for method_item in sourceClass.methods:
                        if method_item==self.method_key:
                            continue
                        method_item_dict = sourceClass.methods[method_item]
                        for i in method_item_dict.body_method_invocations_without_typename:
                            if i.getText() == self.class_name:
                                if self.target_package_name != self.package_name:  # 1-import package-check to don't import self package
                                    import_parser = TokensInfo(sourceClass.modifiers_parser_contexts[0])
                                    rewriter.insert_before_start(import_parser,
                                                                 '\nimport ' + self.target_package_name + '.' + self.target_class_name + ';')
                                ii = method_item_dict.body_method_invocations_without_typename[
                                    i]  # create instance before where our target function usage
                                for j in ii:
                                    i_tokens = TokensInfo(j)
                                    rewriter.insert_before_start(i_tokens,
                                                                 self.target_class_name + ' ' + self.target_class_name.lower() + str(
                                                                     int(
                                                                         time.time())) + ' = new ' + self.target_class_name + '();\n' + self.target_class_name.lower() + str(
                                                                     int(
                                                                         time.time())) + '.')
                                    rewriter.apply()

                else:
                    for method_item in class_item_dic.methods:
                        method_item_dict = class_item_dic.methods[
                            method_item]  # check that class use our target method or not ***
                        tempIndex = method_item_dict.body_text.find('=new' + self.class_name + '()')
                        tempIndex2 = method_item_dict.body_text[:tempIndex].find(self.class_name)
                        tempIndex2 = tempIndex2 + len(self.class_name)
                        instance_name = method_item_dict.body_text[tempIndex2:tempIndex]
                        my_line = instance_name + '.' + self.method_key
                        if my_line in method_item_dict.body_text:  # check that class use our target method or not ***
                            if self.target_package_name != class_item_dic.package_name:  # check to dont import self package
                                import_parser = TokensInfo(class_item_dic.modifiers_parser_contexts[0])
                                rewriter.insert_before_start(import_parser,
                                                             '\nimport ' + self.target_package_name + '.' + self.target_class_name + ';')
                            new_instance_name = self.target_class_name.lower() + str(
                                int(time.time()))  # this trick will create a unique name
                            method_parser = TokensInfo(
                                method_item_dict.body_local_vars_and_expr_names[0].parser_context)
                            if self.target_class_name != class_item_dic.name:  # dont create a instace of self class ( if target class is our selecting class )
                                rewriter.insert_before_start(method_parser,
                                                             self.target_class_name + ' ' + new_instance_name + ' = new ' + self.target_class_name + '();\n')
                            for body_item in method_item_dict.body_local_vars_and_expr_names:
                                try:
                                    if body_item.dot_separated_identifiers[0] == instance_name and \
                                            body_item.dot_separated_identifiers[1] == \
                                            self.method_key.split('(')[0]:
                                        instance_parser = TokensInfo(body_item.parser_context)
                                        if self.target_class_name != class_item_dic.name:  # if target class is our selecting class dont write myClass.function instead of function
                                            rewriter.replace(instance_parser,
                                                             new_instance_name + '.' + self.method_key)
                                        else:
                                            rewriter.replace(instance_parser, self.method_key)
                                except:
                                    continue
                            rewriter.apply()
                self.__reformat(class_item_dic)


    def __reformat(self, src_class: Class):
        subprocess.call(["java", "-jar", self.formatter, "--replace", src_class.filename])


if __name__ == "__main__":
    mylist = get_filenames_in_dir('/data/Dev/JavaSample/')
    # mylist = get_filenames_in_dir('tests/movemethod_test')
    print("Testing move_method...")
    if MoveMethodRefactoring(mylist, "my_package", "Source", "getNumber2()", "Target",
                             "my_package").do_refactor():  # if move_method_refactoring(mylist, "ss", "source", "m(int)","target","sss"):
        print("Success!")
    else:
        print("Cannot refactor.")
