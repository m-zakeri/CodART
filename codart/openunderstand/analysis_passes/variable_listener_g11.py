"""This module is for create, Read of entities of type package."""

__author__ = "Navid Mousavizadeh, Amir Mohammad Sohrabi, Sara Younesi, Deniz Ahmadi"
__copyright__ = "Copyright 2022, The OpenUnderstand Project, Iran University of Science and technology"
__credits__ = [
    "Dr.Parsa",
    "Dr.Zakeri",
    "Mehdi Razavi",
    "Navid Mousavizadeh",
    "Amir Mohammad Sohrabi",
    "Sara Younesi",
    "Deniz Ahmadi",
]
__license__ = "GPL"
__version__ = "1.0.0"

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class VariableListener(JavaParserLabeledListener):
    """A listener class for detecting variables"""

    # def __init__(self, entity_manager_object):
    def __init__(self):
        # self.entity_manager = entity_manager_object
        self.package = ""
        self._class = ""
        self._method = ""
        self._interface = ""
        self.parent = ""
        self.type = None
        self.modifiers = []
        self.value = None
        self.var = []
        self.var_const = []

    # package
    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package = ctx.qualifiedName().getText()

    # class parent
    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self._class = self._class + ctx.IDENTIFIER().getText() + "."
        self.parent = ctx.IDENTIFIER().getText()
        interface_array = self._interface.split(".")
        if "" in interface_array:
            interface_array.remove("")
        if len(interface_array) > 0:
            self._class = ".".join(interface_array) + "." + self._class
        # print("------- self._class:", self._class)
        if len(self._class.split(".")) > 2:
            # print("---- len(self._class.split(.)):", len(self._class.split(".")))
            self.parent = self._class[:-1]

    # exit class parent
    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_array = self._class.split(".")
        if "" in class_array:
            class_array.remove("")
        self._class = ".".join(class_array[:-1])
        if len(class_array[:-1]) > 0:
            self._class = self._class + "."

    # method parent
    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self._method = self._method + ctx.IDENTIFIER().getText() + "."
        self.parent = self._class + self._method[:-1]
        # print("self.method:", self._method)
        # print("self.parent:", self.parent)

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        method_array = self._method.split(".")
        if "" in method_array:
            method_array.remove("")
        self._method = ".".join(method_array[:-1])
        if len(method_array[:-1]) > 0:
            self._method = self._method + "."

    # interface parent
    def enterInterfaceDeclaration(
        self, ctx: JavaParserLabeled.InterfaceDeclarationContext
    ):
        self._interface = self._interface + ctx.IDENTIFIER().getText() + "."
        class_array = self._class.split(".")
        if "" in class_array:
            class_array.remove("")
        # print(class_array)
        if len(class_array) > 0:
            self.parent = ".".join(class_array) + "." + self._interface[:-1]
        else:
            self.parent = self._interface[:-1]
        # print("self.parent:", self.parent)

    def exitInterfaceDeclaration(
        self, ctx: JavaParserLabeled.InterfaceDeclarationContext
    ):
        interface_array = self._interface.split(".")
        if "" in interface_array:
            interface_array.remove("")
        self._interface = ".".join(interface_array[:-1])
        if len(interface_array[:-1]) > 0:
            self._interface = self._interface + "."

    # interface modifiers
    def enterInterfaceBodyDeclaration(
        self, ctx: JavaParserLabeled.InterfaceBodyDeclarationContext
    ):
        self.modifiers = ctx.modifier()
        for i in range(len(self.modifiers)):
            self.modifiers[i] = self.modifiers[i].getText()

    # class modifiers
    def enterClassBodyDeclaration2(
        self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context
    ):
        self.modifiers = ctx.modifier()
        for i in range(len(self.modifiers)):
            self.modifiers[i] = self.modifiers[i].getText()

    # method modifiers and data type
    def enterLocalVariableDeclaration(
        self, ctx: JavaParserLabeled.LocalVariableDeclarationContext
    ):
        self.modifiers = ctx.variableModifier()
        self.type = ctx.typeType().getText()
        for i in range(len(self.modifiers)):
            self.modifiers[i] = self.modifiers[i].getText()
        self.modifiers.append("local")

    # interface variable type
    def enterConstDeclaration(self, ctx: JavaParserLabeled.ConstDeclarationContext):
        self.type = ctx.typeType().getText()

    #
    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        self.type = ctx.typeType().getText()

    # method parameters modifiers and data type
    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        self.modifiers = None
        self.type = ctx.typeType().getText()

    # value
    def enterVariableInitializer1(
        self, ctx: JavaParserLabeled.VariableInitializer1Context
    ):
        self.value = ctx.getText()

    # interface variable
    def enterConstantDeclarator(self, ctx: JavaParserLabeled.ConstantDeclaratorContext):
        res = {
            "name": ctx.IDENTIFIER().getText().lstrip("_"),
            "parent_longname": self.package + "." + self.parent,
            "type": self.type,
            "modifiers": self.modifiers,
            "value": self.value,
        }
        self.var_const.append(res)
        # self.entity_manager.get_or_create_variable_entity(res)
        # print(self.modifiers, self.package, self.parent, self.type, ctx.IDENTIFIER().getText())

    # variable
    def enterVariableDeclaratorId(
        self, ctx: JavaParserLabeled.VariableDeclaratorIdContext
    ):
        # print("--- self.package + '.' + self.parent:", self.package + '.' + self.parent)
        res = {
            "name": ctx.IDENTIFIER().getText().lstrip("_"),
            "parent_longname": self.package + "." + self.parent,
            "type": self.type,
            "modifiers": self.modifiers,
            "value": self.value,
        }
        self.var.append(res)
        # self.entity_manager.get_or_create_variable_entity(res)
        # print(self.modifiers, self.package, self.parent, self.type, ctx.IDENTIFIER().getText())
