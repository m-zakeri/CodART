import os
import re  # regular expressions
import antlr4
from antlr4 import FileStream
from antlr4.Token import CommonToken
import antlr4.tree
from antlr4.CommonTokenStream import CommonTokenStream
from gen.java.JavaParser import JavaParser
from gen.java.JavaParserListener import JavaParserListener

from antlr4 import FileStream, ParseTreeWalker
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from gen.java.JavaLexer import JavaLexer


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
    def __init__(self, dot_separated_identifiers: list, ctx: JavaParser.ExpressionContext):
        self.dot_separated_identifiers = dot_separated_identifiers
        self.parser_context = ctx


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
        self.package.package_ctx = ctx

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
                    self.current_method.body_local_vars_and_expr_names.append(ExpressionName(names, ctx))

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


class StaticFieldUsageListener(UtilsListener):
    def __init__(self, filename: str, field_name: str, source_class: str):
        super().__init__(filename)
        self.current_class_name = os.path.basename(filename).replace(".java", "")
        self.field_name = field_name
        self.source_class = source_class
        self.stack = []
        self.usages = []

    def enterExpression(self, ctx: JavaParser.ExpressionContext):
        text = ctx.getText()

        # if we reached expression this.field
        if text == f"this.{self.field_name}":
            self.usages.append(ctx)
            return

        # if we reached expression Source.field
        if text == f"{self.source_class}.{self.field_name}":
            self.usages.append(ctx)
            return

        if text != self.field_name:
            return

        # if we reached field and there is no local declaration with the same name as field
        if len(self.stack) == 0:
            self.usages.append(ctx)

        # self.state_machine.change_state(ctx, len(self.stack) > 0 and self.stack[-1] == self.field_name)
        # if self.state_machine.is_final():
        #     self.state_machine.reset()
        #     self.usages.append(ctx)

    def exitClassBody(self, ctx: JavaParser.ClassBodyContext):
        if self.current_class_name not in self.package.classes:
            print("wtf")
            return
        setattr(self.package.classes[self.current_class_name], "usages", self.usages)

    def enterBlock(self, ctx: JavaParser.BlockContext):
        super().enterBlock(ctx)

        if len(self.stack) != 0:
            self.stack.append(self.field_name)

    def exitBlock(self, ctx: JavaParser.BlockContext):
        super().exitBlock(ctx)
        try:
            self.stack.pop()
        except IndexError:
            pass

    def enterVariableDeclarator(self, ctx: JavaParser.VariableDeclaratorContext):
        super().enterVariableDeclarator(ctx)
        if type(ctx.parentCtx.parentCtx) is JavaParser.FieldDeclarationContext:
            return

        # if we're in a method and we have a parameter with
        # the same name as field, we shouldn't consider any
        # references to field a usage since it is referring
        # to the parameter
        var_name = ctx.variableDeclaratorId().IDENTIFIER().getText()
        if self.current_method is not None:
            for _, param in self.current_method.parameters:
                if param == self.field_name:
                    self.stack.append(var_name)
                    return

        if var_name == self.field_name:
            self.stack.append(var_name)


class FieldUsageListener(UtilsListener):
    """
    FieldUsageListener finds all the usage of
    an specified field f, from a class c in
    package pkg.
    """

    def __init__(self, filename: str, source_class: str, source_package: str, target_class: str, target_package: str,
                 field_name: str, field_candidates: set, field_tobe_moved: Field):
        super().__init__(filename)
        self.source_class = source_class
        self.source_package = source_package
        self.target_class = target_class
        self.target_package = target_package
        self.field_name = field_name
        self.has_imported_source = False
        self.has_imported_target = False
        self.usages = []
        # current class name is the public class in each file.
        self.current_class_name = ""
        self.field_candidates = field_candidates
        self.rewriter = None
        # this represents the text to be added in target i.e. public int a;
        self.field_tobe_moved = field_tobe_moved
        self.methods_tobe_updated = []

    def enterCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
        super().enterCompilationUnit(ctx)
        self.rewriter = TokenStreamRewriter(ctx.parser.getTokenStream())

    def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        super().enterClassDeclaration(ctx)

        if ctx.parentCtx.classOrInterfaceModifier()[0].getText() == "public":
            self.current_class_name = ctx.IDENTIFIER().getText()

        self.has_imported_source = self.file_info.has_imported_package(self.package.name) or \
                                   self.file_info.has_imported_class(self.package.name, self.source_class)

        # import target if we're not in Target and have not imported before
        if self.current_class_name != self.target_class:
            self.rewriter.insertBeforeIndex(ctx.parentCtx.start.tokenIndex,
                                            f"import {self.target_package}.{self.target_class};\n")

    def enterClassBody(self, ctx: JavaParser.ClassBodyContext):
        super().exitClassBody(ctx)
        if self.current_class_name == self.target_class:
            replacement_text = ""
            if self.field_tobe_moved.name == self.field_name:
                for mod in self.field_tobe_moved.modifiers:
                    replacement_text += f"{mod} "
                replacement_text += f"{self.field_tobe_moved.datatype} {self.field_tobe_moved.name};"
            self.rewriter.insertAfter(ctx.start.tokenIndex, f"\n\t{replacement_text}\n")

            # add getter and setter
            name = self.field_tobe_moved.name
            method_name = self.field_tobe_moved.name.upper() + self.field_tobe_moved.name[1:-1]
            type = self.field_tobe_moved.datatype

            getter = f"\tpublic {type} get{method_name}() {{ return this.{name}; }}\n"
            setter = f"\tpublic void set{method_name}({type} {name}) {{ this.{name} = {name}; }}\n"
            self.rewriter.insertBeforeIndex(ctx.stop.tokenIndex, getter)
            self.rewriter.insertBeforeIndex(ctx.stop.tokenIndex, setter)

    def exitFieldDeclaration(self, ctx: JavaParser.FieldDeclarationContext):
        super().exitFieldDeclaration(ctx)
        if self.current_class_name != self.source_class:
            return

        if self.field_tobe_moved is None:
            field = self.package.classes[self.current_class_name].fields[
                ctx.variableDeclarators().children[0].children[0].IDENTIFIER().getText()]
            if field.name == self.field_name:
                self.field_tobe_moved = field

    def exitClassBody(self, ctx: JavaParser.ClassBodyContext):
        super().exitClassBody(ctx)
        save(self.rewriter, self.filename)

    def exitMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        super().exitMethodDeclaration(ctx)
        # we will remove getter and setter from source
        # and add it to target so there is no need to
        # find usages there

        if self.current_class_name == self.source_class and \
                self.is_method_getter_or_setter(ctx.IDENTIFIER().getText()):
            self.rewriter.replaceRange(
                ctx.parentCtx.parentCtx.start.tokenIndex,
                ctx.parentCtx.parentCtx.stop.tokenIndex, "")

    def exitConstructorDeclaration(self, ctx: JavaParser.ConstructorDeclarationContext):
        self.current_method.name = ctx.IDENTIFIER().getText()
        self.current_method.returntype = self.current_method.class_name
        self.handleMethodUsage(ctx, True)
        super().exitConstructorDeclaration(ctx)

    def exitMethodBody(self, ctx: JavaParser.MethodBodyContext):
        super().exitMethodBody(ctx)
        self.handleMethodUsage(ctx, False)

    def handleMethodUsage(self, ctx, is_constructor: bool):
        method_identifier = ctx.IDENTIFIER().getText() if is_constructor else ctx.parentCtx.IDENTIFIER().getText()
        formal_params = ctx.formalParameters() if is_constructor else ctx.parentCtx.formalParameters()
        target_added = False
        target_param_name = "$$target"
        target_param = f"Target {target_param_name}" if \
            len(self.current_method.parameters) == 0 \
            else f", Target {target_param_name}"

        # if we have not imported source package or
        # Source class just ignore this
        if not self.has_imported_source:
            return

        local_candidates = set()
        if self.current_class_name == self.source_class:
            # we will remove getter and setter from source
            # and add it to target so there is no need to
            # find usages there
            if self.is_method_getter_or_setter(method_identifier):
                self.rewriter.replaceRange(ctx.start.tokenIndex, ctx.stop.tokenIndex, "")
                return
            local_candidates.add("this")

        # find parameters with type Source
        for t, identifier in self.current_method.parameters:
            if t == self.source_class:
                local_candidates.add(identifier)

        # find all local variables with type Source
        for var_or_exprs in self.current_method.body_local_vars_and_expr_names:
            if type(var_or_exprs) is LocalVariable:
                if var_or_exprs.datatype == self.source_class:
                    local_candidates.add(var_or_exprs.identifier)

        should_ignore = False

        for var_or_exprs in self.current_method.body_local_vars_and_expr_names:
            if type(var_or_exprs) is ExpressionName:
                # we're going to find source.field
                try:
                    local_ctx = var_or_exprs.parser_context.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx
                    creator = local_ctx.expression()[0].getText()
                    if creator.__contains__(
                            f"new{self.source_class}") and local_ctx.IDENTIFIER().getText() == self.field_name:
                        self.propagate_field(local_ctx, target_param_name)

                except:
                    pass

                if len(var_or_exprs.dot_separated_identifiers) < 2:
                    continue
                if (var_or_exprs.dot_separated_identifiers[0] in local_candidates or
                    var_or_exprs.dot_separated_identifiers[0] in self.field_candidates) and \
                        var_or_exprs.dot_separated_identifiers[1] == self.field_name:
                    if not target_added:
                        # add target to param
                        self.rewriter.insertBeforeIndex(formal_params.stop.tokenIndex,
                                                        target_param)
                        self.methods_tobe_updated.append(self.current_method)
                        target_added = True

                    self.usages.append(var_or_exprs.parser_context)
                    self.propagate_field(var_or_exprs.parser_context, target_param_name)

            elif type(var_or_exprs) is MethodInvocation:
                # we are going to find getter or setters
                # if len(var_or_exprs.dot_separated_identifiers) < 2:
                #     continue
                if var_or_exprs.dot_separated_identifiers[0] == f"new{self.source_class}":
                    if var_or_exprs.parser_context.methodCall() is not None and \
                            self.is_method_getter_or_setter(
                                var_or_exprs.parser_context.methodCall().IDENTIFIER().getText()):
                        self.propagate_getter_setter(var_or_exprs.parser_context, target_param_name)
                elif self.is_method_getter_or_setter(var_or_exprs.dot_separated_identifiers[0]):
                    if not target_added:
                        # add target to param
                        self.rewriter.insertBeforeIndex(formal_params.stop.tokenIndex,
                                                        target_param)
                        self.methods_tobe_updated.append(self.current_method)
                        target_added = True
                    if not should_ignore and var_or_exprs.parser_context is not None and type(
                            var_or_exprs.parser_context) is not JavaParser.ExpressionContext:
                        continue
                    self.usages.append(var_or_exprs.parser_context)
                    self.propagate_getter_setter_form2(var_or_exprs.parser_context, target_param_name)
                elif len(var_or_exprs.dot_separated_identifiers) > 1 and self.is_getter_or_setter(
                        var_or_exprs.dot_separated_identifiers[0],
                        var_or_exprs.dot_separated_identifiers[1], local_candidates):
                    if not target_added:
                        # add target to param
                        self.rewriter.insertBeforeIndex(formal_params.stop.tokenIndex,
                                                        target_param)
                        self.methods_tobe_updated.append(self.current_method)
                        target_added = True

                    self.usages.append(var_or_exprs.parser_context)
                    self.propagate_getter_setter(var_or_exprs.parser_context, target_param_name)

    def is_getter_or_setter(self, first_id: str, second_id: str, local_candidates: set):
        return (first_id in local_candidates or first_id in self.field_candidates) and (
                second_id == f"set{self.field_name[0].upper() + self.field_name[1:-1]}" or
                second_id == f"get{self.field_name[0].upper() + self.field_name[1:-1]}" or
                second_id == f"has{self.field_name[0].upper() + self.field_name[1:-1]}" or
                second_id == f"is{self.field_name[0].upper() + self.field_name[1:-1]}"
        )

    def is_method_getter_or_setter(self, method: str):
        return (
                method == f"set{self.field_name[0].upper() + self.field_name[1:-1]}" or
                method == f"get{self.field_name[0].upper() + self.field_name[1:-1]}" or
                method == f"has{self.field_name[0].upper() + self.field_name[1:-1]}" or
                method == f"is{self.field_name[0].upper() + self.field_name[1:-1]}"
        )

    def propagate_getter_setter(self, ctx: JavaParser.ExpressionContext, target_name: str):
        index = ctx.DOT().symbol.tokenIndex
        self.rewriter.replaceRange(ctx.start.tokenIndex, index - 1, target_name)

    def propagate_getter_setter_form2(self, ctx: JavaParser.ExpressionContext, target_name: str):
        """
        form 2 is getA() setA()...
        """
        self.rewriter.insertBeforeIndex(ctx.start.tokenIndex, f"{target_name}.")

    def propagate_field(self, ctx: JavaParser.ExpressionContext, target_name: str):
        index = ctx.DOT().symbol.tokenIndex
        self.rewriter.replaceRange(ctx.start.tokenIndex, index - 1, target_name)


def save(rewriter: TokenStreamRewriter, file_name: str, filename_mapping=lambda x: x + ".rewritten.java"):
    new_filename = filename_mapping(file_name).replace("\\", "/")
    path = new_filename[:new_filename.rfind('/')]
    if not os.path.exists(path):
        os.makedirs(path)
    with open(new_filename, mode='w', newline='') as file:
        file.write(rewriter.getDefaultText())


class MethodUsageListener(UtilsListener):
    def __init__(self, filename: str, methods: str, target_class: str):
        super().__init__(filename)
        self.methods = methods
        self.method_names = set(map(lambda m: m.name, methods))
        self.rewriter = None
        self.target_class = target_class

    def enterCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
        super().enterCompilationUnit(ctx)
        self.rewriter = TokenStreamRewriter(ctx.parser.getTokenStream())

    def enterClassCreatorRest(self, ctx: JavaParser.ClassCreatorRestContext):
        if type(ctx.parentCtx) is JavaParser.CreatorContext:
            if ctx.parentCtx.createdName().IDENTIFIER()[0].getText() not in self.method_names:
                return
        text = f"new {self.target_class}()" if ctx.arguments().expressionList() is None else f", new {self.target_class}()"
        index = ctx.arguments().RPAREN().symbol.tokenIndex
        self.rewriter.insertBeforeIndex(index, text)

    def exitMethodCall(self, ctx: JavaParser.MethodCallContext):
        super().exitMethodCall(ctx)
        if ctx.IDENTIFIER().getText() in self.method_names:
            text = f"new {self.target_class}()" if ctx.expressionList() is None else f", new {self.target_class}()"
            self.rewriter.insertBeforeIndex(ctx.RPAREN().symbol.tokenIndex, text)

    def exitClassBody(self, ctx: JavaParser.ClassBodyContext):
        super().exitClassBody(ctx)
        save(self.rewriter, self.filename)


def get_filenames_in_dir(directory_name: str, filter=lambda x: x.endswith(".java")) -> list:
    result = []
    for (dirname, dirnames, filenames) in os.walk(directory_name):
        result.extend([dirname + '/' + name for name in filenames if filter(name)])
    return result


def clean_up_dir(files: list) -> list:
    """
    :param files: List of files in the project directory
    :return: list

    Cleans up trashed files and gives original files
    """

    original_files = list()
    for file in files:
        if "rewritten.java" in file:
            os.remove(file)
        else:
            original_files.append(file)
    return original_files


if __name__ == '__main__':
    source_class = "JSONArray"
    source_package = "org.json"
    target_class = "JSON Object"
    target_package = "org.json"
    field_name = "myArrayList"
    files = get_filenames_in_dir(
        '/home/nima/Nima/Uni/Compiler/Project/CodART/benchmark_projects/JSON/src/main/java/org/json/')
    field = None
    methods_tobe_update = []
    for file in files:
        stream = FileStream(file, encoding='utf8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParser(token_stream)
        tree = parser.compilationUnit()
        utilsListener = UtilsListener(file)
        walker = ParseTreeWalker()
        walker.walk(utilsListener, tree)

        if len(utilsListener.package.classes) > 1:
            exit(1)

        # find fields with the type Source first and store it
        field_candidate = set()
        for klass in utilsListener.package.classes.values():
            for f in klass.fields.values():
                if f.datatype == source_class:
                    field_candidate.add(f.name)

        listener = FieldUsageListener(
            file,
            source_class,
            source_package,
            target_class,
            target_package,
            field_name,
            field_candidate,
            field)
        walker.walk(listener, tree)

        methods_tobe_update = listener.methods_tobe_updated + methods_tobe_update

        if file.__contains__(source_class):
            field = listener.field_tobe_moved

    for method in methods_tobe_update:
        print(method.name)

    filess = [f'{file}.rewritten.java' for file in files]
    for i, file in enumerate(files):
        stream = FileStream(filess[i], encoding='utf8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParser(token_stream)
        tree = parser.compilationUnit()
        listener = MethodUsageListener(file, methods_tobe_update, target_class)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
