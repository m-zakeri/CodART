from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class TypedAndTypedByListener(JavaParserLabeledListener):
    def __init__(self):
        self.package_name = ""
        self.typedBy = []

    @property
    def get_type(self):
        d = {}
        d["typedBy"] = self.typedBy
        return d

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_name = ctx.getText().replace("package", "").replace(";", "")

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        # ==========typed/typedby=============
        ctx1 = ctx.variableDeclarators()
        ctx_name = ctx1.variableDeclarator()[0].variableDeclaratorId()
        ctx_type = ctx.typeType()

        type_line = ctx_type.children[0].children[0].symbol.line
        type_column = ctx_type.children[0].children[0].symbol.column
        name_line = ctx_name.IDENTIFIER().symbol.line
        name_column = ctx_name.IDENTIFIER().symbol.column

        self.typedBy.append(
            (
                ctx_name.getText(),
                ctx_type.getText(),
                name_line,
                name_column,
                type_line,
                type_column,
                self.package_name,
            )
        )

    # khode enum
    def enterEnumDeclaration(self, ctx: JavaParserLabeled.EnumDeclarationContext):
        ctx_name = ctx.IDENTIFIER()
        ctx_type = ctx.ENUM()

        type_line = ctx_type.symbol.line
        type_column = ctx_type.symbol.column
        name_line = ctx_name.symbol.line
        name_column = ctx_name.symbol.column

        self.typedBy.append(
            (
                ctx.IDENTIFIER().getText(),
                ctx_type.getText(),
                name_line,
                name_column,
                type_line,
                type_column,
                self.package_name,
            )
        )

    # type haye enum
    def enterEnumConstant(self, ctx: JavaParserLabeled.EnumConstantContext):
        # type enum
        enum_type = ctx.IDENTIFIER()
        # esme khode enum
        pctx = ctx.parentCtx.parentCtx

        type_line = enum_type.symbol.line
        type_column = enum_type.symbol.column
        name_line = pctx.IDENTIFIER().symbol.line
        name_column = pctx.IDENTIFIER().symbol.column

        self.typedBy.append(
            (
                pctx.IDENTIFIER().getText(),
                ctx.getText(),
                name_line,
                name_column,
                type_line,
                type_column,
                self.package_name,
            )
        )

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        # method types
        t = ctx.typeTypeOrVoid()
        try:
            ctx_type = t.typeType()
            type_line = ctx_type.children[0].children[0].symbol.line
            type_column = ctx_type.children[0].children[0].symbol.column
            name_line = ctx.IDENTIFIER().symbol.line
            name_column = ctx.IDENTIFIER().symbol.column
        except:
            ctx_type = t.VOID()
            type_line = t.children[0].symbol.line
            type_column = t.children[0].symbol.column
            name_line = ctx.IDENTIFIER().symbol.line
            name_column = ctx.IDENTIFIER().symbol.column

        self.typedBy.append(
            (
                ctx.IDENTIFIER().getText(),
                ctx_type.getText(),
                name_line,
                name_column,
                type_line,
                type_column,
                self.package_name,
            )
        )

    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        ctx_name = ctx.variableDeclaratorId()
        ctx_type = ctx.typeType()

        type_line = ctx_type.children[0].children[0].symbol.line
        type_column = ctx_type.children[0].children[0].symbol.column
        name_line = ctx_name.IDENTIFIER().symbol.line
        name_column = ctx_name.IDENTIFIER().symbol.column

        self.typedBy.append(
            (
                ctx_name.getText(),
                ctx_type.getText(),
                name_line,
                name_column,
                type_line,
                type_column,
                self.package_name,
            )
        )

    def enterLocalVariableDeclaration(
        self, ctx: JavaParserLabeled.LocalVariableDeclarationContext
    ):
        # baraye try va catch va function
        ctx1 = ctx.variableDeclarators()
        ctx_name = ctx1.variableDeclarator()[0].variableDeclaratorId()
        ctx_type = ctx.typeType()

        type_line = ctx_type.children[0].children[0].symbol.line
        type_column = ctx_type.children[0].children[0].symbol.column
        name_line = ctx_name.IDENTIFIER().symbol.line
        name_column = ctx_name.IDENTIFIER().symbol.column

        self.typedBy.append(
            (
                ctx_name.getText(),
                ctx_type.getText(),
                name_line,
                name_column,
                type_line,
                type_column,
                self.package_name,
            )
        )
