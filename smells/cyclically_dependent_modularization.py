from antlr4.TokenStreamRewriter import TokenStreamRewriter
from refactorings.utils.utils2 import get_program, Rewriter, get_filenames_in_dir
from refactorings.utils.utils_listener_fast import TokensInfo, SingleFileElement, Class


class CyclicDependentModularization(object):
    def __init__(self, source_filenames: list):
        self.source_filenames = source_filenames
        self.program = get_program(self.source_filenames)

    def check(self):
        super_classes = []
        packages = self.program.packages
        for package_item in packages:
            package_item_dic = self.program.packages[package_item]
            for classes_item in package_item_dic.classes:
                class_item_dic = package_item_dic.classes[classes_item]
                if class_item_dic.modifiers[0] == 'abstract':
                    while class_item_dic.superclass_name:
                        super_class = self.find_super_type(class_item_dic.superclass_name)
                        if super_class.modifiers[0] == 'abstract':
                            print("Find : cyclic dependent modularization...")
                            return
                        class_item_dic = super_class

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
    CyclicDependentModularization(mylist).check()
    print("finish ....")
