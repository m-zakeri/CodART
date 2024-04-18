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


class ExtendCoupleAndExtendCoupleBy(JavaParserLabeledListener):
    """
    #Todo: Implementing the ANTLR listener pass for Java Call and Java Callby reference kind
    """

    def __init__(self):
        self.implement = []

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):

        # if ctx.IMPLEMENTS():
        scope_parents = class_properties.ClassPropertiesListener.findParents(ctx)

        if len(scope_parents) == 1:
            scope_longname = scope_parents[0]
        else:
            scope_longname = ".".join(scope_parents)

        line = ctx.children[0].symbol.line
        col = ctx.children[0].symbol.column
        if ctx.EXTENDS():
            extendedBy = ctx.typeType().classOrInterfaceType().IDENTIFIER(i=0)
            print("[DEBUG] ExtendCouples: ", scope_parents, scope_longname, extendedBy)

            self.implement.append(
                {
                    "scope_kind": "Class",
                    "scope_name": ctx.IDENTIFIER().__str__(),
                    "scope_longname": str(scope_longname),
                    "scope_parent": scope_parents[-2]
                    if len(scope_parents) > 2
                    else None,
                    "scope_contents": ctx.getText(),
                    "scope_modifiers": class_properties.ClassPropertiesListener.findClassOrInterfaceModifiers(
                        ctx
                    ),
                    "line": line,
                    "col": col,
                    "type_ent_longname": str(extendedBy),
                }
            )
