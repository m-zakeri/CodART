"""
## Introduction

Although it was planned to use a field universally for all classes, in reality the field is used only in
some subclasses. This situation can occur when planned features fail to pan out, for example.
because of this, we push down the field from the superclass into its related subclass.

## Pre and Post Conditions

### Pre Conditions:
1. There should exist a corresponding child and parent in the project.

2. The field that should be pushed down must be valid.

3. The user must enter the package's name, class's name and the fields that need to be added.

### Post Conditions:
1. The changed field's usages and callings will also change respectively.

2. There will be children and parents having their desired fields added or removed.
"""

from refactorings.utils import utils_listener_fast, utils2


class PushDownField:
    def __init__(self, source_filenames: list,
                 package_name: str,
                 superclass_name: str,
                 field_name: str,
                 class_names: list = [],
                 filename_mapping=lambda x: (x[:-5] if x.endswith(".java") else x) + ".java"):
        """
        The main function that does the process of pull up field refactoring.
                Adds the necessary fields to the subclasses and removes them from the superclass.

                Args:
                      source_filenames (list): A list of file names to be processed

                      package_name (str): The name of the package in which the refactoring has to be done (contains the superclass)

                      superclass_name (str): The name of the needed superclass

                      class_names (str): Name of the classes in which the refactoring has to be done (the classes to push down field from)

                      field_name (str): Name of the field that has to be refactored

                      filename_mapping (str): Mapping the file's name to the correct format so that it can be processed

                Returns:
                    No returns
        """
        self.source_filenames = source_filenames
        self.package_name = package_name
        self.superclass_name = superclass_name
        self.field_name = field_name
        self.class_names = class_names
        self.filename_mapping = filename_mapping



    def pre_condition_check(self, program, superclass):
        if self.package_name not in program.packages \
                or self.superclass_name not in program.packages[self.package_name].classes \
                or self.field_name not in program.packages[self.package_name].classes[self.superclass_name].fields:
            return False

        for m in superclass.methods:
            method: utils_listener_fast.Method = superclass.methods[m]
            for item in method.body_local_vars_and_expr_names:
                if isinstance(item, utils_listener_fast.ExpressionName):
                    if ((len(item.dot_separated_identifiers) == 1
                         and item.dot_separated_identifiers[0] == self.field_name)
                            or (len(item.dot_separated_identifiers) == 2
                                and item.dot_separated_identifiers[0] == "this"
                                and item.dot_separated_identifiers[1] == self.field_name)):
                        return False
        return True

    def do_refactor(self):
        program = utils2.get_program(self.source_filenames, print_status=True)
        superclass: utils_listener_fast.Class = program.packages[self.package_name].classes[self.superclass_name]

        if not self.pre_condition_check(program, superclass):
            print("Can't refactor")
            return False

        # all_derived_classes = [] # Not needed
        other_derived_classes = []
        classes_to_add_to = []
        for pn in program.packages:
            p: utils_listener_fast.Package = program.packages[pn]
            for cn in p.classes:
                c: utils_listener_fast.Class = p.classes[cn]
                if ((c.superclass_name == self.superclass_name and c.file_info.has_imported_class(self.package_name,
                                                                                                  self.superclass_name)) \
                        or (self.package_name is not None and c.superclass_name == self.package_name + '.' + self.superclass_name)):
                    # all_derived_classes.append(c)

                    if len(self.class_names) == 0 or cn in self.class_names:
                        if self.field_name in c.fields:
                            print("some classes have same variable")
                            return False
                        else:
                            classes_to_add_to.append(c)
                    else:
                        other_derived_classes.append(c)
                        
        # Check if the field is used from the superclass or other derived classes
        for pn in program.packages:
            p: utils_listener_fast.Package = program.packages[pn]
            for cn in p.classes:
                c: utils_listener_fast.Class = p.classes[cn]
                has_imported_superclass = c.file_info.has_imported_class(self.package_name, self.superclass_name)
                fields_of_superclass_type_or_others = []
                for fn in c.fields:
                    f: utils_listener_fast.Field = c.fields[fn]
                    if (f.name == self.field_name and has_imported_superclass) \
                            or (self.package_name is not None and f.name == (
                            self.package_name + '.' + self.superclass_name)):
                        fields_of_superclass_type_or_others.append(f.name)
                    if any((c.file_info.has_imported_class(o.package_name, o.name) and f.datatype == o.name)
                           or f.datatype == (o.package_name + '.' + o.name) for o in other_derived_classes):
                        fields_of_superclass_type_or_others.append(f.name)
                for mk in c.methods:
                    m: utils_listener_fast.Method = c.methods[mk]
                    local_vars_of_superclass_type_or_others = []
                    for item in m.body_local_vars_and_expr_names:
                        if isinstance(item, utils_listener_fast.LocalVariable):
                            if (item.datatype == self.superclass_name and has_imported_superclass) \
                                    or item.datatype == (self.package_name + '.' + self.superclass_name):
                                local_vars_of_superclass_type_or_others.append(item.identifier)
                            if any((c.file_info.has_imported_class(o.package_name, o.name) and item.datatype == o.name)
                                   or item.datatype == (o.package_name + '.' + o.name) for o in other_derived_classes):
                                local_vars_of_superclass_type_or_others.append(item.identifier)
                        elif isinstance(item, utils_listener_fast.ExpressionName):
                            if item.dot_separated_identifiers[-1] == self.field_name \
                                    and (
                                    (len(item.dot_separated_identifiers) == 2)
                                    or (len(item.dot_separated_identifiers) == 3 and item.dot_separated_identifiers[
                                0] == "this")
                            ) and (
                                    (item.dot_separated_identifiers[
                                         -2] in local_vars_of_superclass_type_or_others and len(
                                        item.dot_separated_identifiers) == 2)
                                    or item.dot_separated_identifiers[-2] in fields_of_superclass_type_or_others
                            ):
                                return False

        rewriter = utils2.Rewriter(program, self.filename_mapping)

        field = superclass.fields[self.field_name]
        if len(field.neighbor_names) == 0:
            rewriter.replace(field.get_tokens_info(), "")
            # Have to remove the modifiers too, because of the new grammar.
            for mod_ctx in field.modifiers_parser_contexts:
                rewriter.replace(utils_listener_fast.TokensInfo(mod_ctx), "")
        else:
            i = field.index_in_variable_declarators
            var_ctxs = field.all_variable_declarator_contexts
            if i == 0:
                to_remove = utils_listener_fast.TokensInfo(var_ctxs[i])
                to_remove.stop = utils_listener_fast.TokensInfo(var_ctxs[i + 1]).start - 1  # Include the ',' after it
                rewriter.replace(to_remove, "")
            else:
                to_remove = utils_listener_fast.TokensInfo(var_ctxs[i])
                to_remove.start = utils_listener_fast.TokensInfo(var_ctxs[i - 1]).stop + 1  # Include the ',' before it
                rewriter.replace(to_remove, "")

        is_public = "public" in field.modifiers
        is_protected = "protected" in field.modifiers
        modifier = ("public " if is_public else ("protected " if is_protected else ""))
        for c in classes_to_add_to:
            c_body_start = utils_listener_fast.TokensInfo(c.parser_context.classBody())
            c_body_start.stop = c_body_start.start  # Start and stop both point to the '{'
            rewriter.insert_after(c_body_start, "\n    " + modifier + field.datatype + " " + self.field_name \
                                  + ((" = " + field.initializer) if field.initializer is not None else "")
                                  + ";")

        rewriter.apply()
        return True


def test():
    print("Testing pushdown_field...")
    filenames = [
        "../benchmark_projects/tests/pushdown_field/test1.java",
        "../benchmark_projects/tests/pushdown_field/test2.java",
        "../benchmark_projects/tests/pushdown_field/test3.java",
        "../benchmark_projects/tests/pushdown_field/test4.java",
        "../benchmark_projects/tests/pushdown_field/test5.java",
        "../benchmark_projects/tests/pushdown_field/test6.java",
        "../benchmark_projects/tests/pushdown_field/test7.java",
    ]
    PushDownField(filenames, "pushdown_field_test_vehicle", "Vehicle", "brand").do_refactor()

    if PushDownField(filenames[:2], "pushdown_field_test1", "A", "a").do_refactor():
        print("1, 2: Success!")
    else:
        print("1, 2: Cannot refactor.")

    for i in range(2, 7):
        if PushDownField(filenames[:2] + [filenames[i]], "pushdown_field_test1", "A", "a").do_refactor():
            print("1, 2, " + str(i + 1) + ": Success!")
        else:
            print("1, 2, " + str(i + 1) + ": Cannot refactor.")


def test_ant():
    """
    target_files = [
        "tests/apache-ant/main/org/apache/tools/ant/types/ArchiveFileSet.java",
        "tests/apache-ant/main/org/apache/tools/ant/types/TarFileSet.java",
        "tests/apache-ant/main/org/apache/tools/ant/types/ZipFileSet.java"
    ]
    """
    ant_dir = "/home/ali/Desktop/code/TestProject/"
    print("Success!" if PushDownField(
        utils2.get_filenames_in_dir(ant_dir),
        "test_package",
        "App",
        "push_down",
        [],
        # lambda x: "tests/pushdown_field_ant/" + x[len(ant_dir):]
    ).do_refactor() else "Cannot refactor.")


if __name__ == "__main__":
    test_ant()
