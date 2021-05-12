import re  # regular expressions

import antlr4
from antlr4.Token import CommonToken
import antlr4.tree
from antlr4.CommonTokenStream import CommonTokenStream

from gen.java.JavaParser import JavaParser
from gen.java.JavaParserListener import JavaParserListener


class Program:
    def __init__(self):
        self.packages = {}

    def __str__(self):
        return str(self.packages)


class Package:
    def __init__(self):
        self.name = None
        self.classes = {}
        self.package_ctx = None

    def __str__(self):
        return str(self.name) + " " + str(self.classes)


class TokensInfo:
    """Note that start and stop are inclusive."""

    def __init__(self, parser_context=None):
        if parser_context is not None:
            self.token_stream: CommonTokenStream = parser_context.parser.getTokenStream()
            self.start: int = parser_context.start.tokenIndex
            self.stop: int = parser_context.stop.tokenIndex
        else:
            self.token_stream: CommonTokenStream = None
            self.start: int = None
            self.stop: int = None

    def get_token_index(self, tokens: list, start: int, stop: int):

        return tokens[start:stop]


class FileInfo:
    def __init__(self, filename: str = None, package_name: str = None):
        self.filename: str = filename
        self.package_name: str = package_name
        self.all_imports = []
        self.package_imports = []
        self.class_imports = []

    def has_imported_class(self, package_name: str, class_name: str) -> bool:
        if self.package_name == package_name:
            return True
        return (
                any(lambda x: x.package_name == package_name for package_import in self.package_imports)
                or any(lambda x: x.package_name == package_name and x.class_name == class_name for class_import in
                       self.class_imports)
        )

    def has_imported_package(self, package_name: str):
        if self.package_name == package_name:
            return True
        return (
            any(lambda x: x.package_name == package_name for package_import in self.package_imports)
        )


class SingleFileElement:
    """The base class for those elements that are extracted from a single file"""

    def __init__(self, parser_context, filename: str = None, _file_info: FileInfo = None):
        self.parser_context = parser_context
        self.filename = filename
        self.file_info = _file_info

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

    def get_file_position_range(self) -> tuple:
        return (
            self.get_first_symbol().start,
            self.get_last_symbol().stop
        )

    def get_text_from_file(self, filename=None) -> str:
        if filename is None:
            filename = self.filename
        if filename is None:
            return None
        file = open(filename, 'r')
        text = file.read()
        file.close()

        return text[self.get_first_symbol().start:self.get_last_symbol().stop + 1]


class ClassImport(SingleFileElement):
    """import package_name.class_name;"""

    def __init__(self,
                 package_name: str = None,
                 class_name: str = None,
                 parser_context: JavaParser.ImportDeclarationContext = None,
                 filename: str = None,
                 file_info: FileInfo = None):
        self.package_name = package_name
        self.class_name = class_name
        self.parser_context = parser_context
        self.filename = filename
        self.file_info = file_info

    def __str__(self):
        return "import " + str(self.package_name) + '.' + str(self.class_name)


class PackageImport(SingleFileElement):
    """import package_name.*;"""

    def __init__(self,
                 package_name: str = None,
                 parser_context: JavaParser.ImportDeclarationContext = None,
                 filename: str = None,
                 file_info: FileInfo = None):
        self.package_name = package_name
        self.parser_context = parser_context
        self.filename = filename
        self.file_info = file_info

    def __str__(self):
        return "import " + str(self.package_name) + ".*"


class Class(SingleFileElement):
    def __init__(self,
                 name: str = None,
                 super_class_name: str = None,
                 package_name: str = None,
                 parser_context: JavaParser.ClassDeclarationContext = None,
                 filename: str = None,
                 file_info: FileInfo = None):
        self.modifiers = []
        self.modifiers_parser_contexts = []
        self.name = name
        self.superclass_name = None
        self.superinterface_names = []
        self.fields = {}
        self.methods = {}
        self.package_name = package_name
        self.parser_context = parser_context
        self.filename = filename
        self.file_info = file_info
        self.body_context = None

    def find_methods_with_name(self, name: str) -> list:
        result = []
        for mk in self.methods:
            m = self.methods[mk]
            if m.name == name:
                result.append(m)
        return result

    def __str__(self):
        return str(self.modifiers) + " " + str(self.name) \
               + ((" extends " + str(self.superclass_name)) if self.superclass_name is not None else "") \
               + ((" implements " + str(self.superinterface_names)) if len(self.superinterface_names) > 0 else "") \
               + " " + str(self.fields) \
               + " " + str(self.methods)


class Field(SingleFileElement):
    def __init__(self,
                 datatype: str = None,
                 name: str = None,
                 initializer: str = None,
                 package_name: str = None,
                 class_name: str = None,
                 parser_context: JavaParser.FieldDeclarationContext = None,
                 filename: str = None,
                 file_info: FileInfo = None):
        self.modifiers = []
        self.modifiers_parser_contexts = []
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
        self.file_info = file_info

    def __str__(self):
        return str(self.modifiers) + " " + str(self.datatype) + " " + str(self.name)


class Method(SingleFileElement):
    def __init__(self,
                 returntype: str = None,
                 name: str = None,
                 body_text: str = None,
                 package_name: str = None,
                 class_name: str = None,
                 parser_context=None,
                 filename: str = None,
                 file_info: FileInfo = None):
        self.modifiers = []
        self.modifiers_parser_contexts = []
        self.returntype = returntype
        self.name = name
        self.parameters = []
        self.body_text = body_text
        self.body_method_invocations = {}
        self.body_local_vars_and_expr_names = []  # Type: either LocalVariable, ExpressionName or MethodInvocation
        self.package_name = package_name
        self.class_name = class_name
        self.parser_context = parser_context
        self.filename = filename
        self.file_info = file_info
        self.formalparam_context = None
        self.body_method_invocations_without_typename = {}
        self.method_declaration_context = None
        self.is_constructor = False

    def __str__(self):
        return str(self.modifiers) + " " + str(self.returntype) + " " + str(self.name) \
               + str(tuple(self.parameters))


class LocalVariable:
    def __init__(self, datatype: str = None, identifier: str = None,
                 parser_context: JavaParser.LocalVariableDeclarationContext = None):
        self.datatype = datatype
        self.identifier = identifier
        self.parser_context = parser_context


class ExpressionName:
    def __init__(self, dot_separated_identifiers: list):
        self.dot_separated_identifiers = dot_separated_identifiers


class MethodInvocation:
    def __init__(self, dot_separated_identifiers: list, parser_context: JavaParser.ExpressionContext = None):
        self.dot_separated_identifiers = dot_separated_identifiers
        self.parser_context = parser_context


class UtilsListener(JavaParserListener):

    def __init__(self, filename):
        self.package = Package()

        self.last_modifiers = []
        self.last_modifiers_contexts = []

        self.current_class_identifier = None
        self.current_class_identifier_temp = None
        self.nest_count = 0

        self.current_method_identifier = None
        self.current_method = None

        self.current_local_var_type = None
        self.current_local_var_ctx = None

        self.current_field_decl = None
        self.current_field_ids = None
        self.current_field_dims = None
        self.current_field_inits = None
        self.current_field_var_ctxs = None

        self.filename = filename
        self.file_info = FileInfo(filename=filename)

        self.field_enter_count = 0

    def enterPackageDeclaration(self, ctx: JavaParser.PackageDeclarationContext):
        self.package.name = ctx.qualifiedName().getText()
        self.file_info.package_name = self.package.name
        self.package.package_ctx = ctx;

    def enterImportDeclaration(self, ctx: JavaParser.ImportDeclarationContext):
        if ctx.STATIC() is None:
            name: str = ctx.qualifiedName().getText()
            if ctx.getText().endswith(".*;"):  # Package import
                p = name
                package_import = PackageImport(
                    package_name=p,
                    parser_context=ctx,
                    filename=self.filename,
                    file_info=self.file_info
                )
                self.file_info.all_imports.append(package_import)
                self.file_info.package_imports.append(package_import)
            else:  # Class import
                p = None
                dot_i = name.rfind('.')
                if dot_i != -1:
                    p = name[:dot_i]
                    c = name[dot_i + 1:]
                else:
                    c = name
                class_import = ClassImport(
                    package_name=p,
                    class_name=c,
                    parser_context=ctx,
                    filename=self.filename,
                    file_info=self.file_info
                )
                self.file_info.all_imports.append(class_import)
                self.file_info.class_imports.append(class_import)

    def enterTypeDeclaration(self, ctx: JavaParser.TypeDeclarationContext):
        self.last_modifiers.clear()
        self.last_modifiers_contexts.clear()
        for modifier in ctx.getChildren(lambda x: type(x) == JavaParser.ClassOrInterfaceModifierContext):
            self.last_modifiers.append(modifier.getText())
            self.last_modifiers_contexts.append(modifier)

    def enterClassBodyDeclaration(self, ctx: JavaParser.ClassBodyDeclarationContext):
        self.last_modifiers.clear()
        self.last_modifiers_contexts.clear()
        for modifier in ctx.getChildren(lambda x: type(x) == JavaParser.ModifierContext):
            self.last_modifiers.append(modifier.getText())
            self.last_modifiers_contexts.append(modifier)

    def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        if self.current_class_identifier is None and self.nest_count == 0:
            self.current_class_identifier = ctx.IDENTIFIER().getText()
            self.current_class_ctx = ctx.IDENTIFIER()
            current_class = Class(
                package_name=self.package.name,
                parser_context=ctx,
                filename=self.filename,
                file_info=self.file_info
            )
            current_class.modifiers = self.last_modifiers.copy()
            current_class.modifiers_parser_contexts = self.last_modifiers_contexts.copy()
            current_class.name = self.current_class_identifier
            if ctx.EXTENDS() is not None:
                current_class.superclass_name = ctx.typeType().getText()
            if ctx.IMPLEMENTS() is not None:
                for interface_type in ctx.typeList().getChildren(lambda x: type(x) == JavaParser.TypeTypeContext):
                    current_class.superinterface_names.append(interface_type.getText())
            self.package.classes[current_class.name] = current_class

        else:
            if self.nest_count == 0:
                self.current_class_identifier_temp = self.current_class_identifier
                self.current_class_identifier = None
            self.nest_count += 1

    def enterClassBody(self, ctx: JavaParser.ClassBodyContext):
        if self.current_class_identifier is not None:
            self.package.classes[self.current_class_identifier].body_context = ctx

    def exitClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        if self.nest_count > 0:
            self.nest_count -= 1
            if self.nest_count == 0:
                self.current_class_identifier = self.current_class_identifier_temp
                self.current_class_identifier_temp = None
        elif self.current_class_identifier is not None:
            self.current_class_identifier = None

    def enterFormalParameterList(self, ctx: JavaParser.FormalParameterListContext):
        if self.current_method is not None:
            self.current_method.formalparam_context = ctx

    def enterMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        if self.current_class_identifier is not None:
            # method_header = ctx.methodHeader()
            self.current_method_identifier = ctx.IDENTIFIER().getText()

            method = Method(
                package_name=self.package.name,
                class_name=self.current_class_identifier,
                parser_context=ctx.parentCtx.parentCtx,
                filename=self.filename,
                file_info=self.file_info
            )
            method.modifiers = self.last_modifiers.copy()
            method.modifiers_parser_contexts = self.last_modifiers_contexts.copy()
            method.returntype = ctx.typeTypeOrVoid().getText()
            method.name = self.current_method_identifier
            method.is_constructor = False

            # This is done on exit to collect params too, to support overloading.
            # self.package.classes[self.current_class_identifier].methods[method.name] = method
            self.current_method = method

    def enterFormalParameters(self, ctx: JavaParser.FormalParametersContext):
        if self.current_method is not None:
            self.current_method.method_declaration_context = ctx

    def enterFormalParameter(self, ctx: JavaParser.FormalParameterContext):
        if self.current_method is not None:
            self.current_method.parameters.append(
                (ctx.typeType().getText(), ctx.variableDeclaratorId().IDENTIFIER().getText())
            )

    def enterMethodBody(self, ctx: JavaParser.MethodBodyContext):
        if self.current_method is not None:
            self.current_method.body_text = ctx.getText()
            pass

    def general_exit_method_decl(self):
        if self.current_class_identifier is not None:
            if self.current_method is not None:
                method = self.current_method
                method_key = ("" if method.name is None else method.name) + '('
                is_first = True
                for param in method.parameters:
                    if not is_first:
                        method_key += ','
                    is_first = False
                    method_key += param[0]  # the type
                method_key += ')'
                self.package.classes[self.current_class_identifier].methods[method_key] = method
        self.current_method_identifier = None
        self.current_method = None

    def exitMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        self.general_exit_method_decl()

    def enterConstructorDeclaration(self, ctx: JavaParser.ConstructorDeclarationContext):
        if self.current_class_identifier is not None:
            self.current_method_identifier = ctx.IDENTIFIER().getText()

            method = Method(
                package_name=self.package.name,
                class_name=self.current_class_identifier,
                parser_context=ctx.parentCtx.parentCtx,
                filename=self.filename,
                file_info=self.file_info
            )
            method.modifiers = self.last_modifiers.copy()
            method.modifiers_parser_contexts = self.last_modifiers_contexts.copy()
            method.returntype = None
            method.name = None  # self.current_method_identifier
            method.body_text = ctx.constructorBody.getText()
            method.is_constructor = True

            # This is done on exit to collect params too, to support overloading.
            # self.package.classes[self.current_class_identifier].methods[method.name] = method
            self.current_method = method

    def exitConstructorDeclaration(self, ctx: JavaParser.ConstructorDeclarationContext):
        self.general_exit_method_decl()

    def enterMethodCall(self, ctx: JavaParser.MethodCallContext):
        if self.current_method is not None:
            if ctx.parentCtx.IDENTIFIER() != None:
                if ctx.parentCtx.IDENTIFIER() not in self.current_method.body_method_invocations:
                    self.current_method.body_method_invocations[ctx.parentCtx.IDENTIFIER()] = [
                        ctx.IDENTIFIER().getText()]
                else:
                    self.current_method.body_method_invocations[ctx.parentCtx.IDENTIFIER()].append(
                        ctx.IDENTIFIER().getText())
            else:
                a = len(ctx.parentCtx.children)
            if a == 1:
                if ctx.IDENTIFIER() != None:
                    if self.current_class_ctx not in self.current_method.body_method_invocations_without_typename:
                        self.current_method.body_method_invocations_without_typename[self.current_class_ctx] = [ctx]
                    else:
                        self.current_method.body_method_invocations_without_typename[self.current_class_ctx].append(
                            ctx)
            # MethodInvocation
            txt = ctx.getText()
            ids = txt[:txt.find('(')].split('.')
            self.current_method.body_local_vars_and_expr_names.append(
                MethodInvocation(ids, ctx)
            )

    def enterExpression(self, ctx: JavaParser.ExpressionContext):
        if self.current_method is not None:
            if ctx.methodCall() is not None:
                txt = ctx.getText()
                ids = txt[:txt.find('(')].split('.')
                self.current_method.body_local_vars_and_expr_names.append(
                    MethodInvocation(ids, ctx)
                )
            else:
                names = ctx.getText().split('.')
                should_add = True
                for name in names:
                    if not re.match("^[A-Za-z0-9_]*$", name):
                        should_add = False
                if should_add:
                    self.current_method.body_local_vars_and_expr_names.append(ExpressionName(names))

    def enterLocalVariableDeclaration(self, ctx: JavaParser.LocalVariableDeclarationContext):
        if self.current_method is not None:
            self.current_local_var_type = ctx.typeType().getText()
            self.current_local_var_ctx = ctx
            # The rest in: enterVariableDeclarator

    def exitLocalVariableDeclaration(self, ctx: JavaParser.LocalVariableDeclarationContext):
        self.current_local_var_type = None

    def enterFieldDeclaration(self, ctx: JavaParser.FieldDeclarationContext):
        self.field_enter_count += 1
        if self.current_class_identifier is not None and self.field_enter_count == 1:
            modifiers = self.last_modifiers.copy()
            modifiers_contexts = self.last_modifiers_contexts.copy()
            datatype = ctx.typeType().getText()
            self.current_field_decl = (modifiers, datatype, ctx, modifiers_contexts)
            self.current_field_ids = []
            self.current_field_dims = []
            self.current_field_inits = []
            self.current_field_var_ctxs = []

    def enterVariableDeclarator(self, ctx: JavaParser.VariableDeclaratorContext):
        dims = ""
        v_id: str = ctx.variableDeclaratorId().getText()
        dims_i = v_id.find('[')
        if dims_i != -1:
            dims = v_id[dims_i:]
        if self.current_field_decl is not None:
            self.current_field_ids.append(ctx.variableDeclaratorId().IDENTIFIER().getText())
            self.current_field_dims.append(dims)
            init = None
            init_ctx = ctx.variableInitializer()
            if init_ctx is not None:
                init = init_ctx.getText()
            self.current_field_inits.append(init)
            self.current_field_var_ctxs.append(ctx)
        if self.current_local_var_type is not None:
            if self.current_method is not None:
                self.current_method.body_local_vars_and_expr_names.append(
                    LocalVariable(
                        self.current_local_var_type + dims,
                        ctx.variableDeclaratorId().IDENTIFIER().getText(),
                        self.current_local_var_ctx
                    )
                )

    def exitFieldDeclaration(self, ctx: JavaParser.FieldDeclarationContext):
        self.field_enter_count -= 1
        if self.current_class_identifier is not None and self.field_enter_count == 0:
            for i in range(len(self.current_field_ids)):
                field_id = self.current_field_ids[i]
                dims = self.current_field_dims[i]
                field_init = self.current_field_inits[i]
                var_ctx = self.current_field_var_ctxs[i]
                field = Field(
                    package_name=self.package.name,
                    class_name=self.current_class_identifier,
                    parser_context=self.current_field_decl[2],
                    filename=self.filename,
                    file_info=self.file_info
                )
                field.modifiers = self.current_field_decl[0]
                field.modifiers_parser_contexts = self.current_field_decl[3]
                field.datatype = self.current_field_decl[1] + dims
                field.name = field_id
                field.initializer = field_init
                field.neighbor_names = [x for x in self.current_field_ids if x != field_id]
                field.all_variable_declarator_contexts = self.current_field_var_ctxs
                field.index_in_variable_declarators = i
                self.package.classes[self.current_class_identifier].fields[field.name] = field
            self.current_field_decl = None
