from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class UseAndUseByListener(JavaParserLabeledListener):
    def __init__(self):
        self.package_name = ""
        self.useBy = []

    @property
    def get_use(self):
        d = {}
        d["useBy"] = self.useBy
        return d

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_name = ctx.getText().replace("package", "").replace(";", "")

    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        # ==========used/usedby=============
        is_None = False
        VI = ctx

        while (
            type(ctx) != JavaParserLabeled.ClassDeclarationContext
            and type(ctx) != JavaParserLabeled.MethodDeclarationContext
        ):
            if ctx.parentCtx:
                ctx = ctx.parentCtx
            else:
                is_None = True
                break

        if not is_None:
            line1 = VI.IDENTIFIER().symbol.line
            column1 = VI.IDENTIFIER().symbol.column
            line2 = ctx.IDENTIFIER().symbol.line
            column2 = ctx.IDENTIFIER().symbol.column

            self.useBy.append(
                (
                    VI.getText(),
                    ctx.IDENTIFIER().getText(),
                    line1,
                    column1,
                    line2,
                    column2,
                    self.package_name,
                )
            )
