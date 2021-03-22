"""
The scripts implements different refactoring operations


"""
__version__ = '0.1.0'
__author__ = 'Morteza'

import networkx as nx

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.java9.Java9_v2Parser import Java9_v2Parser
from gen.java9 import Java9_v2Listener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
import visualization.graph_visualization


class DecreaseMethodVisibilityRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class=None, method_name = None):

        if method_name is None:
            self.method_name = []
        else:
            self.method_name = method_name

        if source_class is None:
            self.source_class = []
        else:
            self.source_class = source_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_source_class = False

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        print("Refactoring started, please wait...")
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = True
        else:
            self.is_source_class = False

    def exitMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        if not self.is_source_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        method_identifier = ctx.IDENTIFIER().getText()
        if self.method_name in method_identifier:
            if grand_parent_ctx.modifier()==[]:
                self.token_stream_rewriter.replaceRange(
                    from_idx=ctx.typeTypeOrVoid().start.tokenIndex,
                    to_idx=ctx.typeTypeOrVoid().stop.tokenIndex,
                    text='public '+ ctx.typeTypeOrVoid().getText()
                )
            elif grand_parent_ctx.modifier(0).getText() == 'private':
                self.token_stream_rewriter.replaceRange(
                    from_idx=grand_parent_ctx.modifier(0).start.tokenIndex,
                    to_idx=grand_parent_ctx.modifier(0).stop.tokenIndex,
                    text='public')
            elif grand_parent_ctx.modifier(0).getText() != 'public':
                self.token_stream_rewriter.replaceRange(
                    from_idx=grand_parent_ctx.modifier(0).start.tokenIndex,
                    to_idx=grand_parent_ctx.modifier(0).stop.tokenIndex,
                    text='public '+grand_parent_ctx.modifier(0).getText())

        print("Finished Processing...")