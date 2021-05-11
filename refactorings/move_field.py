import os
import subprocess
from refactorings.utils.utils2 import get_program, Rewriter, get_filenames_in_dir
from refactorings.utils.scope_listener import get_program2
from refactorings.utils.utils_listener_fast import TokensInfo, Field, Class, LocalVariable
from antlr4.TokenStreamRewriter import TokenStreamRewriter

class UnResolvedMetaError(Exception):
    pass


class NonStaticFieldRefactorError(Exception):
    pass


class MoveFieldRefactoring:
    def __init__(self, source_filenames: list, package_name: str,
                 class_name: str, field_name: str, target_class_name: str,
                 target_package_name: str, filename_mapping: str):
        self.source_filenames = source_filenames
        self.package_name = package_name
        self.class_name = class_name
        self.field_name = field_name
        self.target_class_name = target_class_name
        self.target_package_name = target_package_name
        self.filename_mapping = filename_mapping + ".rewritten.java"
        self.formatter = os.path.abspath("../assets/formatter/google-java-format-1.10.0-all-deps.jar")

    def get_metadata(self, program):
        """
        Finds the source and the target class inside the program.
        """
        try:
            class_name = program.packages[self.package_name].classes[self.class_name]
            target_class = program.packages[self.package_name].classes[self.target_class_name]
            field = program.packages[self.package_name].classes[self.class_name].fields[self.field_name]
        except KeyError:
            return None
        return class_name, target_class, field

    @staticmethod
    def stringify(tokens, start, end):
        """
        Converts list of tokens into strings
        """
        string = ""
        for t in tokens[start: end]:
            if t.text != ' ':
                string += t.text
        return string

    def is_method_scope_var(self, tokens, token, method):
        """
        Checks if given token is related to a method parameter or not
        """
        method_params = list(map(lambda p: p[1], method.parameters))
        if token.text in method_params:
            selector = self.stringify(tokens, token.tokenIndex - 2, token.tokenIndex)
            if method.class_name == self.class_name:
                return selector not in ['this.', self.class_name + '.']
            return selector == self.class_name + '.'
        return False

    def is_declared_in_method(self, tokens, token, method):
        """
        Checks if given token is related to a new declared variable in a method
        """
        selector = self.stringify(tokens, token.tokenIndex - 2, token.tokenIndex)
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

    def is_a_usage(self, tokens, token, method):
        """
        Checks if given token is related to the static field, program searching for
        """
        selector = self.stringify(tokens, token.tokenIndex - 2, token.tokenIndex)
        if selector == 'this.':
            if method.class_name == self.class_name:
                return True
            return False
        return True

    def get_usages_in_methods(self, src):
        """
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
                    is_method_param = self.is_method_scope_var(tokens_info.token_stream.tokens, token, method)
                    is_new_declaration = self.is_declared_in_method(tokens_info.token_stream.tokens, token, method)
                    is_a_usage = self.is_a_usage(tokens_info.token_stream.tokens, token, method)
                    if is_new_declaration or is_method_param or not is_a_usage:
                        continue

                    new_case = {
                        'method': method,
                        'tokens': list(filter(lambda t: t.line == token.line, exps))
                    }
                    usages.append(new_case)
        return usages

    def get_usage(self):
        """
        Finds usages of a field inside project files
        # todo We should add usage search for class fields
        """
        program = get_program(self.source_filenames)

        try:
            source_class, target_class, field = self.get_metadata(program)
        except KeyError:
            raise UnResolvedMetaError("Source or destination not found!")

        if 'static' not in field.modifiers:
            raise NonStaticFieldRefactorError("Non-static fields cannot be refactored!")

        usages = list()
        for p_name, package in program.packages.items():
            for cls_name, cls in package.classes.items():
                new_usages = self.get_usages_in_methods(cls)
                usages.extend(new_usages)

        return usages, program

    def propagate(self, field: Field, rewriter: Rewriter):
        usages, program = self.get_usage()
        for usage in usages:
            method_tokens = TokensInfo(usage["method"].parser_context)

            for i, token in enumerate(usage['tokens']):
                if token.text != self.field_name:
                    continue

                method_tokens.start = token.tokenIndex
                method_tokens.stop = token.tokenIndex
                if i > 1:
                    if usage["tokens"][i - 2].text == "this" or \
                            usage["tokens"][i - 2].text == self.class_name:
                        method_tokens.start -= 2

                token_stream = usage["method"].parser_context.parser.getTokenStream()
                if token_stream not in rewriter.token_streams.keys():
                    rewriter.token_streams[token_stream] = (
                        usage["method"].filename,
                        TokenStreamRewriter(token_stream),
                        usage["method"].filename.replace(".java", ".rewritten.java")
                    )
                rewriter.replace(method_tokens, f'{self.target_class_name}.{self.field_name}')
                break

    def move(self):
        usage, program = self.get_usage()
        source_package = program.packages[self.package_name]
        source_class = source_package.classes[self.class_name]
        target_class = source_package.classes[self.target_class_name]
        field = source_class.fields[self.field_name]
        rewriter = Rewriter(program,
                            lambda x: f"{os.path.dirname(x)}/{os.path.splitext(os.path.basename(x))[0]}.rewritten.java")

        self.__remove_field_from_src(field, rewriter)
        self.__move_field_to_dst(target_class, field, rewriter)
        self.propagate(field, rewriter)
        rewriter.apply()

        modified_files = set(map(lambda x: x["method"].filename.replace(".java", ".rewritten.java"), usage))
        modified_files.add(source_class.filename.replace(".java", ".rewritten.java"))
        modified_files.add(target_class.filename.replace(".java", ".rewritten.java"))
        self.__reformat(modified_files)

        return True

    def __remove_field_from_src(self, field: Field, rewriter: Rewriter):
        tokens = TokensInfo(field.parser_context)
        tokens.stop += 1
        rewriter.replace(tokens, "")

        for mod_ctx in field.modifiers_parser_contexts:
            mod_tokens = TokensInfo(mod_ctx)
            mod_tokens.stop += 1
            rewriter.replace(mod_tokens, "")

    def __move_field_to_dst(self, target: Class, field: Field, rewriter: Rewriter):
        # this nasty if is because the grammar sucks. converts new SomeClass() to newSomeClass()
        if field.initializer is not None and field.initializer.startswith("new"):
            field.initializer = field.initializer.replace("new", "new ", 1)

        self.__modify_access_modifiers(field)

        new_field = f'\n\t{" ".join(field.modifiers)} {field.datatype} {field.name}{f" = {field.initializer};" if field.initializer else ";"}\n'
        target_class_tokens = TokensInfo(target.body_context)
        rewriter.insert_after_start(target_class_tokens, new_field)

    def __modify_access_modifiers(self, field: Field):
        index = -1
        for i, mod in enumerate(field.modifiers):
            if mod == "private" or mod == "protected":
                index = i
                break

        if index != -1:
            field.modifiers.pop(index)

        field.modifiers.insert(0, "public")

    def __reformat(self, modified_files: set):
        temp = ["java", "-jar", self.formatter, "--replace"]
        temp.extend(list(modified_files))
        print(temp)
        subprocess.call(temp)


if __name__ == '__main__':
    path = "/home/loop/IdeaProjects/Sample"
    my_list = get_filenames_in_dir(path)
    filtered = []
    for file in my_list:
        if "rewritten.java" in file:
            os.remove(file)
        else:
            filtered.append(file)

    refactoring = MoveFieldRefactoring(filtered, "sample", "Test3", "toBeMoved",
                                       "Test", "sample", "")

    refac = refactoring.move()
    print(refac)
