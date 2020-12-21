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
    """Note that start and stop are inclusive."""

    def __init__(self, parser_context = None):
        if parser_context is not None:
            self.token_stream: CommonTokenStream = parser_context.parser.getTokenStream()
            self.start: int = parser_context.start.tokenIndex
            self.stop: int = parser_context.stop.tokenIndex
        else:
            self.token_stream: CommonTokenStream = None
            self.start: int = None
            self.stop: int = None

class SingleFileElement:
    """The base class for those elements that are extracted from a single file"""

    def __init__(self, parser_context, filename: str = None):
        self.parser_context = parser_context
        self.filename = filename

    def get_token_stream(self) -> CommonTokenStream:
        self.parser_context.parser.getTokenStream()

    def get_tokens_info(self) -> TokensInfo:
        return TokensInfo(
            self.parser_context
        )

class Class(SingleFileElement):
    def __init__(self,
                 name: str = None,
                 super_class_name: str = None,
                 parser_context: Java9Parser.NormalClassDeclarationContext = None,
                 filename: str = None):
        self.modifiers = []
        self.name = name
        self.superclass_name = None
        self.superinterface_names = []
        self.fields = {}
        self.methods = {}
        self.parser_context = parser_context
        self.filename = filename
    def __str__(self):
        return str(self.modifiers) +  " " + str(self.name) \
            + ((" extends " + str(self.superclass_name)) if self.superclass_name is not None else "") \
            + ((" implements " + str(self.superinterface_names)) if len(self.superinterface_names) > 0 else "") \
            + " " + str(self.fields) \
            + " " + str(self.methods)

# TODO Add Interface

class Field(SingleFileElement):
    def __init__(self,
                 datatype: str = None,
                 name: str = None,
                 parser_context: Java9Parser.NormalClassDeclarationContext = None,
                 filename: str = None):
        self.modifiers = []
        self.datatype = datatype
        self.name = name
        self.neighbor_names = []
        self.parser_context = parser_context
        self.filename = filename
    def __str__(self):
        return str(self.modifiers) +  " " + str(self.datatype) + " " + str(self.name)

class Method(SingleFileElement):
    def __init__(self,
                 returntype: str = None,
                 name: str = None,
                 body_text: str = None,
                 parser_context: Java9Parser.NormalClassDeclarationContext = None,
                 filename: str = None):
        self.modifiers = []
        self.returntype = None
        self.name = None
        self.parameters = []
        self.body_text = None
        self.body_expression_names = []
        self.parser_context = parser_context
        self.filename = filename
        self.method_invocations = []
    def __str__(self):
        return str(self.modifiers) +  " " + str(self.returntype) + " " + str(self.name) \
            + str(tuple(self.parameters))

class ExpressionName(SingleFileElement):
    def __init__(self,
                 text: str = None,
                 parser_context: Java9Parser.NormalClassDeclarationContext = None,
                 filename: str = None):
        self.text = text
        self.parser_context = parser_context
        self.filename = filename
    def __str__(self):
        return str(self.text)

class UtilsListener(Java9Listener):

    def __init__(self, filename):
        self.package = Package()

        self.current_class_identifier = None
        self.current_class_identifier_temp = None
        self.nest_count = 0

        self.current_method_identifier = None
        self.current_method = None

        self.current_field_decl = None
        self.current_field_ids = None

        self.filename = filename

    def enterPackageDeclaration(self, ctx:Java9Parser.PackageDeclarationContext):
        self.package.name = ctx.packageName().getText()

    def enterNormalClassDeclaration(self, ctx:Java9Parser.NormalClassDeclarationContext):
        if self.current_class_identifier is None and self.nest_count == 0:
            self.current_class_identifier = ctx.identifier().getText()

            current_class = Class(filename=self.filename)
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

    def enterSuperclass(self, ctx:Java9Parser.SuperclassContext):
        if self.current_class_identifier is not None:
            self.package.classes[self.current_class_identifier].superclass_name = ctx.classType().getText()

    def enterSuperinterfaces(self, ctx:Java9Parser.SuperinterfacesContext):
        if self.current_class_identifier is not None:
            _class = self.package.classes[self.current_class_identifier]
            for interface_type in ctx.interfaceTypeList().getChildren(lambda x: type(x) == Java9Parser.InterfaceTypeContext):
                _class.superinterface_names.append(interface_type.getText())

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

            method = Method(filename=self.filename)
            for modifier in ctx.getChildren(lambda x: type(x) == Java9Parser.MethodModifierContext):
                method.modifiers.append(modifier.getText())
            method.returntype = method_header.result().getText()
            method.name = self.current_method_identifier
            method.parser_context = ctx

            self.package.classes[self.current_class_identifier].methods[method.name] = method
            self.current_method = method


    def enterFormalParameter(self, ctx:Java9Parser.FormalParameterContext):
        if self.current_method is not None:
            self.current_method.parameters.append(
                (ctx.unannType().getText(), ctx.variableDeclaratorId().identifier().getText())
            )

    def enterMethodBody(self, ctx:Java9Parser.MethodBodyContext):
        if self.current_method is not None:
            self.current_method.body_text = ctx.getText()
            pass

    def enterExpressionName(self, ctx:Java9Parser.ExpressionNameContext):
        if self.current_method is not None:
            self.current_method.body_expression_names.append(
                ExpressionName(text=ctx.getText(), parser_context=ctx, filename=self.filename)
            )

    def exitMethodDeclaration(self, ctx:Java9Parser.MethodDeclarationContext):
        self.current_method_identifier = None
        self.current_method = None

    def enterMethodInvocation(self, ctx:Java9Parser.MethodInvocationContext):
        if self.current_method is not None:
            for typename in ctx.getChildren(lambda x: type(x) == Java9Parser.TypeNameContext):
                self.current_method.method_invocations.append(typename.getText())


    def enterFieldDeclaration(self, ctx:Java9Parser.FieldDeclarationContext):
        if self.current_class_identifier is not None:
            modifiers = []
            for modifier in ctx.getChildren(lambda x: type(x) == Java9Parser.FieldModifierContext):
                modifiers.append(modifier.getText())
            datatype = ctx.unannType().getText()
            self.current_field_decl = (modifiers, datatype, ctx)
            self.current_field_ids = []

    def enterVariableDeclarator(self, ctx:Java9Parser.VariableDeclaratorContext):
        if self.current_field_decl is not None:
            self.current_field_ids.append(ctx.variableDeclaratorId().identifier().getText())

    def exitFieldDeclaration(self, ctx:Java9Parser.FieldDeclarationContext):
        if self.current_class_identifier is not None:
            for field_id in self.current_field_ids:
                field = Field(
                    parser_context=self.current_field_decl[2],
                    filename=self.filename
                )
                field.modifiers = self.current_field_decl[0]
                field.datatype = self.current_field_decl[1]
                field.name = field_id
                field.neighbor_names = [ x for x in self.current_field_ids if x != field_id ]
                self.package.classes[self.current_class_identifier].fields[field.name] = field
            self.current_field_decl = None
