import os

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import openunderstand.analysis_passes.class_properties as class_properties
from openunderstand.oudb.models import ProjectModel, EntityModel


def throws_parent_finder(root_dir, file_name):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".java") and file == (file_name + ".java"):
                root_splited = str(root).split("/")
                org_index = root_splited.index("org")
                return ".".join(root_splited[org_index:])


class Throws_TrowsBy(JavaParserLabeledListener):
    def __init__(self):
        self.implement = []

    def findmethodreturntype(self, c):
        parents = ""
        context = ""
        current = c
        parents_list = [
            "ConstructorDeclarationContext",
            "MethodDeclarationContext",
            "InterfaceMethodDeclarationContext",
        ]
        while current is not None:
            if type(current.parentCtx).__name__ in parents_list:
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

    # def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
    #     if ctx.IMPLEMENTS():
    #         scope_parents = class_properties.ClassPropertiesListener.findParents(ctx)
    #         if len(scope_parents) == 1:
    #             scope_longname = scope_parents[0]
    #         else:
    #             scope_longname = ".".join(scope_parents)
    #
    #         [line, col] = str(ctx.start).split(",")[3].split(":")
    #         for myType in ctx.typeList().typeType():
    #             if myType.classOrInterfaceType():
    #                 myType_longname = ".".join([x.getText() for x in myType.classOrInterfaceType().IDENTIFIER()])
    #                 self.implement.append({"scope_kind": "Class", "scope_name": ctx.IDENTIFIER().__str__(),
    #                                        "scope_longname": scope_longname,
    #                                        "scope_parent": scope_parents[-2] if len(scope_parents) > 2 else None,
    #                                        "scope_contents": ctx.getText(),
    #                                        "scope_modifiers":
    #                                            class_properties.ClassPropertiesListener.findClassOrInterfaceModifiers(ctx),
    #                                        "line": line,
    #                                        "col": col[:-1],
    #                                        "type_ent_longname": myType_longname})

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.EnumDeclarationContext):

        if ctx.THROWS():
            modifiers = self.findmethodacess(ctx)
            mothodedreturn, methodcontext = self.findmethodreturntype(ctx)
            refEntName = ctx.qualifiedNameList().getText().split(",")[-1]
            if refEntName:
                allrefs = class_properties.ClassPropertiesListener.findParents(
                    ctx
                )  # self.findParents(ctx)
                refent = allrefs[-1]
                entlongname = ".".join(allrefs)
                is_here = throws_parent_finder(
                    ProjectModel.select()[0].root, refEntName
                )
                if is_here is not None:
                    refEntName = is_here + "." + refEntName
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
                        "potential_refent": ".".join(allrefs[:-1]) + "." + refEntName,
                    }
                )

    def enterConstructorDeclaration(
        self, ctx: JavaParserLabeled.EnumDeclarationContext
    ):

        if ctx.THROWS():
            modifiers = self.findmethodacess(ctx)
            mothodedreturn, methodcontext = self.findmethodreturntype(ctx)
            refEntName = ctx.qualifiedNameList().getText().split(",")[-1]
            if refEntName:
                allrefs = class_properties.ClassPropertiesListener.findParents(
                    ctx
                )  # self.findParents(ctx)
                refent = allrefs[-1]
                entlongname = ".".join(allrefs)
                is_here = throws_parent_finder(
                    ProjectModel.select()[0].root, refEntName
                )
                if is_here is not None:
                    refEntName = is_here + "." + refEntName
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
                        "potential_refent": ".".join(allrefs[:-1]) + "." + refEntName,
                    }
                )

    def enterInterfaceMethodDeclaration(
        self, ctx: JavaParserLabeled.EnumDeclarationContext
    ):

        if ctx.THROWS():
            modifiers = self.findmethodacess(ctx)
            mothodedreturn, methodcontext = self.findmethodreturntype(ctx)
            refEntName = ctx.qualifiedNameList().getText().split(",")[-1]
            if refEntName:
                allrefs = class_properties.ClassPropertiesListener.findParents(
                    ctx
                )  # self.findParents(ctx)
                refent = allrefs[-1]
                entlongname = ".".join(allrefs)
                is_here = throws_parent_finder(
                    ProjectModel.select()[0].root, refEntName
                )
                if is_here is not None:
                    refEntName = is_here + "." + refEntName
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
                        "potential_refent": ".".join(allrefs[:-1]) + "." + refEntName,
                    }
                )
