"""
## Introduction

When subclasses grow and get developed separately, identical (or nearly identical) fields and methods appear.
Pull up field refactoring removes the repetitive field from subclasses and moves it to a superclass.

## Pre and Post Conditions

### Pre Conditions:
1. There should exist a corresponding child and parent in the project.

2. The field that should be pulled up must be valid.

3. The user must enter the package's name, class's name and the fields that need to be removed.

### Post Conditions:
1. The changed field's usages and callings will also change respectively.

2. There will be children and parents having their desired fields added or removed.

3. Check for multilevel inheritance.

"""

from refactorings.utils import utils_listener_fast, utils2


class PullUpFieldRefactoring:
    def __init__(self, source_filenames: list,
                 package_name: str,
                 class_name: str,
                 field_name: str,
                 filename_mapping=lambda x: (x[:-5] if x.endswith(".java") else x) + ".java"):
        """The main function that does the process of pull up field refactoring.
               Removes the repetitive fields from the subclasses, creates the superclass,
               and moves the fields to the superclass.

               Args:
                   source_filenames (list): A list of file names to be processed

                   package_name (str): The name of the package in which the refactoring has to be done (contains the classes/superclasses)

                   class_name (str): Name of the class that the field is pulled up from

                   field_name (str): Name of the field that has to be refactored

                   filename_mapping (str): Mapping the file's name to the correct format so that it can be processed

               Returns:
                   No returns
            """
        self.source_filenames = source_filenames
        self.package_name = package_name
        self.class_name = class_name
        self.field_name = field_name
        self.filename_mapping = filename_mapping

    def do_refactor(self):
        program = utils2.get_program(self.source_filenames, print_status=True)
        # print(program.packages)
        if self.package_name not in program.packages \
                or self.class_name not in program.packages[self.package_name].classes \
                or self.field_name not in program.packages[self.package_name].classes[self.class_name].fields:
            return False

        _class: utils_listener_fast.Class = program.packages[self.package_name].classes[self.class_name]
        if _class.superclass_name is None:
            return False

        superclass_name = _class.superclass_name

        superclass: utils_listener_fast.Class = program.packages[self.package_name].classes[superclass_name]
        superclass_body_start = utils_listener_fast.TokensInfo(superclass.parser_context.classBody())
        superclass_body_start.stop = superclass_body_start.start  # Start and stop both point to the '{'

        if self.field_name in superclass.fields:
            return False

        datatype = _class.fields[self.field_name].datatype

        fields_to_remove = []
        for pn in program.packages:
            p: utils_listener_fast.Package = program.packages[pn]
            for cn in p.classes:
                c: utils_listener_fast.Class = p.classes[cn]
                if ((c.superclass_name == superclass_name and c.file_info.has_imported_class(self.package_name,
                                                                                             superclass_name))
                    or (
                            self.package_name is not None and c.superclass_name == self.package_name + '.' + superclass_name)) \
                        and self.field_name in c.fields \
                        and c.fields[self.field_name].datatype == datatype:
                    fields_to_remove.append(c.fields[self.field_name])

        if len(fields_to_remove) == 0:
            return False

        is_public = False
        is_protected = True
        for field in fields_to_remove:
            field: utils_listener_fast.Field = field
            is_public = is_public or "public" in field.modifiers
            is_protected = is_protected and ("protected" in field.modifiers or "private" in field.modifiers)

        rewriter = utils2.Rewriter(program, self.filename_mapping)

        rewriter.insert_after(superclass_body_start, "\n    " + (
            "public " if is_public else (
                "protected " if is_protected else "")) + datatype + " " + self.field_name + ";")

        for field in fields_to_remove:
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
                    to_remove.stop = utils_listener_fast.TokensInfo(
                        var_ctxs[i + 1]).start - 1  # Include the ',' after it
                    rewriter.replace(to_remove, "")
                else:
                    to_remove = utils_listener_fast.TokensInfo(var_ctxs[i])
                    to_remove.start = utils_listener_fast.TokensInfo(
                        var_ctxs[i - 1]).stop + 1  # Include the ',' before it
                    rewriter.replace(to_remove, "")

            # Add initializer to class constructor if initializer exists in field declaration
            if field.initializer is not None:
                _class: utils_listener_fast.Class = program.packages[field.package_name].classes[field.class_name]
                initializer_statement = (field.name
                                         + " = "
                                         + ("new " + field.datatype + " " if field.initializer.startswith('{') else "")
                                         + field.initializer
                                         + ";")
                has_contructor = False
                for class_body_decl in _class.parser_context.classBody().getChildren():
                    if class_body_decl.getText() in ['{', '}']:
                        continue
                    member_decl = class_body_decl.memberDeclaration()
                    if member_decl is not None:
                        constructor = member_decl.constructorDeclaration()
                        if constructor is not None:
                            body = constructor.constructorBody  # Start token = '{'
                            body_start = utils_listener_fast.TokensInfo(body)
                            body_start.stop = body_start.start  # Start and stop both point to the '{'
                            rewriter.insert_after(body_start, "\n        " + initializer_statement)
                            has_contructor = True
                if not has_contructor:
                    body = _class.parser_context.classBody()
                    body_start = utils_listener_fast.TokensInfo(body)
                    body_start.stop = body_start.start  # Start and stop both point to the '{'
                    rewriter.insert_after(body_start,
                                          "\n    " + _class.modifiers[
                                              0] + " " + _class.name + "() { " + initializer_statement + " }"
                                          )

        rewriter.apply()

        # check for multilevel inheritance recursively.

        if _class.superclass_name is not None:
            PullUpFieldRefactoring(self.source_filenames, self.package_name, _class.superclass_name, "id").do_refactor()
        return True


def test():
    print("Testing pullup_field...")
    filenames = [
        "D:/archive/uni/CD/project/CodART/tests/pullup_field/test5.java",
        "D:/archive/uni/CD/project/CodART/tests/pullup_field/test6.java",
        # "../benchmark_projects/tests/pullup_field/test1.java",
        # "../benchmark_projects/tests/pullup_field/test2.java",
        # "../benchmark_projects/tests/pullup_field/test3.java",
        # "../benchmark_projects/tests/pullup_field/test4.java"
    ]

    if PullUpFieldRefactoring(filenames, "pullup_field_test5", "C", "id").do_refactor():
        print("Success!")
    else:
        print("Cannot refactor.")


def test_ant():
    """
    target_files = [
        "tests/apache-ant/main/org/apache/tools/ant/types/ArchiveFileSet.java",
        "tests/apache-ant/main/org/apache/tools/ant/types/TarFileSet.java",
        "tests/apache-ant/main/org/apache/tools/ant/types/ZipFileSet.java"
    ]
    """
    ant_dir = "/home/ali/Desktop/code/TestProject/"
def main(project_dir: str, package_name: str, children_class: str, field_name: str):
    print("Pullup Field")
    print("Success!" if PullUpFieldRefactoring(
        utils2.get_filenames_in_dir(project_dir),
        package_name,
        children_class,
        field_name
        # lambda x: "tests/pullup_field_ant/" + x[len(ant_dir):]
    ).do_refactor() else "Cannot refactor.")


if __name__ == "__main__":
    test()
