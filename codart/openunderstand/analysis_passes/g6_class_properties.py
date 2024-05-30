"""
The helper module for couple_coupleby.py, create_createby_G11.py, declare_declareby.py modules
Todo: Must be document well
"""

__author__ = (
    "Parmida Majmasanaye , Zahra Momeninezhad , Bayan Divaani-Azar , Bavan Divaani-Azar"
)
__version__ = "0.1.0"


from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from antlr4 import *


RULES = [
    JavaParserLabeled.RULE_classDeclaration,
    JavaParserLabeled.RULE_methodDeclaration,
    JavaParserLabeled.RULE_enumDeclaration,
    JavaParserLabeled.RULE_interfaceDeclaration,
    JavaParserLabeled.RULE_constructorDeclaration,
    JavaParserLabeled.RULE_annotationTypeDeclaration,
]


class ClassPropertiesListener(JavaParserLabeledListener):
    def __init__(self) -> None:
        self.class_name = None
        self.package_name = None
        self.class_properties = None
        self.class_longname = []

    def checkParents(self, ctx: JavaParserLabeled.ClassDeclarationContext) -> set:
        return set(ClassPropertiesListener.findParents(ctx)) & set(
            self.class_longname[::-1]
        )

    def enterPackageDeclaration(
        self, ctx: JavaParserLabeled.PackageDeclarationContext
    ) -> None:
        self.package_name = ctx.qualifiedName().getText()

    @staticmethod
    def findParents(ctx: ParserRuleContext) -> list:  # includes the ctx identifier
        parents = []
        current = ctx.parentCtx
        while current is not None:
            if current.getRuleIndex() in RULES:
                parents.append(current.IDENTIFIER().getText())
            current = current.parentCtx
        return parents[::-1]

    def extractOriginalText(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        token_source = ctx.start.getTokenSource()
        input_stream = token_source.inputStream
        start, stop = ctx.start.start, ctx.stop.stop
        return input_stream.getText(start, stop)

    def enterClassDeclaration(
        self, ctx: JavaParserLabeled.ClassDeclarationContext
    ) -> None:
        if self.class_properties:  # already found the class
            return None

        if self.class_longname[-1] == ctx.IDENTIFIER().getText() and self.checkParents(
            ctx
        ):

            # this is the exact class we wanted.
            self.class_properties = {
                "name": self.class_longname[-1],
                "longname": ".".join(self.class_longname),
                "package_name": self.package_name,
                "parent": (
                    None if len(self.class_longname) == 1 else self.class_longname[-2]
                ),
                "modifiers": ctx.parentCtx.getChild(0).getText(),
                "contents": self.extractOriginalText(ctx.parentCtx),
            }


class InterfacePropertiesListener(JavaParserLabeledListener):
    def __init__(self) -> None:
        self.interface_longname = []
        self.interface_properties = None

    def checkParents(self, ctx: JavaParserLabeled.InterfaceDeclarationContext) -> set:
        return set(ClassPropertiesListener.findParents(ctx)) & set(
            self.interface_longname[::-1]
        )

    def enterInterfaceDeclaration(
        self, ctx: JavaParserLabeled.InterfaceDeclarationContext
    ) -> None:
        if self.interface_properties:  # already found the interface
            return

        if self.interface_longname[
            -1
        ] == ctx.IDENTIFIER().getText() and self.checkParents(ctx):

            # this is the exact class we wanted.
            self.interface_properties = {
                "name": self.interface_longname[-1],
                "longname": ".".join(self.interface_longname),
                "parent": (
                    None
                    if len(self.interface_longname) == 1
                    else self.interface_longname[-2]
                ),
                "modifiers": ClassPropertiesListener.findClassOrInterfaceModifiers(ctx),
                "contents": ctx.getText(),
            }
