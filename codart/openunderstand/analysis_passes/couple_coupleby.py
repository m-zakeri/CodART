"""
## Description
This module find all OpenUnderstand call and callby references in a Java project


## References


"""

__author__ = "AminHZ Dev"
__version__ = "0.1.0"

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class CoupleAndCoupleBy(JavaParserLabeledListener):
    couples = []

    def __init__(self):
        self.couples = []

    def addReference(
        self,
        scope_kind,
        scope_name,
        scope_longname,
        scope_parent,
        scope_contents,
        scope_modifiers,
        line,
        col,
        type_ent_longname,
    ):

        if scope_name is not None and type_ent_longname is not None:
            self.couples.append(
                {
                    "scope_kind": scope_kind,
                    "scope_name": scope_name,
                    "scope_longname": scope_longname,
                    "scope_parent": scope_parent,
                    "scope_contents": scope_contents,
                    "scope_modifiers": scope_modifiers,
                    "line": line,
                    "col": col,
                    "type_ent_longname": type_ent_longname,
                }
            )

    def addStaticClassesToCouples(
        self, ctx, expression: JavaParserLabeled.Expression0Context
    ):
        self.addReference(
            "Class",
            ctx.IDENTIFIER().getText(),
            ctx.IDENTIFIER().getText(),
            None,
            ctx.getText(),
            [],
            expression.primary().children[0].symbol.line,
            expression.primary().children[0].symbol.column,
            str(expression.primary().getText()),
        )

    def addClassObjectsToCouples(self, ctx, field):
        typeType = field.typeType()
        targetClass = typeType.classOrInterfaceType()

        if targetClass is not None:

            self.addReference(
                "Class",
                ctx.IDENTIFIER().getText(),
                ctx.IDENTIFIER().getText(),
                None,
                ctx.getText(),
                [],
                targetClass.children[0].symbol.line,
                targetClass.children[0].symbol.column,
                str(targetClass.IDENTIFIER()[0]),
            )

    def globalClassVariablesAnalyzer(self, ctx, member):
        field = member.fieldDeclaration()
        self.addClassObjectsToCouples(ctx, field)

    def parameterVariablesAnalyzer(self, ctx, formalParameters):
        for formalParameter in formalParameters.formalParameter():
            self.addClassObjectsToCouples(ctx, formalParameter)

    def recursiveExpressions(
        self, ctx, expression: JavaParserLabeled.Expression1Context
    ):
        mainExpression = expression.expression()
        while (
            type(mainExpression) != JavaParserLabeled.Expression0Context
            and mainExpression.expression()
            and type(mainExpression.expression())
            == JavaParserLabeled.Expression0Context
        ):
            mainExpression = mainExpression.expression()
        if type(mainExpression) == JavaParserLabeled.Expression0Context:
            self.addStaticClassesToCouples(ctx, mainExpression)
            methodCall = expression.methodCall()
            if (
                type(methodCall) == JavaParserLabeled.MethodCall0Context
                and type(methodCall.expressionList())
                == JavaParserLabeled.ExpressionListContext
            ):
                expressionList = methodCall.expressionList()
                if expressionList.expression():
                    for subExpression in expressionList.expression():
                        if type(subExpression) == JavaParserLabeled.Expression1Context:
                            self.recursiveExpressions(ctx, subExpression)

    def localMethodVariablesAnalyzer(self, ctx, block):
        for blockStatement in block.blockStatement():
            if type(blockStatement) == JavaParserLabeled.BlockStatement0Context:
                variable = blockStatement.localVariableDeclaration()
                self.addClassObjectsToCouples(ctx, variable)
            elif type(blockStatement) == JavaParserLabeled.BlockStatement1Context:
                statement = blockStatement.statement()
                if type(statement) == JavaParserLabeled.Statement15Context:
                    expression = statement.expression()
                    if type(expression) == JavaParserLabeled.Expression1Context:
                        self.recursiveExpressions(ctx, expression)

    def methodAnalyzer(self, ctx, member):
        formalParameters = (
            member.methodDeclaration().formalParameters().formalParameterList()
        )
        if type(formalParameters) == JavaParserLabeled.FormalParameterList0Context:
            self.parameterVariablesAnalyzer(ctx, formalParameters)

        block = member.methodDeclaration().methodBody().block()
        self.localMethodVariablesAnalyzer(ctx, block)

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        for item in ctx.classBody().classBodyDeclaration():
            member = item.memberDeclaration()

            if (
                type(item) == JavaParserLabeled.ClassBodyDeclaration2Context
                and type(member) == JavaParserLabeled.MemberDeclaration2Context
            ):
                # Global class variables declaration
                self.globalClassVariablesAnalyzer(ctx, member)

            elif (
                type(item) == JavaParserLabeled.ClassBodyDeclaration2Context
                and type(member) == JavaParserLabeled.MemberDeclaration0Context
            ):
                # Method declaration
                self.methodAnalyzer(ctx, member)
