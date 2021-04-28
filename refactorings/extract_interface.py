"""
## Introduction

When multiple clients are using the same part of a class interface, or part of the interface in two classes is the same;
Extract Interface Refactoring moves this identical portion to its own interface.

## Pre and Post Conditions

### Pre Conditions:
1. precondition is whether the package name, all the class names and method names in
those classes exist.

2. The parameter types and return types of each method should be the same across the
classes.

### Post Conditions:

No specific Post Condition
"""

import os

from refactorings.utils import utils_listener_fast, utils2


class ExtractInterfaceRefactoring:
    def __init__(
            self, source_filenames: list,
            package_name: str,
            class_names: list,
            method_keys: list,
            interface_name: str,
            interface_filename: str,
            filename_mapping=lambda x: (x[:-5] if x.endswith(".java") else x) + ".java"):
        """The main function that does the process of extract interface refactoring.
                      Splits the identical,reused portion of the interface, creates a new interface,
                      and moves the split portion to the new interface.

                Args:
                      source_filenames (list): A list of file names to be processed

                      package_name (str): The name of the package in which the refactoring has to be done (contains the classes)

                      class_names (str): The classes which are going to implement the new interface

                      method_keys (str): The methods which are going to be included in the interface

                      filename_mapping (str): Mapping the file's name to the correct format so that it can be processed

                      interface_name (str): The new interface name

                      interface_filename (str): The new interface file name

                Returns:
                    No returns
            """
        self.source_filenames = source_filenames
        self.package_name = package_name
        self.class_names = class_names
        self.method_keys = method_keys
        self.interface_name = interface_name
        self.interface_filename = interface_filename
        self.filename_mapping = filename_mapping

    def do_refactor(self):
        program = utils2.get_program(self.source_filenames, print_status=True)
        if self.package_name not in program.packages \
                or any(
            class_name not in program.packages[self.package_name].classes
            for class_name in self.class_names
        ) \
                or any(
            method_key not in program.packages[self.package_name].classes[class_name].methods
            for class_name in self.class_names for method_key in self.method_keys
        ):
            return False

        method_returntypes = {}
        method_parameters = {}
        method_names = []
        for method_key in self.method_keys:
            method_names.append(method_key[:method_key.find('(')])

        rewriter = utils2.Rewriter(program, self.filename_mapping)

        for class_name in self.class_names:
            c: utils_listener_fast.Class = program.packages[self.package_name].classes[class_name]
            # Add implements to the class
            has_superinterface = False
            if c.parser_context.IMPLEMENTS() is not None:  # old: c.parser_context.superinterfaces()
                t = utils_listener_fast.TokensInfo(
                    c.parser_context.typeList())  # old: c.parser_context.superinterfaces()
                has_superinterface = True
            elif c.parser_context.EXTENDS() is not None:  # old: c.parser_context.superclass()
                t = utils_listener_fast.TokensInfo(c.parser_context.typeType())  # old: c.parser_context.superclass()
            elif c.parser_context.typeParameters() is not None:
                t = utils_listener_fast.TokensInfo(c.parser_context.typeParameters())
            else:
                # old: TokensInfo(c.parser_context.identifier())
                t = utils_listener_fast.TokensInfo(c.parser_context)
                t.stop = c.parser_context.IDENTIFIER().getSymbol().tokenIndex
            rewriter.insert_after(t, (", " if has_superinterface else " implements ") + self.interface_name)
            for method_key in self.method_keys:
                m: utils_listener_fast.Method = c.methods[method_key]
                # Check if the return types / parameter types are the same
                # Or add to dictionary
                if method_key in method_returntypes:
                    if method_returntypes[method_key] != m.returntype:
                        return False
                    if len(method_parameters[method_key]) != len(m.parameters):
                        return False
                    for i in range(len(m.parameters)):
                        if method_parameters[method_key][i][0] != m.parameters[i][0]:
                            return False
                else:
                    method_returntypes[method_key] = m.returntype
                    method_parameters[method_key] = m.parameters
                # Manage method modifiers
                if len(m.modifiers_parser_contexts) > 0:
                    t = utils_listener_fast.TokensInfo(m.modifiers_parser_contexts[0])
                else:
                    t = m.get_tokens_info()
                rewriter.insert_before_start(
                    t,  # old: m.get_tokens_info() # without requiring t
                    ("" if "@Override" in m.modifiers else "@Override\n    ")
                    + ("" if "public" in m.modifiers else "public ")
                )
                for i in range(len(m.modifiers)):
                    mm = m.modifiers[i]
                    if mm == "private" or mm == "protected":
                        t = utils_listener_fast.TokensInfo(
                            m.modifiers_parser_contexts[i])  # old: m.parser_context.methodModifier(i)
                        rewriter.replace(t, "")

        # Change variable types to the interface if only interface methods are used.
        for package_name in program.packages:
            p: utils_listener_fast.Package = program.packages[package_name]
            for class_name in p.classes:
                c: utils_listener_fast.Class = p.classes[class_name]
                fields_of_interest = {}
                for fn in c.fields:
                    f: utils_listener_fast.Field = c.fields[fn]
                    d = False
                    for cn in self.class_names:
                        if (f.datatype == cn and f.file_info.has_imported_class(package_name, cn)) \
                                or (package_name is not None and f.datatype == package_name + '.' + cn):
                            d = True
                            break
                    if d and "private" in f.modifiers:
                        fields_of_interest[f.name] = f
                for method_key in c.methods:
                    m: utils_listener_fast.Method = c.methods[method_key]
                    vars_of_interest = {}
                    for item in m.body_local_vars_and_expr_names:
                        if isinstance(item, utils_listener_fast.LocalVariable):
                            for cn in self.class_names:
                                if (item.datatype == cn and c.file_info.has_imported_class(package_name, cn)) \
                                        or (package_name is not None and item.datatype == package_name + '.' + cn):
                                    vars_of_interest[item.identifier] = item
                                    break
                        if isinstance(item, utils_listener_fast.MethodInvocation):
                            if len(item.dot_separated_identifiers) == 2 or \
                                    (len(item.dot_separated_identifiers) == 3 and item.dot_separated_identifiers[
                                        0] == "this"):
                                if item.dot_separated_identifiers[-2] in vars_of_interest:
                                    if item.dot_separated_identifiers[-1] not in method_names:
                                        vars_of_interest.pop(item.dot_separated_identifiers[-2])
                                elif item.dot_separated_identifiers[-2] in fields_of_interest \
                                        and item.dot_separated_identifiers[-1] not in method_names:
                                    fields_of_interest.pop(item.dot_separated_identifiers[-2])
                    for var_name in vars_of_interest:
                        var = vars_of_interest[var_name]
                        if m.file_info.has_imported_package(package_name):
                            # old: var.parser_context.unannType()
                            rewriter.replace(utils_listener_fast.TokensInfo(var.parser_context.typeType()),
                                             self.interface_name)
                        else:
                            if package_name is None:
                                break
                            # old: var.parser_context.unannType()
                            rewriter.replace(utils_listener_fast.TokensInfo(var.parser_context.typeType()),
                                             package_name + '.' + self.interface_name)
                for field_name in fields_of_interest:
                    f = fields_of_interest[field_name]
                    if c.file_info.has_imported_package(package_name):
                        typename = self.interface_name
                    else:
                        if package_name is None:
                            break
                        typename = package_name + '.' + self.interface_name
                    if len(f.neighbor_names) == 0:
                        rewriter.replace(utils_listener_fast.TokensInfo(f.parser_context.typeType()),
                                         typename)  # old: f.parser_context.unannType()
                    else:
                        if not any(nn in fields_of_interest for nn in f.neighbor_names):
                            t = utils_listener_fast.TokensInfo(
                                f.all_variable_declarator_contexts[f.index_in_variable_declarators])
                            if f.index_in_variable_declarators == 0:
                                t.stop = utils_listener_fast.TokensInfo(
                                    f.all_variable_declarator_contexts[f.index_in_variable_declarators + 1]).start - 1
                            else:
                                t.start = utils_listener_fast.TokensInfo(
                                    f.all_variable_declarator_contexts[f.index_in_variable_declarators - 1]).start + 1
                            rewriter.replace(t, "")
                            rewriter.insert_after(
                                f.get_tokens_info(),
                                "\n    private " + typename + " " + f.name + (
                                    " = " + f.initializer + ";" if f.initializer is not None else ";")
                            )

        # Create the interface
        interface_file_content = (
                "package " + package_name + ";\n\n"
                + "public interface " + self.interface_name + "\n"
                + "{\n"
        )
        for method_key in self.method_keys:
            method_name = method_key[:method_key.find('(')]
            interface_file_content += "    " + method_returntypes[method_key] + " " + method_name + "("
            if len(method_parameters[method_key]) > 0:
                interface_file_content += method_parameters[method_key][0][0] + " " + method_parameters[method_key][0][
                    1]
            for i in range(1, len(method_parameters[method_key])):
                param = method_parameters[method_key][i]
                interface_file_content += ", " + param[0] + " " + param[1]
            interface_file_content += ");\n"
        interface_file_content += "}\n"

        if not os.path.exists(self.interface_filename[:self.interface_filename.rfind('/')]):
            os.makedirs(self.interface_filename[:self.interface_filename.rfind('/')])
        file = open(self.interface_filename, "w+")
        file.write(interface_file_content)
        file.close()

        rewriter.apply()
        return True


def test():
    print("Testing extract_interface...")
    filenames = [
        "../benchmark_projects/tests/extract_interface/A.java",
        "../benchmark_projects/tests/extract_interface/B.java",
        "../benchmark_projects/tests/extract_interface/C.java",
        "../benchmark_projects/tests/extract_interface/D.java",
        "../benchmark_projects/tests/extract_interface/E.java",
        "../benchmark_projects/tests/extract_interface/U.java",
    ]
    if ExtractInterfaceRefactoring(filenames, "test", ["A", "B"], ["a(int,float)", "b()"], "Iab",
                                   "../tests/extract_interface/Iab.re.java").do_refactor():
        print("A, B: Success!")
    else:
        print("A, B: Cannot refactor.")
    for third_class in ["C", "D", "E"]:
        if ExtractInterfaceRefactoring(filenames, "test", ["A", "B", third_class], ["a(int,float)", "b()"], "Iab",
                                       "../tests/extract_interface/Iab.re.java").do_refactor():
            print("A, B, " + third_class + ": Success!")
        else:
            print("A, B, " + third_class + ": Cannot refactor.")


def main():
    """
    target_files = [
        "tests/apache-ant/main/org/apache/tools/ant/input/InputRequest.java",
        "tests/apache-ant/main/org/apache/tools/ant/input/MultipleChoiceInputRequest.java"
    ]
    """
    ant_dir = "/home/ali/Desktop/code/TestProject/"
    print("Success!" if ExtractInterfaceRefactoring(
        utils2.get_filenames_in_dir(ant_dir),
        "test_package",
        ["AppChild1", "AppChild2"],
        ["printTest()"],
        "ExtractedInterface",
        "/home/ali/Desktop/code/TestProject/src/test_package/ExtractedInterface.java",
        # lambda x: "tests/extract_interface_ant/" + x[len(ant_dir):]
    ).do_refactor() else "Cannot refactor.")


