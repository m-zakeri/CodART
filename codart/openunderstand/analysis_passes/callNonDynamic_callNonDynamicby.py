"""
## Description
This module find all OpenUnderstand call and callby references in a Java project


## References


"""

# from OpenUnderstand.openunderstand.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
# from OpenUnderstand.openunderstand.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
# import OpenUnderstand.openunderstand.analysis_passes.class_properties as class_properties
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import openunderstand.analysis_passes.class_properties as class_properties


class CallNonDynamicAndCallNonDynamicBy(JavaParserLabeledListener):
    """
    #Todo: Implementing the ANTLR listener pass for Java Call and Java Callby reference kind
    """

    def __init__(self):
        self.implement = []

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        bodies = ctx.classBody().classBodyDeclaration()
        if bodies is not None:
            if ctx.EXTENDS():
                extendedBy = ctx.typeType().classOrInterfaceType().IDENTIFIER(i=0)
                for body in bodies:
                    member = getattr(body, "memberDeclaration", None)
                    if member is not None:
                        member = member()
                        method = getattr(member, "methodDeclaration", None)
                        if method is not None:
                            method = method()
                            block = method.methodBody().block()
                            self.dfs(block, method, ctx, extendedBy)

    def dfs(self, ctx, cls, context, extendedBy):
        bStatements = ctx.blockStatement()
        for bStatement in bStatements:
            kk = str(type(bStatement)).split(".")[-1][:-2]
            kk2 = "BlockStatement1Context"
            if kk == kk2:

                statement = bStatement.statement()

                s = getattr(statement, "statement", None)

                if s is not None:
                    s = s()
                    bb = getattr(s, "block", None)
                    if bb is not None:
                        bb = bb()
                        self.dfs(bb, cls, context, extendedBy)
                else:
                    exp = statement
                    if hasattr(statement, "expression"):
                        exp = statement.expression()
                    exp2 = getattr(exp, "expression", None)
                    if exp2 is not None:
                        exp2 = exp2()
                        primary = getattr(exp2, "primary", None)
                        if primary is not None:
                            primary = primary()
                            super = getattr(primary, "SUPER", None)
                            if super is not None:
                                super = super()

                                if type(exp) == list:

                                    for exp3 in exp:
                                        methodCall = getattr(exp3, "methodCall", None)
                                        if methodCall is not None:
                                            methodCall = methodCall()
                                            if methodCall is not None:
                                                called = methodCall.IDENTIFIER()
                                                scope_parents = class_properties.ClassPropertiesListener.findParents(
                                                    context
                                                )

                                                if len(scope_parents) == 1:
                                                    scope_longname = scope_parents[0]
                                                else:
                                                    scope_longname = ".".join(
                                                        scope_parents
                                                    )

                                                line = context.children[0].symbol.line
                                                col = context.children[0].symbol.column
                                                self.implement.append(
                                                    {
                                                        "scope_kind": "Class",
                                                        "scope_name": cls.IDENTIFIER().__str__(),
                                                        "scope_longname": str(
                                                            scope_longname
                                                        ),
                                                        "scope_parent": (
                                                            scope_parents[-2]
                                                            if len(scope_parents) > 2
                                                            else None
                                                        ),
                                                        "scope_contents": cls.getText(),
                                                        "scope_modifiers": class_properties.ClassPropertiesListener.findClassOrInterfaceModifiers(
                                                            context
                                                        ),
                                                        "line": line,
                                                        "col": col,
                                                        "type_ent_longname": str(
                                                            called
                                                        ),
                                                    }
                                                )

                                else:
                                    methodCall = getattr(exp, "methodCall", None)
                                    if methodCall is not None:
                                        methodCall = methodCall()
                                        if methodCall is not None:
                                            called = methodCall.IDENTIFIER()
                                            scope_parents = class_properties.ClassPropertiesListener.findParents(
                                                context
                                            )

                                            if len(scope_parents) == 1:
                                                scope_longname = scope_parents[0]
                                            else:
                                                scope_longname = ".".join(scope_parents)

                                            line = methodCall.start.line
                                            col = methodCall.start.column
                                            self.implement.append(
                                                {
                                                    "scope_kind": "Class",
                                                    "scope_name": cls.IDENTIFIER().__str__(),
                                                    "scope_longname": str(
                                                        scope_longname
                                                    ),
                                                    "scope_parent": (
                                                        scope_parents[-2]
                                                        if len(scope_parents) > 2
                                                        else None
                                                    ),
                                                    "scope_contents": cls.getText(),
                                                    "scope_modifiers": class_properties.ClassPropertiesListener.findClassOrInterfaceModifiers(
                                                        context
                                                    ),
                                                    "line": line,
                                                    "col": col,
                                                    "type_ent_longname": str(called),
                                                }
                                            )
