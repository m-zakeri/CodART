from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import openunderstand.analysis_passes.class_properties as class_properties


class DotRef_DotRefBy(JavaParserLabeledListener):
    state = False
    class_name = []

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        all_pac = ctx.qualifiedName().IDENTIFIER()
        self.class_name.append(ctx.qualifiedName().getText())
        if len(all_pac) > 0:
            self.state = True

    def findmethodreturntype(self, c):
        parents = ""
        context = ""
        current = c
        while current is not None:
            if type(current.parentCtx).__name__ == "MethodDeclarationContext":
                parents = current.parentCtx.typeTypeOrVoid().getText()
                context = current.parentCtx.getText()
                break
            current = current.parentCtx

        return parents, context

    def findmethodacess(self, c):
        parents = ""
        current = c
        modifiers = []
        while current is not None:
            if "ClassBodyDeclaration" in type(current.parentCtx).__name__:
                if hasattr(current.parentCtx, "modifier"):
                    parents = current.parentCtx.modifier()
                break
            current = current.parentCtx
        for x in parents:
            if x.classOrInterfaceModifier():
                modifiers.append(x.classOrInterfaceModifier().getText())
        return modifiers

    implement = []

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.class_name.append(ctx.IDENTIFIER().getText())

    def enterExpression1(self, ctx: JavaParserLabeled.Expression0Context):

        if ctx.DOT():
            if ctx.expression() and ("DOT" not in dir(ctx.expression())):
                modifiers = self.findmethodacess(ctx)
                mothodedreturn, methodcontext = self.findmethodreturntype(ctx)

                if self.state:
                    refEntName = ctx.expression().getText()
                else:
                    refEntName = None

                allrefs = class_properties.ClassPropertiesListener.findParents(
                    ctx
                )  # self.findParents(ctx)
                refent = allrefs[-1]
                if refEntName in self.class_name or refEntName is None:
                    entlongname = ".".join(allrefs)
                    [line, col] = str(ctx.start).split(",")[3].split(":")

                    self.implement.append(
                        {
                            "scopename": refent,
                            "scopelongname": entlongname,
                            "scopemodifiers": modifiers,
                            "scopereturntype": mothodedreturn,
                            "scopecontent": methodcontext,
                            "line": line,
                            "col": col[:-1],
                            "refent": refEntName,
                            "scope_parent": allrefs[-2] if len(allrefs) > 2 else None,
                            "potential_refent": (
                                ".".join(allrefs[:-1]) + "." + refEntName
                                if refEntName
                                else ""
                            ),
                        }
                    )
