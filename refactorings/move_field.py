import os

from refactorings.utils.utils2 import get_program, Rewriter, get_filenames_in_dir
from refactorings.utils.utils_listener_fast import TokensInfo, Field


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

    def validate_metadata(self, program) -> bool:
        if self.class_name not in program.packages[self.package_name].classes:
            return False
        if self.target_class_name not in program.packages[self.target_package_name].classes:
            return False
        if self.field_name not in program.packages[self.package_name].classes[
            self.class_name].fields:
            return False
        return True

    def is_method_scope_var(self, tokens, token, method):
        method_params = list(map(lambda p: p[1], method.parameters))
        if token.text not in method_params:
            return False
        if tokens[token.tokenIndex - 1].text == "." and tokens[token.tokenIndex - 2].text == "this":
            return False
        return True

    def get_usage(self):
        program = get_program(self.source_filenames)
        if not self.validate_metadata(program):
            raise Exception()

        source_class = program.packages[self.package_name].classes[self.class_name]
        target_class = program.packages[self.target_package_name].classes[self.target_class_name]
        field = program.packages[self.package_name].classes[self.class_name].fields[self.field_name]
        methods: dict = source_class.methods

        if 'static' not in field.modifiers:
            raise Exception()

        usages = list()

        for method_name, method in methods.items():
            tokens_info = TokensInfo(method.parser_context)  # tokens of ctx method
            param_tokens_info = TokensInfo(method.formalparam_context)
            param_text = list(map(lambda x: x.text, param_tokens_info.token_stream.tokens[
                                                    param_tokens_info.start:param_tokens_info.stop + 1]))
            method_declaration_info = TokensInfo(method.method_declaration_context)
            exps = tokens_info.get_token_index(tokens_info.token_stream.tokens, tokens_info.start, tokens_info.stop)

            for token in exps:
                if token.text == self.field_name:
                    if self.is_method_scope_var(tokens_info.token_stream.tokens, token, method):
                        continue
                    new_case = {
                        'method': method,
                        'tokens': list(filter(lambda t: t.line == token.line, exps))
                    }
                    usages.append(new_case)

        return program

    def propagate(self):
        pass

    def is_static(self, field: Field):
        return "static" in field.modifiers

    def move(self):
        # tokens_info = TokensInfo(_method.parser_context)  # tokens of ctx method
        program = self.get_usage()
        source_package = program.packages[self.package_name]
        source_class = source_package.classes[self.class_name]
        field = source_class.fields[self.field_name]
        if not self.is_static(field):
            print("right now, we won't move non static members")
            return False
        rewriter = Rewriter(program,
                            lambda x: f"{os.path.dirname(x)}/{os.path.splitext(os.path.basename(x))[0]}.rewritten.java")
        self.remove_field(field, rewriter)
        return True

    def remove_field(self, field: Field, rewriter: Rewriter):
        tokens = TokensInfo(field.parser_context)
        rewriter.replace(tokens, "")
        for mod_ctx in field.modifiers_parser_contexts:
            rewriter.replace(TokensInfo(mod_ctx), "")
        rewriter.apply()


if __name__ == '__main__':
    path = "/home/amiresm/Desktop/test_project"
    my_list = get_filenames_in_dir(path)
    refactoring = MoveFieldRefactoring(my_list, "hello", "classA", "a",
                                       "classB", "hello", "")

    refac = refactoring.move()
    print(refac)
