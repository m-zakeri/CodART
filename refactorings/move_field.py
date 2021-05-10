from antlr4.TokenStreamRewriter import TokenStreamRewriter
from refactorings.utils.utils2 import get_program, Rewriter, get_filenames_in_dir
from refactorings.utils.utils_listener_fast import TokensInfo, SingleFileElement, Field
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
            raise KeyError(f"The class {self.class_name} does not exist in the program")
        if self.target_class_name not in program.packages[self.target_package_name].classes:
            raise KeyError(f"The class {self.target_class_name} does not exist in the program")
        if self.field_name not in program.packages[self.package_name].classes[
                    self.class_name].fields:
            raise KeyError(f"The class {self.target_class_name} does not exist in the program")


    def get_usage(self):
        program = get_program(self.source_filenames)
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
        rewriter = Rewriter(program, lambda x: f"{os.path.dirname(x)}/{os.path.splitext(os.path.basename(x))[0]}.rewritten.java")
        self.remove_field(field, rewriter)
        return True

    def remove_field(self, field: Field, rewriter: Rewriter):
        tokens = TokensInfo(field.parser_context)
        rewriter.replace(tokens, "")
        for mod_ctx in field.modifiers_parser_contexts:
            rewriter.replace(TokensInfo(mod_ctx), "")
        rewriter.apply()


if __name__ == '__main__':
    path = "/home/loop/IdeaProjects/Sample"
    my_list = get_filenames_in_dir(path)
    refactoring = MoveFieldRefactoring(my_list, "sample", "Test3", "toBeMoved",
                                       "Test", "sample", "")

    refac = refactoring.move()
    print(refac)
