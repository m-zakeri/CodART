# expression -> NEW creator


"""
## Description
This module find all OpenUnderstand create and createby references in a Java project


## References


"""

__author__ = (
    "Parmida Majmasanaye , Zahra Momeninezhad , Bayan Divaani-Azar , Bavan Divaani-Azar"
)
__version__ = "0.1.0"

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import analysis_passes.g6_class_properties as class_properties


class CreateAndCreateByListener(JavaParserLabeledListener):
    def __init__(self):
        self.class_name = None
        self.package_name = None
        self.new_class_name = None
        self.refers = {}
        self.create = []

    def get_method_content(self, ctx) -> tuple[str, str]:
        # TODO Parents is always equal to ""
        parents = ""
        content = ""
        current = ctx

        while current is not None:
            if type(current.parentCtx).__name__ == "ClassBodyDeclaration2Context":
                content = self.extract_original_text(current.parentCtx)
                break
            current = current.parentCtx

        return parents, content

    def get_new_class_path(self, ctx) -> str:
        path = ""

        while ctx is not None:
            if type(ctx.parentCtx).__name__ == "CompilationUnitContext":
                ctx = ctx.parentCtx
                i = 1
                while True:

                    if ctx.getChild(i) is None:
                        break

                    import_list = ctx.getChild(i).getChild(1).getText().split(".")

                    if import_list[-1] == self.new_class_name:
                        path = "\\".join(import_list) + ".java"
                        break

                    i += 1
            ctx = ctx.parentCtx

        return path

    def get_method_modifiers(self, ctx) -> list:
        parents = ""
        modifiers = []
        current = ctx
        while current is not None:
            if "ClassBodyDeclaration" in type(current.parentCtx).__name__:
                parents = current.parentCtx.modifier()
                break
            current = current.parentCtx

        for p in parents:
            if p.classOrInterfaceModifier():
                modifiers.append(p.classOrInterfaceModifier().getText())

        return modifiers

    def extract_original_text(self, ctx):
        token_source = ctx.start.getTokenSource()
        input_stream = token_source.inputStream
        start, stop = ctx.start.start, ctx.stop.stop
        return input_stream.getText(start, stop)

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_name = ctx.qualifiedName().getText()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.class_name = ctx.IDENTIFIER().getText()

    def enterExpression4(self, ctx: JavaParserLabeled.Expression4Context):

        self.new_class_name = ctx.creator().createdName().IDENTIFIER()[0].getText()
        new_class_path = self.get_new_class_path(ctx)
        if not self.refers.__contains__(self.class_name):
            self.refers[self.class_name] = []
        self.refers[self.class_name].append(self.new_class_name)

        if ctx.creator().classCreatorRest():
            all_refs = class_properties.ClassPropertiesListener.findParents(ctx)
            [line, col] = str(ctx.start).split(",")[3].split(":")

            modifiers = self.get_method_modifiers(ctx)
            method_return, method_context = self.get_method_content(ctx)
            self.create.append(
                {
                    "scope_name": all_refs[-1],
                    "scope_longname": ".".join(all_refs),
                    "scope_modifiers": modifiers,
                    "scope_return_type": method_return,
                    "scope_content": method_context,
                    "line": line,
                    "col": col[:-1],
                    "new_class_name": self.new_class_name,
                    "scope_parent": all_refs[-2] if len(all_refs) > 2 else None,
                    "package_name": self.package_name,
                    "new_class_path": new_class_path,
                }
            )
