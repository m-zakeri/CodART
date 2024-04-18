import os
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from antlr4 import *
from openunderstand.analysis_passes.call_callby import *


class GeneralScopeListener(JavaParserLabeledListener):

    # available_imported_classes -> corresponds to the list of imported classes' full names
    def __init__(
        self,
        file_full_path,
        available_package_classes,
        available_class_methods,
        available_class_fields,
        class_parents,
    ):
        self.scope_stack = [[file_full_path]]
        self.available_imported_classes = set()
        self.class_parents = class_parents
        # the three following variables are derived from self.init_info
        # customized for the current file under consideration
        self.classes_repo = []
        self.class_methods_repo = {}
        self.class_fields_repo = {}

        self.all_classes_repo = set()

        self.init_info = [
            available_package_classes,
            available_class_methods,
            available_class_fields,
        ]
        self.current_long_name = ""
        self.current_class_name = ""
        self.current_package = None
        self.UNKNOWN_PACKAGE = "<unknown_package>"
        self.abspath = file_full_path

        self.in_class_declaration = False
        self.is_child_class = False
        self.parent_class_type = None

        self.in_field_declaration = False
        self.is_field_non_primitive_type = False
        self.non_primitive_field_type = None

        self.in_method_declaration = False

    def fill_all_classes_repo(self):
        try:
            for classname in self.classes_repo:
                self.all_classes_repo.add(classname)
            for classname in self.available_imported_classes:
                self.all_classes_repo.add(classname)
        except Exception as e:
            print("ERROR fill_all_classes_repo : ", e)

    def fill_class_parents(self):
        try:
            for classname in self.class_parents.keys():
                self.class_parents[classname] = self.get_fullname(
                    self.class_parents[classname]
                )
        except Exception as e:
            print("ERROR fill_class_parents : ", e)

    def add_unknown_package(self):
        try:
            if self.current_package is None:
                target_name = self.UNKNOWN_PACKAGE + "," + self.abspath
                if target_name in self.init_info[0]:
                    self.current_package = target_name
                self.classes_repo = self.init_info[0][self.current_package]
        except Exception as e:
            print("ERROR add_unknown_package : ", e)

    def add_class_methods(self):
        try:
            for classname in self.all_classes_repo:
                if classname in self.init_info[1].keys():
                    self.class_methods_repo[classname] = self.init_info[1][classname]
        except Exception as e:
            print("ERROR add_class_methods : ", e)

    def add_class_fields(self):
        try:
            for classname in self.all_classes_repo:
                if classname in self.init_info[2].keys():
                    self.class_fields_repo[classname] = self.init_info[2][classname]
                    if classname not in self.class_fields_repo.keys():
                        self.class_fields_repo[classname] = []
                    for i in range(len(self.class_fields_repo[classname])):
                        typename = self.class_fields_repo[classname][i]["tp"]
                        self.class_fields_repo[classname][i] = {
                            "tp": self.get_fullname(typename),
                            "name": self.class_fields_repo[classname][i]["name"],
                        }
        except Exception as e:
            print("ERROR add_class_fields : ", e)

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        try:
            package_text = ctx.getText()
            package_name = package_text[
                package_text.find("package") + 7 : package_text.find(";")
            ]
            self.scope_stack[0].append(package_name)
            self.current_package = package_name
            self.classes_repo = self.init_info[0][package_name]
            self.current_long_name = package_name
        except Exception as e:
            print("ERROR enterPackageDeclaration : ", e)

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        try:
            import_text = ctx.getText()
            imported_entity = import_text[
                import_text.find("import") + 6 : import_text.find(";")
            ]
            index = imported_entity.rfind(".")
            package_prefix = imported_entity[:index]
            if import_text[index + 1 :] == "*":
                for classname in self.init_info[0][package_prefix]:
                    self.available_imported_classes.add(classname)
            else:
                self.available_imported_classes.add(imported_entity)
        except Exception as e:
            print("ERROR enterImportDeclaration : ", e)

    def enterFormalParameters(self, ctx: JavaParserLabeled.FormalParametersContext):
        try:
            if self.in_method_declaration:
                params_text = ctx.getText()
                self.scope_stack[len(self.scope_stack) - 1]["params"] = params_text[
                    1:-1
                ]
            self.in_method_declaration = False
        except Exception as e:
            print("ERROR enterFormalParameters : ", e)

    # push method entity_id to scope_stack
    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        try:
            method_name = str(ctx.IDENTIFIER())
            new_scope_info = {
                "tp": "method",
                "name": self.current_long_name + "." + method_name,
                "params": ctx.formalParameters().getText()[1:-1],
            }
            self.scope_stack.append(new_scope_info)
            self.in_method_declaration = True
        except Exception as e:
            print("ERROR enterMethodDeclaration : ", e)

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        try:
            self.in_field_declaration = True
        except Exception as e:
            print("ERROR enterFieldDeclaration : ", e)

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        try:
            self.in_field_declaration = False
            self.is_field_non_primitive_type = False
            self.non_primitive_field_type = None
        except Exception as e:
            print("ERROR exitFieldDeclaration : ", e)

    def enterClassOrInterfaceType(
        self, ctx: JavaParserLabeled.ClassOrInterfaceTypeContext
    ):
        try:
            if type(ctx.parentCtx) is JavaParserLabeled.TypeTypeContext:
                if self.in_field_declaration:
                    self.is_field_non_primitive_type = True
                    self.non_primitive_field_type = ctx.getText()
                elif self.in_class_declaration:
                    self.is_child_class = True
                    self.parent_class_type = ctx.getText()
        except Exception as e:
            print("ERROR enterClassOrInterfaceType : ", e)

    def enterTypeDeclaration(self, ctx: JavaParserLabeled.TypeDeclarationContext):
        try:
            self.add_unknown_package()
            for info in self.init_info[0]:
                self.classes_repo.extend(self.init_info[0][info])
            self.fill_all_classes_repo()
            self.add_class_methods()
            self.add_class_fields()
            self.fill_class_parents()
        except Exception as e:
            print("ERROR enterTypeDeclaration : ", e)

    # push class entity_id to scope_stack
    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        try:
            self.in_class_declaration = True
            class_name = str(ctx.IDENTIFIER())
            self.current_long_name = (
                self.current_long_name + "." + class_name
                if self.current_long_name != ""
                else class_name
            )
            self.current_class_name = self.current_long_name
        except Exception as e:
            print("ERROR enterClassDeclaration : ", e)

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        try:
            self.in_class_declaration = False
            self.is_child_class = False
            self.parent_class_type = None
        except Exception as e:
            print("ERROR enterClassBody : ", e)

    # for classes
    def get_fullname(self, name):
        try:
            if name in self.available_imported_classes:
                return name
            if name in self.classes_repo:
                return name
            for imported_class in self.available_imported_classes:
                if imported_class.endswith("." + name):
                    return imported_class
            for infile_class in self.classes_repo:
                if infile_class.endswith("." + name):
                    return infile_class
            return name
        except Exception as e:
            print("ERROR get_fullname : ", e)


class InitializerListener(JavaParserLabeledListener):
    def __init__(
        self,
        file_full_address,
        available_packages=None,
        available_package_classes=None,
        available_class_methods=None,
        available_class_fields=None,
        class_parents=None,
    ):
        self.abspath = file_full_address
        self.available_packages = (
            available_packages if available_packages is not None else set()
        )
        # each key in the following dictionary should be the name of a package
        # the value of each key is an array with the name of classes
        # each element of this array can also be a dictionary
        # corresponding to classes defined with in classes
        self.available_package_classes = (
            available_package_classes if available_package_classes is not None else {}
        )
        self.available_class_methods = (
            available_class_methods if available_class_methods is not None else {}
        )
        self.available_class_fields = (
            available_class_fields if available_class_fields is not None else {}
        )
        self.class_parents = class_parents if class_parents is not None else {}
        self.current_package_name = None
        self.UNKNOWN_PACKAGE = "<unknown_package>"
        self.current_scope = [self.abspath]
        self.current_long_name = ""
        self.current_class_name = ""

        self.in_class_declaration = False
        self.is_child_class = False
        self.parent_class_type = None

        self.in_field_declaration = False
        self.is_type_non_primitive = False
        self.non_primitive_type = None

        self.in_method_declaration = False

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        package_text = ctx.getText()
        package_name = package_text[
            package_text.find("package") + 7 : package_text.find(";")
        ]
        self.available_packages.add(package_name)
        self.current_package_name = package_name
        self.current_scope.append({"tp": "package", "name": package_name})
        self.current_long_name = package_name

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        self.add_unknown_package()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.add_unknown_package()
        class_name = str(ctx.IDENTIFIER())
        self.current_long_name = (
            self.current_long_name + "." + class_name
            if self.current_long_name != ""
            else class_name
        )
        self.current_class_name = self.current_long_name
        if self.current_package_name not in self.available_package_classes.keys():
            self.available_package_classes[self.current_package_name] = []
        self.available_package_classes[self.current_package_name].append(
            self.current_long_name
        )
        self.current_scope.append({"tp": "class", "name": self.current_long_name})

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        index = self.current_long_name.rfind(".")
        if index > 0:
            self.current_long_name = self.current_long_name[:index]
        else:
            self.current_long_name = ""
        self.current_scope.pop()
        self.in_class_declaration = False
        self.is_child_class = False
        self.parent_class_type = None

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        self.in_field_declaration = True

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        self.in_field_declaration = False
        self.is_type_non_primitive = False
        self.non_primitive_type = None

    def enterTypeType(self, ctx: JavaParserLabeled.TypeTypeContext):
        if type(ctx.parentCtx) is JavaParserLabeled.ClassDeclarationContext:
            self.in_class_declaration = True
            self.is_child_class = True

    def enterClassOrInterfaceType(
        self, ctx: JavaParserLabeled.ClassOrInterfaceTypeContext
    ):
        if type(ctx.parentCtx) is JavaParserLabeled.TypeTypeContext:
            if self.in_field_declaration:
                self.is_type_non_primitive = True
                self.non_primitive_type = ctx.getText()
            elif self.in_class_declaration and self.is_child_class:
                self.parent_class_type = ctx.getText()
                self.class_parents[
                    self.current_scope[len(self.current_scope) - 1]["name"]
                ] = self.parent_class_type

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        self.in_class_declaration = False
        self.is_child_class = False
        self.parent_class_type = None

    def enterVariableDeclaratorId(
        self, ctx: JavaParserLabeled.VariableDeclaratorIdContext
    ):
        if self.in_field_declaration and self.is_type_non_primitive:
            field_identifier = str(ctx.IDENTIFIER())
            if self.current_class_name not in self.available_class_fields.keys():
                self.available_class_fields[self.current_class_name] = []
            self.available_class_fields[self.current_class_name].append(
                {"tp": self.non_primitive_type, "name": field_identifier}
            )

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        method_name = str(ctx.IDENTIFIER())
        if self.current_class_name not in self.available_class_methods.keys():
            self.available_class_methods[self.current_class_name] = []
        self.available_class_methods[self.current_class_name].append(
            {
                "name": self.current_long_name + "." + method_name,
                "params": ctx.formalParameters().getText()[1:-1],
            }
        )
        self.current_long_name = self.current_long_name + "." + method_name
        self.current_scope.append(
            {
                "tp": "method",
                "name": self.current_long_name,
                "params": ctx.formalParameters().getText()[1:-1],
            }
        )
        self.in_method_declaration = True

    def enterFormalParameters(self, ctx: JavaParserLabeled.FormalParametersContext):
        if self.in_method_declaration:
            params_text = ctx.getText()
            length = len(self.available_class_methods[self.current_class_name])
            self.available_class_methods[self.current_class_name][length - 1][
                "params"
            ] = params_text[1:-1]
            self.current_scope[len(self.current_scope) - 1]["params"] = params_text[
                1:-1
            ]
        self.in_method_declaration = False

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        index = self.current_long_name.rfind(".")
        self.current_long_name = self.current_long_name[:index]
        self.current_scope.pop()

    # should be called after walking the tree
    def get_status(self):
        return [
            self.available_packages,
            self.available_package_classes,
            self.available_class_methods,
            self.available_class_fields,
            self.class_parents,
        ]

    def add_unknown_package(self):
        if self.current_package_name is None:
            self.current_package_name = self.UNKNOWN_PACKAGE + "," + self.abspath
            self.available_packages.add(self.current_package_name)


def initialize(root_folder):
    available_packages = None
    available_package_classes = None
    available_class_methods = None
    available_class_fields = None
    class_parents = None
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".java"):
                (
                    available_packages,
                    available_package_classes,
                    available_class_methods,
                    available_class_fields,
                    class_parents,
                ) = walk_on_file(
                    filepath,
                    available_packages,
                    available_package_classes,
                    available_class_methods,
                    available_class_fields,
                    class_parents,
                )
    return [
        available_packages,
        available_package_classes,
        available_class_methods,
        available_class_fields,
        class_parents,
    ]


def walk_on_file(
    filepath,
    available_packages,
    available_package_classes,
    available_class_methods,
    available_class_fields,
    class_parents,
):
    address = filepath
    listener = InitializerListener(
        filepath,
        available_packages,
        available_package_classes,
        available_class_methods,
        available_class_fields,
        class_parents,
    )
    fs = FileStream(address)
    lexer = JavaLexer(fs)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    tree = parser.compilationUnit()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    return listener.get_status()


def extract_data_from_all_files(available_info, root_folder):
    file_call_infos = {}
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".java"):
                file_call_infos[filepath] = extract_data_from_file(
                    available_info, filepath
                )
    return file_call_infos


def extract_data_from_file(available_info, file_abspath):
    listener = CallAndCallBy(
        file_abspath,
        available_info[1],
        available_info[2],
        available_info[3],
        available_info[4],
    )
    fs = FileStream(file_abspath)
    lexer = JavaLexer(fs)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    tree = parser.compilationUnit()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    return listener.get_result_dicts()


def main():
    print(os.path.abspath(__file__))
    abspath = "F:\\IUST_4001\\Compiler\\Project\\OpenUnderstand\\OpenUnderstand\\benchmark\\calculator_app\\src"
    # abspath = 'F:\\IUST_4001\\Compiler\\Project\\OpenUnderstand\\OpenUnderstand\\benchmark\\testing_legacy_code\\src'
    info = initialize(abspath)
    print("***(AVAILABLE PACKAGES)***")
    for package in info[0]:
        print(package)
    print("***(AVAILABLE PACKAGE CLASSES)***")
    for package in info[1].keys():
        print("***(PACKAGE = {name})***".format(name=package))
        for package_class in info[1][package]:
            print(package_class)
    print("***(AVAILABLE CLASS METHODS)***")
    for class_long_name in info[2].keys():
        print("***(CLASS = {name})***".format(name=class_long_name))
        for method in info[2][class_long_name]:
            print(method)

    print("#####################################################")
    input()
    call_info = extract_data_from_all_files(info, abspath)
    for filename in call_info.keys():
        print("***(FILE NAME = {name})***".format(name=filename))
        print("***(NORMAL CALL)***")
        for method_key in call_info[filename][0].keys():
            print("method_key", method_key)
            for call in call_info[filename][0][method_key]:
                for spec in call.keys():
                    print(spec, ":", call[spec])
                print("--------------------")

        print("***(NON DYNAMIC CALL)***")
        for method_key in call_info[filename][1].keys():
            print("method_key", method_key)
            for call in call_info[filename][1][method_key]:
                for spec in call.keys():
                    print(spec, ":", call[spec])
                print("--------------------")
