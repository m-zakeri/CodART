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

class TokensInfo:
    """Note that begin is inclusive and end is exclusive."""

    def __init__(self, token_stream: CommonTokenStream, begin: int, end: int):
        self.token_stream = token_stream
        self.begin = begin
        self.end = end

class SingleFileElement:
    """The base class for those elements that are extracted from a single file"""

    def __init__(self, parser_context):
        self.parser_context = parser_context

    def get_tokens_info(self) -> TokensInfo:
        return TokensInfo(
            self.parser_context.parser.getTokenStream(),
            self.parser_context.start.tokenIndex,
            self.parser_context.stop.tokenIndex + 1
        )

class Class(SingleFileElement):
    def __init__(self,
                 name: str = None,
                 parser_context: Java9Parser.NormalClassDeclarationContext = None):
        self.modifiers = []
        self.name = name
        self.fields = {}
        self.methods = {}
        self.parser_context = parser_context
    def __str__(self):
        return str(self.modifiers) +  " " + str(self.name) + " " + str(self.fields) \
            + " " + str(self.methods)

class Field(SingleFileElement):
    def __init__(self,
                 datatype: str = None,
                 name: str = None,
                 parser_context: Java9Parser.NormalClassDeclarationContext = None):
        self.modifiers = []
        self.datatype = datatype
        self.name = name
        self.parser_context = parser_context
    def __str__(self):
        return str(self.modifiers) +  " " + str(self.datatype) + " " + str(self.name)

class Method(SingleFileElement):
    def __init__(self,
                 returntype: str = None,
                 name: str = None,
                 body_text: str = None,
                 parser_context: Java9Parser.NormalClassDeclarationContext = None):
        self.modifiers = []
        self.returntype = None
        self.name = None
        self.parameters = []
        self.body_text = None
        self.body_content = [] # TODO Design
        self.parser_context = parser_context
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
        self.package.name = ctx.packageName().getText()

    def enterNormalClassDeclaration(self, ctx:Java9Parser.NormalClassDeclarationContext):
        if self.current_class_identifier is None and self.nest_count == 0:
            self.current_class_identifier = ctx.identifier().getText()

            current_class = Class()
            for modifier in ctx.getChildren(lambda x: type(x) == Java9Parser.ClassModifierContext):
                current_class.modifiers.append(modifier.getText())
            current_class.name = self.current_class_identifier
            current_class.parser_context = ctx
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
            method.parser_context = ctx

            self.package.classes[self.current_class_identifier].methods[method.name] = method

    def enterFormalParameter(self, ctx:Java9Parser.FormalParameterContext):
        if self.current_class_identifier is not None and self.current_method_identifier is not None:
            method = self.package.classes[self.current_class_identifier].methods[self.current_method_identifier]
            method.parameters.append(
                (ctx.unannType().getText(), ctx.variableDeclaratorId().identifier().getText())
            )

    def enterMethodBody(self, ctx:Java9Parser.MethodBodyContext):
        if self.current_class_identifier is not None and self.current_method_identifier is not None:
            # TODO
            pass

    def exitMethodDeclaration(self, ctx:Java9Parser.MethodDeclarationContext):
        self.current_method_identifier = None
