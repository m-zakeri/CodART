# expression -> NEW creator


"""
## Description
This module find all OpenUnderstand call and callby references in a Java project


## References


"""

__author__ = "Shaghayegh Mobasher , Setayesh kouloubandi ,Parisa Alaie"
__version__ = "0.1.0"

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import analysis_passes.class_properties as class_properties


class CreateAndCreateBy(JavaParserLabeledListener):
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
        modifiers = []
        current = c
        while current is not None:
            if "ClassBodyDeclaration" in type(current.parentCtx).__name__:
                parents = current.parentCtx.modifier()
                break
            current = current.parentCtx
        for x in parents:
            if x.classOrInterfaceModifier():
                modifiers.append(x.classOrInterfaceModifier().getText())
        return modifiers

    create = []

    def enterExpression4(self, ctx: JavaParserLabeled.Expression4Context):
        modifiers = self.findmethodacess(ctx)
        mothodedreturn, methodcontext = self.findmethodreturntype(ctx)

        if ctx.creator().classCreatorRest():
            allrefs = class_properties.ClassPropertiesListener.findParents(
                ctx
            )  # self.findParents(ctx)
            refent = allrefs[-1]
            entlongname = ".".join(allrefs)
            [line, col] = str(ctx.start).split(",")[3].split(":")

            self.create.append(
                {
                    "scopename": refent,
                    "scopelongname": entlongname,
                    "scopemodifiers": modifiers,
                    "scopereturntype": mothodedreturn,
                    "scopecontent": methodcontext,
                    "line": line,
                    "col": col[:-1],
                    "refent": ctx.creator().createdName().getText(),
                    "scope_parent": allrefs[-2] if len(allrefs) > 2 else None,
                    "potential_refent": ".".join(allrefs[:-1])
                    + "."
                    + ctx.creator().createdName().getText(),
                }
            )
