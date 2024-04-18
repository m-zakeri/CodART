"""
## Description
This module find all OpenUnderstand modify and modifyby references in a Java project

## References

"""

__author__ = "Shaghayegh Mobasher , Setayesh kouloubandi ,Parisa Alaie"
__version__ = "0.1.0"

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class ModifyModifyByListener(JavaParserLabeledListener):
    """
    #Todo: Implementing the ANTLR listener pass for Java modify and Java modifyby reference kind
    """

    def __init__(self):
        self.modifyBy = []
        self.scope = None
        self.ent = None
        self.isE7 = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.scope = ctx.IDENTIFIER().getText()

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.scope = ctx.IDENTIFIER().getText()

    def enterExpression0(self, ctx: JavaParserLabeled.Expression0Context):
        self.ent = ctx.getText()

    def exitExpression0(self, ctx: JavaParserLabeled.Expression0Context):
        if self.isE7:
            line_col = str(ctx.children[1].start).split(",")[3][:-1].split(":")

            self.modifyBy.append(
                {
                    "scope": self.scope,
                    "ent": self.ent,
                    "line": line_col[0],
                    "col": line_col[1],
                }
            )

    def enterExpression6(self, ctx: JavaParserLabeled.Expression6Context):
        self.isE7 = False
        line_col = str(ctx.children[0].start).split(",")[3][:-1].split(":")
        self.modifyBy.append(
            {
                "scope": self.scope,
                "ent": self.ent,
                "line": line_col[0],
                "col": line_col[1],
            }
        )

    def enterExpression7(self, ctx: JavaParserLabeled.Expression7Context):
        self.isE7 = True

    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        self.isE7 = False
        operations = ["+=", "-=", "/=", "*=", "&=", "|=", "^=", "%="]
        line_col = str(ctx.children[0].start).split(",")[3][:-1].split(":")
        if ctx.children[1].getText() in operations:
            self.modifyBy.append(
                {
                    "scope": self.scope,
                    "ent": self.ent,
                    "line": line_col[0],
                    "col": line_col[1],
                }
            )
