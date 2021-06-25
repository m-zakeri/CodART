from antlr4.TokenStreamRewriter import TokenStreamRewriter
from refactorings.utils.utils2 import get_program, Rewriter, get_filenames_in_dir
from refactorings.utils.utils_listener_fast import TokensInfo, SingleFileElement, Class


class CyclicHierarchy(object):
    def __init__(self, source_filenames: list):
        self.source_filenames = source_filenames
        self.program = get_program(self.source_filenames)

    def check(self):
        # package = self.program.packages
        for package_item in self.program.packages:
            package_item_dic = self.program.packages[package_item]
            for classes_item in package_item_dic.classes:
                class_item_dic = package_item_dic.classes[classes_item]
                if class_item_dic.superclass_name:
                    super_class = self.find_super_type(class_item_dic.superclass_name)
                    a = 2

    def find_super_type(self, class_name):
        for package_item in self.program.packages:
            package_item_dic = self.program.packages[package_item]
            for classes_item in package_item_dic.classes:
                class_item_dic = package_item_dic.classes[classes_item]
                if class_item_dic.name == class_name:
                    return class_item_dic

if __name__ == "__main__":
    mylist = get_filenames_in_dir('C:/Users/Qafari/Desktop/propagationTest')
    print("start ....")
    CyclicHierarchy(mylist).check()
    print("finish ....")
