"""


"""

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import analysis_passes.class_properties as class_properties


class DefineListener(JavaParserLabeledListener):
    def __init__(self):
        self.defines = []
        self.package = ""
        self.lambda_expression_count = 0

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package = [str(i) for i in ctx.qualifiedName().IDENTIFIER()]

        ent_start = ctx.qualifiedName().IDENTIFIER()[0]
        ent_name = ctx.qualifiedName().IDENTIFIER()[-1].getText()
        ent_longname = ".".join(self.package)
        line = ent_start.symbol.line
        column = ent_start.symbol.column
        self.defines.append(
            {
                "scope": None,
                "ent": ent_name,
                "scope_longname": None,
                "ent_longname": ent_longname,
                "line": line,
                "col": column,
            }
        )

    def add_define_info(self, ent, ent_parents, ent_name=None):
        if ent_name is None:
            ent_name = ent.getText()
        line = ent.symbol.line
        column = ent.symbol.column
        scope_longname = ".".join(self.package + ent_parents)
        ent_longname = scope_longname + "." + ent_name
        if len(ent_parents) == 0:
            scope_name = None
        else:
            scope_name = ent_parents[-1]
        self.defines.append(
            {
                "scope": scope_name,
                "ent": ent_name,
                "scope_longname": scope_longname,
                "ent_longname": ent_longname,
                "line": line,
                "col": column,
            }
        )

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        ent = ctx.IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)

    def enterInterfaceDeclaration(
        self, ctx: JavaParserLabeled.InterfaceDeclarationContext
    ):
        ent = ctx.IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        ent = ctx.IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)

    def enterAnnotationTypeDeclaration(
        self, ctx: JavaParserLabeled.AnnotationTypeDeclarationContext
    ):
        ent = ctx.IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)

    def enterConstructorDeclaration(
        self, ctx: JavaParserLabeled.ConstructorDeclarationContext
    ):
        ent = ctx.IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)

    def enterVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        ent = ctx.variableDeclaratorId().IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)

    def enterEnumConstant(self, ctx: JavaParserLabeled.EnumConstantContext):
        ent = ctx.IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)

    def enterEnumDeclaration(self, ctx: JavaParserLabeled.EnumDeclarationContext):
        ent = ctx.IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)
        self.add_define_info(ent, ent_parents + [ent.getText()], "values")
        self.add_define_info(ent, ent_parents + [ent.getText()], "valueOf")

    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParametersContext):
        ent = ctx.variableDeclaratorId().IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)

    def enterLambdaParameters0(self, ctx: JavaParserLabeled.LambdaParameters0Context):
        self.lambda_expression_count += 1
        ent = ctx.IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        ent_name = f"(lambda_expr_{self.lambda_expression_count})"
        self.add_define_info(ent, ent_parents, ent_name)
        self.add_define_info(ent, ent_parents + [ent_name])

    def enterLambdaParameters2(self, ctx: JavaParserLabeled.LambdaParameters2Context):
        self.lambda_expression_count += 1
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        ent_name = f"(lambda_expr_{self.lambda_expression_count})"
        identifiers = ctx.IDENTIFIER()
        self.add_define_info(identifiers[0], ent_parents, ent_name)
        for ent in identifiers:
            self.add_define_info(ent, ent_parents + [ent_name])

    def enterEnhancedForControl(self, ctx: JavaParserLabeled.EnhancedForControlContext):
        ent = ctx.variableDeclaratorId().IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)

    def enterCatchClause(self, ctx: JavaParserLabeled.CatchClauseContext):
        ent = ctx.IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)

    def enterTypeParameter(self, ctx: JavaParserLabeled.TypeParameterContext):
        ent = ctx.IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)

    def enterConstantDeclarator(self, ctx: JavaParserLabeled.ConstantDeclaratorContext):
        ent = ctx.IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)

    def enterLastFormalParameter(
        self, ctx: JavaParserLabeled.LastFormalParameterContext
    ):
        ent = ctx.variableDeclaratorId().IDENTIFIER()
        ent_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        self.add_define_info(ent, ent_parents)
