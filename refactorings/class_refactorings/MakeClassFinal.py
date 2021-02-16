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




class MakeFinalClassRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, class_name: str = None):


        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if class_name is None:
            raise ValueError("source_class is None")
        else:
            self.objective_class = class_name

        self.is_objective_class = False

        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        print("Refactoring started, please wait...")
        if self.objective_class == ctx.IDENTIFIER().getText():
            self.token_stream_rewriter.replaceRange(
                from_idx=0,
                to_idx=0,
                text= "final "+ctx.CLASS().getText()
            )
    # def enterTypeDeclaration(self, ctx:JavaParserLabeled.TypeDeclarationContext):
    #     print("Refactoring started, please wait...")
    #     if self.objective_class == ctx.classDeclaration().IDENTIFIER().getText():
    #
    #         self.token_stream_rewriter.replaceRange(
    #             from_idx=ctx.classOrInterfaceModifier(0).start.tokenIndex,
    #             to_idx=ctx.classOrInterfaceModifier(0).stop.tokenIndex,
    #             text=ctx.classOrInterfaceModifier(0).getText()+" final"
    #         )
