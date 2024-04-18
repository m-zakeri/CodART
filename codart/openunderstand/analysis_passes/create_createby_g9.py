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
import openunderstand.analysis_passes.class_properties as class_properties


class CreateAndCreateBy(JavaParserLabeledListener):
    def __init__(self):
        self.package_long_name = ""

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

    # def findmethodaccess(self, c):
    #     parents = ""
    #     modifiers=[]
    #     current = c
    #     while current is not None:
    #         if "ClassBodyDeclaration" in type(current.parentCtx).__name__:
    #             parents=(current.parentCtx.modifier())
    #             break
    #         current = current.parentCtx
    #     for x in parents:
    #         if x.classOrInterfaceModifier():
    #             modifiers.append(x.classOrInterfaceModifier().getText())
    #     return modifiers

    def findmethodaccess(self, ctx):
        modifiers_list = [
            "Default",
            "Private",
            "Public",
            "Protected",
            "Static",
            "Generic",
            "Abstract",
            "Final",
        ]
        parent_modifiers = ""
        modifiers = []
        parent_type = ""
        current = ctx
        while current is not None:
            if "ClassBodyDeclaration2" in type(current.parentCtx).__name__:
                parent_modifiers = current.parentCtx.modifier()
                if "MethodDeclaration" in type(current.children[0]).__name__:
                    parent_type = "Method"
                elif "ConstructorDeclaration" in type(current.children[0]).__name__:
                    parent_type = "Constructor"
                # elif "FieldDeclaration" in type(current.children[0]).__name__:
                #     parent_type = "Method"
                elif "ClassDeclaration" in type(current.children[0]).__name__:
                    parent_type = "Class"
                elif "EnumDeclaration" in type(current.children[0]).__name__:
                    parent_type = "Enum"
                else:
                    parent_type = "Unresolved"
                break
            current = current.parentCtx

        for modifier in parent_modifiers:
            if modifier.classOrInterfaceModifier():
                if (
                    modifier.classOrInterfaceModifier().getText().title()
                    in modifiers_list
                ):
                    modifiers.append(modifier.classOrInterfaceModifier().getText())

        return modifiers, parent_type

    create = []

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_long_name = ctx.qualifiedName().getText()

    def enterExpression4(self, ctx: JavaParserLabeled.Expression4Context):
        modifiers, parent_type = self.findmethodaccess(ctx)
        mothodedreturn, methodcontext = self.findmethodreturntype(ctx)

        if ctx.creator().classCreatorRest():
            all_parents = class_properties.ClassPropertiesListener.findParents(ctx)
            scope_name = all_parents[-1]
            scope_longname = self.package_long_name + "." + ".".join(all_parents)
            [line, col] = str(ctx.start).split(",")[3].split(":")

            self.create.append(
                {
                    "scopename": scope_name,
                    "scopelongname": scope_longname,
                    "scopemodifiers": modifiers,
                    "parent_type": parent_type,
                    "scopereturntype": mothodedreturn,
                    "scopecontent": methodcontext,
                    "line": line,
                    "col": col[:-1],
                    "refent": ctx.creator().createdName().getText(),
                    "scope_parent": all_parents[-2] if len(all_parents) > 2 else None,
                    "potential_refent": ".".join(all_parents[:-1])
                    + "."
                    + ctx.creator().createdName().getText(),
                }
            )
