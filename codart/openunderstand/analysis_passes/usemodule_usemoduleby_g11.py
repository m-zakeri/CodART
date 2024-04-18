"""
## Description
This module find all OpenUnderstand Usemodule and Usemoduleby references in a Java project

## References

"""

__author__ = "Navid Mousavizade, Amir Mohammad Sohrabi, Sara Younesi, Deniz Ahmadi"
__version__ = "0.1.0"

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class UseModuleUseModuleByListener(JavaParserLabeledListener):
    """
    Todo: Implementing the ANTLR listener pass for Java Usemodule and Java Usemoduleby reference kind
    """

    def __init__(self):
        self.useModules = []
        self.useUnknownModules = []
        self.useUnresolvedModules = []
        self.methods = []

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.methods.append(ctx.IDENTIFIER().getText())

    def enterAnnotation(self, ctx: JavaParserLabeled.AnnotationContext):
        line_col = str(ctx.start).split(",")[3][:-1].split(":")
        self.useModules.append(
            {
                "scope": "",
                "ent": "",
                "name": ctx.children[1].IDENTIFIER()[0].getText(),
                "line": line_col[0],
                "col": line_col[1],
                "package": "",
            }
        )
        self.useUnresolvedModules.append(
            {
                "scope": "",
                "ent": "",
                "name": ctx.children[1].IDENTIFIER()[0].getText(),
                "line": line_col[0],
                "col": line_col[1],
                "package": "",
            }
        )

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        package_name_array = ctx.getText().replace("package", "").split(".")
        if len(package_name_array) == 4 and package_name_array[0] == "com":
            self.useUnknownModules.append(
                {
                    "scope": None,
                    "ent": ctx.getChild(1).IDENTIFIER()[3].getText(),
                    "name": ctx.getChild(1).IDENTIFIER()[2].getText(),
                    "line": 1,
                    "col": 1,
                    "package": ctx.getText(),
                }
            )
            self.useUnresolvedModules.append(
                {
                    "scope": None,
                    "ent": ctx.getChild(1).IDENTIFIER()[3].getText(),
                    "name": ctx.getChild(1).IDENTIFIER()[2].getText(),
                    "line": 1,
                    "col": 1,
                    "package": ctx.getText(),
                }
            )
