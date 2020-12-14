from antlr4_java9.Java9Parser import *
from antlr4_java9.Java9Listener import *

class Program:
    def __init__(self):
        self.packages = {}
    def __str__(self):
        return str(self.packages)

class Package:
    def __init__(self):
        self.name = None
        self.classes = {}
    def __str__(self):
        return str(self.name) + " " + str(self.classes)

class Class:
    def __init__(self):
        self.modifiers = []
        self.name = None
        self.fields = {}
        self.methods = {}
    def __str__(self):
        return str(self.modifiers) +  " " + str(self.name) + " " + str(self.fields) \
            + " " + str(self.methods)

class Field:
    def __init__(self):
        self.modifiers = []
        self.datatype = None
        self.name = None
    def __str__(self):
        return str(self.modifiers) +  " " + str(self.datatype) + " " + str(self.name)

class Method:
    def __init__(self):
        self.modifiers = []
        self.returntype = None
        self.name = None
        self.parameters = []
        self.body_text = None
        self.body_content = [] # TODO Design
    def __str__(self):
        return str(self.modifiers) +  " " + str(self.returntype) + " " + str(self.name) \
            + str(tuple(self.parameters))

class UtilsListener(Java9Listener):

    def __init__(self):
        self.package = Package()

        self.current_class_identifier = None
        self.current_class_identifier_temp = None
        self.nest_count = 0

        self.current_method_identifier = None

    def enterPackageDeclaration(self, ctx:Java9Parser.PackageDeclarationContext):
        print(ctx.packageName().getText())
        self.package.name = ctx.packageName().getText()

    def enterNormalClassDeclaration(self, ctx:Java9Parser.NormalClassDeclarationContext):
        print(ctx.identifier().getText())
        if self.current_class_identifier is None and self.nest_count == 0:
            self.current_class_identifier = ctx.identifier().getText()

            current_class = Class()
            for modifier in ctx.getChildren(lambda x: type(x) == Java9Parser.ClassModifierContext):
                current_class.modifiers.append(modifier.getText())
            current_class.name = self.current_class_identifier
            self.package.classes[current_class.name] = current_class

        else:
            if self.nest_count == 0:
                self.current_class_identifier_temp = self.current_class_identifier
                self.current_class_identifier = None
            self.nest_count += 1

    def exitNormalClassDeclaration(self, ctx:Java9Parser.NormalClassDeclarationContext):
        if self.nest_count > 0:
            self.nest_count -= 1
            if self.nest_count == 0:
                self.current_class_identifier = self.current_class_identifier_temp
                self.current_class_identifier_temp = None
        elif self.current_class_identifier is not None:
                self.current_class_identifier = None

    def enterMethodDeclaration(self, ctx:Java9Parser.MethodDeclarationContext):
        if self.current_class_identifier is not None:
            method_header = ctx.methodHeader()
            self.current_method_identifier = method_header.methodDeclarator().identifier().getText()

            method = Method()
            for modifier in ctx.getChildren(lambda x: type(x) == Java9Parser.MethodModifierContext):
                method.modifiers.append(modifier.getText())
            method.returntype = method_header.result().getText()
            method.name = self.current_method_identifier

            self.package.classes[self.current_class_identifier].methods[method.name] = method

    def enterFormalParameter(self, ctx:Java9Parser.FormalParameterContext):
        # TODO
        pass

    def enterMethodBody(self, ctx:Java9Parser.MethodBodyContext):
        # TODO
        pass

    def exitMethodDeclaration(self, ctx:Java9Parser.MethodDeclarationContext):
        self.current_method_identifier = None
