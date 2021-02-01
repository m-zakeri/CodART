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
            source_class: str = None, destination_class: str = None, source_class_data: dict = None):

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if source_class is None:
            raise ValueError("source_class is None")
        else:
            self.source_class = source_class

        if destination_class:
            self.destination_class = destination_class
        if source_class_data:
            self.source_class_data = source_class_data
        else:
            self.source_class_data = {'fields': [], 'methods': []}

        self.is_target_class = False
        self.is_source_class = False
        self.target_class = None
        self.detected_field = None
        self.detected_method = None
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
            l = self.source_class_data
            self.is_source_class = False
        if self.is_target_class:
            self.token_stream_rewriter.insertAfter(
                index=ctx.stop.tokenIndex - 1,
                text=self.code
            )

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        if self.is_source_class:
            self.code += self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.start.tokenIndex + 1,
                stop=ctx.stop.tokenIndex - 1
            )
            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.parentCtx.start.tokenIndex,
                to_idx=ctx.parentCtx.stop.tokenIndex
            )
        else:
            return None

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        print("Finished Processing...")

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if self.is_source_class:
            field_text = ''
            for child in ctx.children:
                if child.getText() == ';':
                    field_text = field_text[:len(field_text)-1] + ';'
                    break
                field_text += child.getText() + ' '
            name = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText()
            modifier_text = ''
            for modifier in ctx.parentCtx.parentCtx.modifier():
                modifier_text += modifier.getText() + ' '
            field_text = modifier_text + field_text
            self.source_class_data['fields'].append(Field(name=name, text=field_text))


class Field:
    def __init__(self, text: str = None, name: str = None):
        self.text = text
        self.name = name
