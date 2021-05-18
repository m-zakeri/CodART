import os
import subprocess
from refactorings.utils.utils2 import get_program, Rewriter, get_filenames_in_dir
from refactorings.utils.scope_listener import get_program2
from refactorings.utils.utils_listener_fast import TokensInfo, Field, Class, Method, LocalVariable, ClassImport
from antlr4.TokenStreamRewriter import TokenStreamRewriter


class UnResolvedMetaError(Exception):
    pass


class NonStaticFieldRefactorError(Exception):
    pass


class MoveFieldRefactoring:
    def __init__(self, source_filenames: list, package_name: str,
                 class_name: str, field_name: str, target_class_name: str,
                 target_package_name: str):
        self.source_filenames = source_filenames
        self.package_name = package_name
        self.class_name = class_name
        self.field_name = field_name
        self.target_class_name = target_class_name
        self.target_package_name = target_package_name
        self.formatter = os.path.abspath("../assets/formatter/google-java-format-1.10.0-all-deps.jar")

    def get_metadata(self, program):
        """
        :param program: The program which is extracted from the get_program() method
        :return: The source class, target_class and the field which is to be moved
        if there are no such classes or fields or packages in the program, KeyError will be raised
        """
        class_name = program.packages[self.package_name].classes[self.class_name]
        target_class = program.packages[self.target_package_name].classes[self.target_class_name]
        field = program.packages[self.package_name].classes[self.class_name].fields[self.field_name]

        return class_name, target_class, field

    @staticmethod
    def __stringify(tokens, start, end):
        """
        :param tokens: a list of tokens
        :param start: the index of the first token you want
        :param end: the index of the last token you want
        :return: String of the desired tokens
        Converts list of tokens into strings
        """
        string = ""
        for t in tokens[start: end]:
            if t.text != ' ':
                string += t.text

        return string

    def __is_var_in_method_params(self, tokens, token, method):
        """
        :param tokens: a list of all the tokens of the file in which the method is
        :param token: The token of the var that is to be checked
        :param method: The method that is going to be checked for its parameters
        :return: Whether the variable is in the method's parameters or not
        Checks if given token is related to a method parameter or not
        """
        method_params = list(map(lambda p: p[1], method.parameters))
        if token.text in method_params:
            selector = self.__stringify(tokens, token.tokenIndex - 2, token.tokenIndex)

            if method.class_name == self.class_name:
                return selector not in ['this.', self.class_name + '.']

            return selector == self.class_name + '.'

        return False

    def __is_declared_in_method(self, tokens, token, method):
        """
        :param tokens: a list of all the tokens of the file in which the method is
        :param token: The token of the var that is to be checked
        :param method: The method that is going to be checked for its local variables
        :return: Whether the variable is declared in the method or not
        Checks if given token is related to a new declared variable in a method
        """
        selector = self.__stringify(tokens, token.tokenIndex - 2, token.tokenIndex)
        if method.class_name == self.class_name:
            if selector in ['this.', self.class_name + '.']:
                return False
        elif selector == self.class_name + '.':
            return False

        local_exp_var = method.body_local_vars_and_expr_names
        try:
            local_var_definition = next(filter(lambda x: isinstance(x, LocalVariable) and
                                                         x.identifier == token.text, local_exp_var))
            start = local_var_definition.parser_context.start.start
            if start <= token.start:
                return True

            return False
        except StopIteration:
            return False

    def __is_declared_in_class(self, tokens, token, method):
        """
        :param tokens: a list of all the tokens of the file in which the method is
        :param token: The token of the var that is to be checked
        :param method: The method that is going to be checked for its fields
        :return: Whether the variable is declared in the method's class or not
        Checks if given token is related to a new declared variable in a method
        """
        selector = self.__stringify(tokens, token.tokenIndex - 2, token.tokenIndex)
        if method.class_name == self.class_name:
            if selector in ['this.', self.class_name + '.']:
                return False
        elif selector == self.class_name + '.':
            return False

    def __is_a_usage(self, tokens, token, method):
        """
        :param tokens: a list of all the tokens of the file in which the method is
        :param token: The token of the var that is to be checked
        :param method: The method that is going to be checked
        :return: Whether the field is used or not
        Checks if given token is related to the static field, program searching for
        """
        selector = self.__stringify(tokens, token.tokenIndex - 2, token.tokenIndex)
        if selector == 'this.':
            if method.class_name == self.class_name:
                return True

            return False

        return True

    def __is_a_usage_in_class(self, tokens, token, field):
        """
        :param tokens: a list of all the tokens of the file in which the method is
        :param token: The token of the var that is to be checked
        :param field: The field that is going to be checked
        :return: Whether the field is used in the class or not
        Checks if given token is related to the static field, program searching for
        """
        selector = self.__stringify(tokens, token.tokenIndex - 2, token.tokenIndex)
        if selector == self.class_name + '.':
            return True
        if selector == 'this.':
            if field.class_name == self.class_name:
                return True

            return False

        return field.class_name == self.class_name

    def __get_usages_in_class_body(self, src):
        """
        :param src: The source in which we want to extract the field's usages
        :return: A `list` of all the field's usages in the class body
        """
        usages = list()
        fields: dict = src.fields
        for field_name, field in fields.items():
            if field_name == self.field_name and src.name == self.class_name:
                continue
            tokens_info = TokensInfo(field.parser_context)  # tokens of ctx method
            exps = tokens_info.get_token_index(tokens_info.token_stream.tokens, tokens_info.start, tokens_info.stop)

            for token in exps:
                if token.text == self.field_name:
                    if self.__is_a_usage_in_class(tokens_info.token_stream.tokens, token, field):
                        new_case = {
                            'meta_data': field,
                            'tokens': list(filter(lambda t: t.line == token.line, exps))
                        }
                        usages.append(new_case)

        return usages

    def __get_usages_in_methods(self, src):
        """
        :param src: The source in which we want to extract the field's usages
        :return: A `list` of all the field's usages in a method
        Finds method based usages of a field
        """
        usages = list()

        methods: dict = src.methods
        for method_name, method in methods.items():
            # if hasattr(method, "scope"):
            #     print(method.scope)
            #      method.scope.declared_vars
            tokens_info = TokensInfo(method.parser_context)  # tokens of ctx method
            param_tokens_info = TokensInfo(method.formalparam_context)
            method_declaration_info = TokensInfo(method.method_declaration_context)
            exps = tokens_info.get_token_index(tokens_info.token_stream.tokens, tokens_info.start, tokens_info.stop)

            for token in exps:
                if token.text == self.field_name:
                    is_method_param = self.__is_var_in_method_params(tokens_info.token_stream.tokens, token, method)
                    is_new_declaration = self.__is_declared_in_method(tokens_info.token_stream.tokens, token, method)
                    is_a_usage = self.__is_a_usage(tokens_info.token_stream.tokens, token, method)
                    if is_new_declaration or is_method_param or not is_a_usage:
                        continue

                    new_case = {
                        'meta_data': method,
                        'tokens': list(filter(lambda t: t.line == token.line, exps))
                    }
                    usages.append(new_case)

        return usages

    def __should_add_import(self, klass: Class):
        """
        :param klass: The class which might need an import statement
        :return: Whether the class needs import or not
        Check whether the file needs a certain import statement
        """
        # we don't need to handle target class
        if klass.name == self.target_class_name:
            return False

        # check package imports
        for package_import in klass.file_info.package_imports:
            if package_import.package_name == self.target_package_name:
                return False

        # if target class not imported as package then check class imports
        for class_import in klass.file_info.class_imports:
            if class_import.class_name == self.target_class_name:
                return False

        # if target class is not imported add the import
        return True

    def __is_field_in_class(self, field, target_class):
        """
        :param field: The field which is to be checked
        :param target_class: The target class name
        :return: Whether the field is in the target class or not
        """
        class_fields = target_class.fields
        for f in class_fields:
            if f == field.name:
                return True

        return False

    def __get_usage(self):
        """
        :return: A list of all the usages of the field
        Finds usages of a field inside project files
        """
        program = get_program(self.source_filenames)

        try:
            source_class, target_class, field = self.get_metadata(program)
        except KeyError:
            raise UnResolvedMetaError("Source or destination not found!")

        if 'static' not in field.modifiers:
            raise NonStaticFieldRefactorError("Non-static fields cannot be refactored!")

        if self.__is_field_in_class(field, target_class):
            raise Exception("A field with the same name exists in target class!")

        usages = list()
        for p_name, package in program.packages.items():
            for cls_name, cls in package.classes.items():
                new_usages = self.__get_usages_in_methods(cls)
                usages.extend(new_usages)
                new_usages = self.__get_usages_in_class_body(cls)
                usages.extend(new_usages)
                should_import = self.__should_add_import(cls)

                if not should_import:
                    continue

                usages.append({
                    "import": cls,
                })

        return usages, program

    def __propagate(self, usages: list, rewriter: Rewriter):
        """
        :param rewriter: The rewriter object which is going to rewrite the files
        :param usages: the usages of the field in the program
        :return: void
        Propagates the changes made to the files and the field
        """
        local_var_declared = False
        for usage in usages:
            if "import" in usage:
                self.__add_import(usage["import"], rewriter)
                continue

            method_tokens = TokensInfo(usage["meta_data"].parser_context)
            for i, token in enumerate(usage['tokens']):
                if token.text != self.field_name:
                    continue
                method_tokens.start = token.tokenIndex
                method_tokens.stop = token.tokenIndex
                if i > 1:
                    if usage["tokens"][i - 2].text == "this" or \
                            usage["tokens"][i - 2].text == self.class_name:
                        method_tokens.start -= 2
                    else:
                        if local_var_declared:
                            continue
                        local_var_declared = True
                        continue
                else:
                    if local_var_declared:
                        continue

                token_stream = usage["meta_data"].parser_context.parser.getTokenStream()
                if token_stream not in rewriter.token_streams.keys():
                    rewriter.token_streams[token_stream] = (
                        usage["meta_data"].filename,
                        TokenStreamRewriter(token_stream),
                        usage["meta_data"].filename
                    )
                rewriter.replace(method_tokens, f'{self.target_class_name}.{self.field_name}')

    def move(self):
        """
        :return: Whether the refactoring is completed or not
        Performs the move field refactoring
        """
        usages, program = self.__get_usage()
        source_package = program.packages[self.package_name]
        target_package = program.packages[self.target_package_name]
        source_class = source_package.classes[self.class_name]
        target_class = target_package.classes[self.target_class_name]
        field = source_class.fields[self.field_name]
        rewriter = Rewriter(program,
                            lambda x: f"{os.path.dirname(x)}/{os.path.splitext(os.path.basename(x))[0]}.java")

        self.__remove_field_from_src(field, rewriter)
        self.__move_field_to_dst(target_class, field, rewriter)
        self.__propagate(usages, rewriter)
        rewriter.apply()
        modified_files = set(map(lambda x: x["meta_data"].filename,
                                 filter(lambda x: "meta_data" in x, usages)))
        modified_files.union(set(map(lambda x: x["import"].filename,
                                     filter(lambda x: "import" in x, usages))))
        modified_files.add(source_class.filename)
        modified_files.add(target_class.filename)
        self.__reformat(list(modified_files))

        return True

    def __remove_field_from_src(self, field: Field, rewriter: Rewriter):
        """
        :param field: The field which is to be moved in the refactoring
        :param rewriter: The rewriter object which is going to rewrite the files
        :return: void
        Remove the field from the source class
        """
        tokens = TokensInfo(field.parser_context)
        tokens.stop += 1
        rewriter.replace(tokens, "")

        for mod_ctx in field.modifiers_parser_contexts:
            mod_tokens = TokensInfo(mod_ctx)
            mod_tokens.stop += 1
            rewriter.replace(mod_tokens, "")

    def __move_field_to_dst(self, target: Class, field: Field, rewriter: Rewriter):
        """
        :param target: The target class that the field is going to be moved to
        :param field: The field which is to be moved in the refactoring
        :param rewriter: The rewriter object which is going to rewrite the files
        :return: void
        Move the field from the source to the target class
        """
        # this nasty if is because the grammar sucks. converts new SomeClass() to newSomeClass()
        if field.initializer is not None and field.initializer.startswith("new"):
            field.initializer = field.initializer.replace("new", "new ", 1)

        self.__modify_access_modifiers(field)

        new_field = f'\n\t{" ".join(field.modifiers)} {field.datatype} {field.name}{f" = {field.initializer};" if field.initializer else ";"}\n'
        target_class_tokens = TokensInfo(target.body_context)
        rewriter.insert_after_start(target_class_tokens, new_field)

    def __modify_access_modifiers(self, field: Field):
        """
        :param field: The field which is going to be modified
        :return: void
        Changes the moving field's access modifiers
        """
        index = -1
        for i, mod in enumerate(field.modifiers):
            if mod == "private" or mod == "protected" or mod == "public":
                index = i
                break

        if index != -1:
            field.modifiers.pop(index)

        field.modifiers.insert(0, "public")

    def __reformat(self, modified_files: list):
        """
        :param modified_files: The files that have been modified since the refactoring
        :return: void
        reformats the java files based on google's java pretty format
        """
        temp = ["java", "-jar", self.formatter, "--replace"]
        temp.extend(modified_files)
        print(temp)
        subprocess.call(temp)

    def __add_import(self, klass: Class, rewriter):
        """
        :param klass: The class where the import should be added to
        :param rewriter: The rewriter object which is going to rewrite the files
        :return: void
        Adds the imports that are needed in the file since the refactorings
        """
        # if there are no imports in the class appends before the start of class
        import_line = f"import {self.target_package_name}.{self.target_class_name};"
        if len(klass.file_info.all_imports) == 0:
            tokens_info = TokensInfo(klass.parser_context)
            tokens_info.start -= len(klass.modifiers_parser_contexts) * 2
            tokens_info.stop += 1
            rewriter.insert_before_start(tokens_info, import_line)
            return

        # if however we have some imports append new import at the end of last import
        tokens_info = TokensInfo(klass.file_info.all_imports[-1].parser_context)
        tokens_info.stop += 1
        rewriter.insert_after(tokens_info, import_line)


if __name__ == '__main__':
    path = "/home/ali/Desktop/JavaTestProject/src/"
    my_list = get_filenames_in_dir(path)

    refactoring = MoveFieldRefactoring(my_list, "", "SourceClass", "field_for_move",
                                       "TargetClass", "")

    refac = refactoring.move()
    print(refac)
