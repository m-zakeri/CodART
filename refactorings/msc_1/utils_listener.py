import antlr4
from antlr4.Token import CommonToken
import antlr4.tree

from antlr4_java9.Java9Parser import Java9Parser, CommonTokenStream
from antlr4_java9.Java9Listener import Java9Listener

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
        return self.parser_context.parser.getTokenStream()

    def get_tokens_info(self) -> TokensInfo:
        return TokensInfo(
            self.parser_context
        )

    def get_first_symbol(self) -> CommonToken:
        first_terminal = self.parser_context
        while not isinstance(first_terminal, antlr4.tree.Tree.TerminalNode):
            first_terminal = first_terminal.getChild(0)
        return first_terminal.getSymbol()

    def get_last_symbol(self) -> CommonToken:
        last_terminal = self.parser_context
        while not isinstance(last_terminal, antlr4.tree.Tree.TerminalNode):
            last_terminal = last_terminal.getChild(last_terminal.getChildCount() - 1)
        return last_terminal.getSymbol()

    def get_file_position_range(self) -> str:
        return (
            self.get_first_symbol().start,
            self.get_last_symbol().stop
        )

    def get_text_from_file(self, filename = None) -> str:
        if filename is None:
            filename = self.filename
        if filename is None:
            return None
        file = open(filename, 'r')
        text = file.read()
        file.close()
        return text[self.get_first_symbol().start:self.get_last_symbol().stop + 1]

class Class(SingleFileElement):
    def __init__(self,
                 name: str = None,
                 super_class_name: str = None,
                 package_name: str = None,
                 parser_context: Java9Parser.NormalClassDeclarationContext = None,
                 filename: str = None):
        self.modifiers = []
        self.name = name
        self.superclass_name = None
        self.superinterface_names = []
        self.fields = {}
        self.methods = {}
        self.package_name = package_name
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
                 initializer: str = None,
                 package_name: str = None,
                 class_name: str = None,
                 parser_context: Java9Parser.NormalClassDeclarationContext = None,
                 filename: str = None):
        self.modifiers = []
        self.datatype = datatype
        self.name = name
        self.initializer = initializer
        self.neighbor_names = []
        self.all_variable_declarator_contexts = []
        self.index_in_variable_declarators: int = None
        self.package_name = package_name
        self.class_name = class_name
        self.parser_context = parser_context
        self.filename = filename
    def __str__(self):
        return str(self.modifiers) +  " " + str(self.datatype) + " " + str(self.name)

class Method(SingleFileElement):
    def __init__(self,
                 returntype: str = None,
                 name: str = None,
                 body_text: str = None,
                 package_name: str = None,
                 class_name: str = None,
                 parser_context: Java9Parser.NormalClassDeclarationContext = None,
                 filename: str = None):
        self.modifiers = []
        self.returntype = None
        self.name = None
        self.parameters = []
        self.body_text = None
        self.body_method_invocations = []
        self.package_name = package_name
        self.class_name = class_name
        self.parser_context = parser_context
        self.filename = filename
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
        self.current_field_dims = None
        self.current_field_inits = None
        self.current_field_var_ctxs = None

        self.filename = filename

    def enterPackageDeclaration(self, ctx:Java9Parser.PackageDeclarationContext):
        self.package.name = ctx.packageName().getText()

    def enterNormalClassDeclaration(self, ctx:Java9Parser.NormalClassDeclarationContext):
        if self.current_class_identifier is None and self.nest_count == 0:
            self.current_class_identifier = ctx.identifier().getText()

            current_class = Class(
                package_name=self.package.name,
                parser_context=ctx,
                filename=self.filename
            )
            for modifier in ctx.getChildren(lambda x: type(x) == Java9Parser.ClassModifierContext):
                current_class.modifiers.append(modifier.getText())
            current_class.name = self.current_class_identifier
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

            method = Method(
                package_name=self.package.name,
                class_name=self.current_class_identifier,
                parser_context=ctx,
                filename=self.filename
            )
            for modifier in ctx.getChildren(lambda x: type(x) == Java9Parser.MethodModifierContext):
                method.modifiers.append(modifier.getText())
            method.returntype = method_header.result().getText()
            method.name = self.current_method_identifier

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

    def exitMethodDeclaration(self, ctx:Java9Parser.MethodDeclarationContext):
        self.current_method_identifier = None
        self.current_method = None

    def enterMethodInvocation(self, ctx:Java9Parser.MethodInvocationContext):
        if self.current_method is not None:
            for typename in ctx.getChildren(lambda x: type(x) == Java9Parser.TypeNameContext):
                self.current_method.body_method_invocations.append(typename)


    def enterFieldDeclaration(self, ctx:Java9Parser.FieldDeclarationContext):
        if self.current_class_identifier is not None:
            modifiers = []
            for modifier in ctx.getChildren(lambda x: type(x) == Java9Parser.FieldModifierContext):
                modifiers.append(modifier.getText())
            datatype = ctx.unannType().getText()
            self.current_field_decl = (modifiers, datatype, ctx)
            self.current_field_ids = []
            self.current_field_dims = []
            self.current_field_inits = []
            self.current_field_var_ctxs = []

    def enterVariableDeclarator(self, ctx:Java9Parser.VariableDeclaratorContext):
        if self.current_field_decl is not None:
            self.current_field_ids.append(ctx.variableDeclaratorId().identifier().getText())
            dims = ""
            dims_ctx = ctx.variableDeclaratorId().dims()
            if dims_ctx is not None:
                dims = dims_ctx.getText()
            self.current_field_dims.append(dims)
            init = None
            init_ctx = ctx.variableInitializer()
            if init_ctx is not None:
                init = init_ctx.getText()
            self.current_field_inits.append(init)
            self.current_field_var_ctxs.append(ctx)

    def exitFieldDeclaration(self, ctx:Java9Parser.FieldDeclarationContext):
        if self.current_class_identifier is not None:
            for i in range(len(self.current_field_ids)):
                field_id = self.current_field_ids[i]
                dims = self.current_field_dims[i]
                field_init = self.current_field_inits[i]
                var_ctx = self.current_field_var_ctxs[i]
                field = Field(
                    package_name=self.package.name,
                    class_name=self.current_class_identifier,
                    parser_context=self.current_field_decl[2],
                    filename=self.filename
                )
                field.modifiers = self.current_field_decl[0]
                field.datatype = self.current_field_decl[1] + dims
                field.name = field_id
                field.initializer = field_init
                field.neighbor_names = [ x for x in self.current_field_ids if x != field_id ]
                field.all_variable_declarator_contexts = self.current_field_var_ctxs
                field.index_in_variable_declarators = i
                self.package.classes[self.current_class_identifier].fields[field.name] = field
            self.current_field_decl = None
