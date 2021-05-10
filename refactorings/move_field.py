from antlr4.TokenStreamRewriter import TokenStreamRewriter
from refactorings.utils.utils2 import get_program, Rewriter, get_filenames_in_dir
from refactorings.utils.utils_listener_fast import TokensInfo, SingleFileElement, Field, Class
import os


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
            method_params = method.parameters
            for token in exps:
                if token.text == self.field_name:
                    if param_tokens_info is not None:
                        if token.text in param_text:
                            if tokens_info.token_stream.tokens[token.tokenIndex - 1].text == '.' and tokens_info.token_stream.tokens[token.tokenIndex - 2].text == 'this':
                                print(token)
                            else:
                                continue

                    new_case = {
                        'method': method,
                        'tokens': list(filter(lambda t: t.line == token.line, exps))
                    }
                    usages.append(new_case)

        return program

    def propagate(self):
        pass

    def move(self):
        # tokens_info = TokensInfo(_method.parser_context)  # tokens of ctx method
        program = self.get_usage()
        source_package = program.packages[self.package_name]
        source_class = source_package.classes[self.class_name]
        target_class = source_package.classes[self.target_class_name]
        field = source_class.fields[self.field_name]
        rewriter = Rewriter(program,
                            lambda x: f"{os.path.dirname(x)}/{os.path.splitext(os.path.basename(x))[0]}.rewritten.java")

        self.__remove_field_from_src(field, rewriter)
        self.__move_field_to_dst(target_class, field, rewriter)
        rewriter.apply()

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
        if field.initializer.startswith("new"):
            field.initializer = field.initializer.replace("new", "new ", 1)

        new_field = f'\n\t{" ".join(field.modifiers)} {field.datatype} {field.name}{f" = {field.initializer};" if field.initializer else ";"}\n'
        target_class_tokens = TokensInfo(target.body_context)
        rewriter.insert_after_start(target_class_tokens, new_field)


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
