"""
The scripts implements different refactoring operations


"""
__version__ = '0.1.0'
__author__ = 'Morteza'

import networkx as nx

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

import visualization.graph_visualization


class CollapseHierarchyRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(
            self, common_token_stream: CommonTokenStream = None,
            source_class: str = None, source_class_data: dict = None,
            target_class: str = None, target_class_data: dict = None):

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if source_class is None:
            raise ValueError("source_class is None")
        else:
            self.source_class = source_class

        if source_class_data:
            self.source_class_data = source_class_data
        else:
            self.source_class_data = {'fields': [], 'methods': [], 'constructors': []}
        if target_class:
            self.target_class = target_class
        else:
            self.target_class = None
        if target_class_data:
            self.target_class_data = target_class_data
        else:
            self.target_class_data = {'fields': [], 'methods': [], 'constructors': []}

        self.is_target_class = False
        self.is_source_class = False
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        print("Refactoring started, please wait...")
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = True
            self.is_target_class = False
            self.target_class = ctx.typeType().classOrInterfaceType().IDENTIFIER(0).getText()
        elif class_identifier == self.target_class:
            self.is_target_class = True
            self.is_source_class = False
        else:
            self.is_target_class = False
            self.is_source_class = False

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_source_class:
            self.is_source_class = False
            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.parentCtx.classOrInterfaceModifier(0).start.tokenIndex,
                to_idx=ctx.stop.tokenIndex
            )
        # if self.is_target_class:
        #     self.token_stream_rewriter.insertAfter(
        #         index=ctx.stop.tokenIndex - 1,
        #         text=self.code
        #     )

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        print("Finished Processing...")

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if self.is_source_class:
            field_text = ''
            for child in ctx.children:
                if child.getText() == ';':
                    field_text = field_text[:len(field_text) - 1] + ';'
                    break
                field_text += child.getText() + ' '
            name = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText()
            modifier_text = ''
            for modifier in ctx.parentCtx.parentCtx.modifier():
                modifier_text += modifier.getText() + ' '
            field_text = modifier_text + field_text
            self.source_class_data['fields'].append(Field(name=name, text=field_text))

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        if self.is_source_class:
            constructor_parameters = [ctx.formalParameters().formalParameterList().children[i] for i in
                                      range(len(ctx.formalParameters().formalParameterList().children)) if i % 2 == 0]
            constructor_text = ''
            for modifier in ctx.parentCtx.parentCtx.modifier():
                constructor_text += modifier.getText() + ' '
            constructor_text += '('
            for parameter in constructor_parameters:
                constructor_text += parameter.typeType().getText() + ' '
                constructor_text += parameter.variableDeclaratorId().getText() + ', '
            constructor_text = constructor_text[:len(constructor_text) - 2]
            constructor_text += ')\n{'
            constructor_text += self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.block().start.tokenIndex + 1,
                stop=ctx.block().stop.tokenIndex - 1
            )
            constructor_text += '}\n'
            self.source_class_data['constructors'].append(ConstructorOrMethod(name=self.source_class,
                                                                              numberOfParameters=len(
                                                                                  constructor_parameters),
                                                                              text=constructor_text))

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_source_class:
            method_parameters = [ctx.formalParameters().formalParameterList().children[i] for i in
                                 range(len(ctx.formalParameters().formalParameterList().children)) if i % 2 == 0]
            method_text = ''
            for modifier in ctx.parentCtx.parentCtx.modifier():
                method_text += modifier.getText() + ' '
            method_text += '('
            for parameter in method_parameters:
                method_text += parameter.typeType().getText() + ' '
                method_text += parameter.variableDeclaratorId().getText() + ', '
            method_text = method_text[:len(method_text) - 2]
            method_text += ')\n{'
            method_text += self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.methodBody().start.tokenIndex + 1,
                stop=ctx.methodBody().stop.tokenIndex - 1
            )
            method_text += '}\n'
            self.source_class_data['methods'].append(ConstructorOrMethod(name=self.source_class,
                                                                         numberOfParameters=len(method_parameters),
                                                                         text=method_text))

    def enterCreatedName0(self, ctx: JavaParserLabeled.CreatedName0Context):
        if ctx.IDENTIFIER(0).getText() == self.source_class and self.target_class:
            self.token_stream_rewriter.replaceIndex(
                index=ctx.start.tokenIndex,
                text=self.target_class
            )

    def enterCreatedName1(self, ctx: JavaParserLabeled.CreatedName1Context):
        if ctx.getText() == self.source_class and self.target_class:
            self.token_stream_rewriter.replaceIndex(
                index=ctx.start.tokenIndex,
                text=self.target_class
            )

    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        class_type = ctx.typeType().classOrInterfaceType()
        if class_type:
            if class_type.IDENTIFIER(0).getText() == self.source_class and self.target_class:
                self.token_stream_rewriter.replaceIndex(
                    index=class_type.start.tokenIndex,
                    text=self.target_class
                )

    def enterQualifiedName(self, ctx: JavaParserLabeled.QualifiedNameContext):
        if ctx.IDENTIFIER(0).getText() == self.source_class and self.target_class:
            self.token_stream_rewriter.replaceIndex(
                index=ctx.start.tokenIndex,
                text=self.target_class
            )


class Field:
    def __init__(self, text: str = None, name: str = None):
        self.text = text
        self.name = name


class ConstructorOrMethod:
    def __init__(self, text: str = None, name: str = None, numberOfParameters: int = None):
        self.text = text
        self.name = name
        self.numberOfParameters = numberOfParameters
