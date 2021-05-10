from antlr4.TokenStreamRewriter import TokenStreamRewriter
from refactorings.utils.utils2 import get_program, Rewriter, get_filenames_in_dir
from refactorings.utils.utils_listener_fast import TokensInfo, SingleFileElement


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


if __name__ == '__main__':
    path = "/home/amiresm/Desktop/test_project"
    my_list = get_filenames_in_dir(path)
    refactoring = MoveFieldRefactoring(my_list, "hello", "Simple", "x",
                                       "Sample", "hello", 'hello')

    refac = refactoring.get_usage()
    print(refac)
