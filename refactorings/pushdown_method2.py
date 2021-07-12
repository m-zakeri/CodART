"""
## Introduction

When a method was meant to be universal for all classes but in reality is used in only one or few subclass. 
This situation can occur when planned features fail to materialize.
Push down method refactoring removes the method from super class and adds it to correspondent subclasses.


## Pre and Post Conditions

### Pre Conditions:
1. The source package, class and method should exist.

2. If the superclass uses the method, The refactoring should not be implemented.

### Post Conditions:

1. If the subclasses has a method with the same name, The refactoring should not be implemented.

"""

from antlr4.TokenStreamRewriter import TokenStreamRewriter
from refactorings.utils.utils_listener_fast import TokensInfo, SingleFileElement
from refactorings.pullup_method_get_removemethod import get_removemethods
from refactorings.utils.utils2 import Rewriter, get_program, get_filenames_in_dir
from refactorings.utils import utils_listener_fast, utils2


class PushDownMethodRefactoring:
    def __init__(self, source_filenames: list,
                 package_name: str,
                 superclass_name: str,
                 method_key: str,
                 class_names: list = [],
                 filename_mapping=lambda x: x):
        """
        The main function that does the process of push down method refactoring.
               Removes the necessary method from the superclass and moves it to correspondent subclasses .

               Args:
                      source_filenames (list): A list of file names to be processed

                      package_name (str): The name of the package in which the refactoring has to be done(contains the classes)

                      superclass_name (str): Name of the superclass in which the refactoring has to be done (pushing down the method from here)

                      method_key (str): Name of the method which needs to be removed from the superclass/pushed down

                      class_names (list) : Names of the classes which user chooses manually to push down the method

                      filename_mapping (str): Mapping the file's name to the correct format so that it can be processed

               Returns:
                   No returns
        """
        self.source_filenames = source_filenames
        self.package_name = package_name
        self.superclass_name = superclass_name
        self.method_key = method_key
        self.class_names = class_names
        self.filename_mapping = filename_mapping

    def pre_propagation_check(self, program, superclass):
        # check input validation (pre-condition 1)
        if self.package_name not in program.packages \
                or self.superclass_name not in program.packages[self.package_name].classes \
                or self.method_key not in program.packages[self.package_name].classes[self.superclass_name].methods:
            return False

        # check if method is used in superclass (pre-condition 2)
        for m in superclass.methods:
            method: utils_listener_fast.Method = superclass.methods[m]
            for item in method.body_local_vars_and_expr_names:
                if isinstance(item, utils_listener_fast.MethodInvocation):
                    if ((len(item.dot_separated_identifiers) == 1
                         and item.dot_separated_identifiers[0] == self.method_key)
                            or (len(item.dot_separated_identifiers) == 2
                                and item.dot_separated_identifiers[0] == "this"
                                and item.dot_separated_identifiers[1] == self.method_key)):
                        return False
        return True

    def do_refactor(self):
        program = get_program(self.source_filenames, print_status=True)  # getting the program packages
        superclass: utils_listener_fast.Class = program.packages[self.package_name].classes[self.superclass_name]
        if not self.pre_propagation_check(program, superclass):
            return False

        other_derived_classes = []
        classes_to_add_to = []
        for p in program.packages:
            package: utils_listener_fast.Package = program.packages[p]
            for cn in package.classes:
                c: utils_listener_fast.Class = package.classes[cn]
                if ((c.superclass_name == self.superclass_name and c.file_info.has_imported_class(self.package_name,
                                                                                                  self.superclass_name)) or (
                        self.package_name is not None and c.superclass_name == self.package_name + '.' + self.superclass_name)):

                    # enable functionality of class name
                    if len(self.class_names) == 0 or cn in self.class_names:
                        # check for methods with same name (post-condition 1)
                        if self.method_key in c.methods:
                            print("some classes have same method")
                            return False
                        else:
                            for m in c.methods:
                                method: utils_listener_fast.Method = c.methods[m]
                                is_used = False
                                for item in method.body_local_vars_and_expr_names:
                                    if isinstance(item, utils_listener_fast.MethodInvocation) and \
                                            item.dot_separated_identifiers[0] + '()' == self.method_key:
                                        is_used = True
                                if is_used:
                                    classes_to_add_to.append(c)
                    else:
                        other_derived_classes.append(c)

        rewriter = utils2.Rewriter(program, self.filename_mapping)

        method = superclass.methods[self.method_key]

        is_public = "public" in method.modifiers
        is_protected = "protected" in method.modifiers
        is_private = "private" in method.modifiers

        for c in classes_to_add_to:
            c_body_start = utils_listener_fast.TokensInfo(c.parser_context.classBody())
            c_body_start.stop = c_body_start.start
            rewriter.insert_after(c_body_start, "\n\n    %s %s %s() {\n       %s\n    }\n"
                                  % (
                                      " ".join(method.modifiers), method.returntype, method.name,
                                      method.body_text[1:-1]))

        method_token_info = utils_listener_fast.TokensInfo(method.parser_context)
        rewriter.replace(method_token_info, "")

        rewriter.apply()
        return True


if __name__ == "__main__":
    my_list = get_filenames_in_dir('D:/archive/uni/CD/project/CodART/tests/pushdown_method/vehicle')
    print("Testing pushdown_method...")
    if PushDownMethodRefactoring(my_list, "pushdown_method_test_vehicle", "Vehicle", "epicMethod()").do_refactor():
        print("Success!")
    else:
        print("Cannot refactor.")
