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


class DeclareAndDeclareinListener(JavaParserLabeledListener):
    """
    #Todo: Implementing the ANTLR listener pass for Java Call and Java Callby reference kind

    """

    def __init__(self):
        self.declare = []

    def enterCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        if not ctx.packageDeclaration():  # unnamed package
            self.declare.append({"scope": None, "ent": None, "line": 1, "col": 0})

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        all_declared = ctx.qualifiedName().IDENTIFIER()
        longname = ""
        for i in range(len(all_declared)):
            ent_name = all_declared[i].getText()
            ent_longname = longname + ("." if longname != "" else "") + ent_name
            self.declare.append(
                {
                    "scope": all_declared[i - 1].getText() if i != 0 else None,
                    "ent": ent_name,
                    "scope_longname": longname,
                    "ent_longname": ent_longname,
                    "line": all_declared[i].symbol.line,
                    "col": all_declared[i].symbol.column,
                }
            )
            longname = ent_longname
