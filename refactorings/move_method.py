from antlr4.TokenStreamRewriter import TokenStreamRewriter
from refactorings.utils.utils2 import get_program, Rewriter, get_filenames_in_dir, get_file_info
from refactorings.utils.utils_listener_fast import TokensInfo, SingleFileElement, Class
import subprocess
import os

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
        static = 0

        if self.class_name not in program.packages[self.package_name].classes or self.target_class_name not in \
                program.packages[
                    self.target_package_name].classes or self.method_key not in \
                program.packages[self.package_name].classes[
                    self.class_name].methods:
            return False

        _sourceclass = program.packages[self.package_name].classes[self.class_name]
        _targetclass = program.packages[self.target_package_name].classes[self.target_class_name]
        _method = program.packages[self.package_name].classes[self.class_name].methods[self.method_key]

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
            # check that where this method is call
        for package_names in program.packages:
            package = program.packages[package_names]
            for class_ in package.classes:
                _class = package.classes[class_]
                for method_ in _class.methods:
                    __method = _class.methods[method_]
                    for inv in __method.body_method_invocations:
                        invc = __method.body_method_invocations[inv]
                        method_name = self.method_key[:self.method_key.find('(')]
                        if invc[0] == method_name:
                            inv_tokens_info = TokensInfo(inv)
                            if static == 0:
                                class_token_info = TokensInfo(_class.body_context)
                                Rewriter_.insert_after_start(class_token_info, self.target_class_name + " " + str.lower(
                                    self.target_class_name) + "=" + "new " + self.target_class_name + "();")
                                Rewriter_.apply()
                            Rewriter_.insert_before_start(class_token_info,
                                                          "import " + self.target_package_name + "." + self.target_class_name + ";")
                            Rewriter_.replace(inv_tokens_info, self.target_class_name)
                        Rewriter_.apply()

        class_tokens_info = TokensInfo(_targetclass.parser_context)
        package_tokens_info = TokensInfo(program.packages[self.target_package_name].package_ctx)
        singlefileelement = SingleFileElement(_method.parser_context, _method.filename)
        token_stream_rewriter = TokenStreamRewriter(singlefileelement.get_token_stream())

        # insert class name of source file before used attributes inside the moving method
        for index in exp:
            token_stream_rewriter.insertBeforeIndex(index=index, text=str.lower(self.class_name) + ".")

        for inv in _method.body_method_invocations:
            if inv.getText() == self.target_class_name:
                inv_tokens_info_target = TokensInfo(inv)
                token_stream_rewriter.replaceRange(from_idx=inv_tokens_info_target.start,
                                                   to_idx=inv_tokens_info_target.stop + 1, text=" ")

        # insert class name of source file before used methods inside the moving method
        for i in _method.body_method_invocations_without_typename:
            if i.getText() == self.class_name:
                ii = _method.body_method_invocations_without_typename[i]
                for j in ii:
                    i_tokens = TokensInfo(j)
                    token_stream_rewriter.insertBeforeIndex(index=i_tokens.start, text=str.lower(self.class_name) + ".")

        # pass object of source class to method
        if len(_method.body_method_invocations_without_typename) or exp:
            if param_tokens_info.start is not None:
                token_stream_rewriter.insertBeforeIndex(param_tokens_info.start,
                                                        text=self.class_name + " " + str.lower(self.class_name) + ",")
            else:
                token_stream_rewriter.insertBeforeIndex(method_declaration_info.stop,
                                                        text=self.class_name + " " + str.lower(self.class_name))

        strofmethod = token_stream_rewriter.getText(program_name=token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                    start=tokens_info.start,
                                                    stop=tokens_info.stop)

        Rewriter_.insert_before(tokens_info=class_tokens_info, text=strofmethod)
        # importing proprate package when method is moved to some other package
        if self.target_package_name != self.package_name:
            target_class_modifier_token = TokensInfo(_targetclass.modifiers_parser_contexts[0])
            Rewriter_.insert_before_start(
                target_class_modifier_token,
                "import " + self.package_name + "." + self.class_name + ";\n"
            )

        # add imported class in destination file
        file_info = get_file_info(_sourceclass.filename)
        for imported_class in file_info.all_imports:
            target_class_modifier_token = TokensInfo(_targetclass.modifiers_parser_contexts[0])
            Rewriter_.insert_before_start(target_class_modifier_token,
                "import " + imported_class.package_name + "." + (imported_class.class_name if hasattr(imported_class, 'class_name') else '*') + ";\n")

        Rewriter_.replace(tokens_info, "")
        Rewriter_.apply()

        self.__reformat(_sourceclass, _targetclass)
        return True

    def __reformat(self, src_class: Class, target_class: Class):
        subprocess.call(["java", "-jar", self.formatter, "--replace", src_class.filename, target_class.filename])


if __name__ == "__main__":
    #mylist = get_filenames_in_dir('/home/mohamad/projects/compiler/TheShitTest/src')
    mylist = get_filenames_in_dir('/home/mohamad/projects/benchmark_projects/JSON/src/main/java/org/json')
    print("Testing move_method...")
    #move_method = MoveMethodRefactoring(mylist, "PackageA", "A", "A_method_1()", "B", "PackageA")
    move_method = MoveMethodRefactoring(mylist, "org.json", "Cookie", "escape(String)", "CookieList", "org.json")
    if move_method.do_refactor():
        print("Success!")
    else:
        print("Cannot refactor.")
