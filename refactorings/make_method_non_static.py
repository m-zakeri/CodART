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


class MakeMethodNonStaticRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(
            self, common_token_stream: CommonTokenStream = None,
            target_class: str = None, target_methods: list = None):

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if target_class is None:
            raise ValueError("source_class is None")
        else:
            self.target_class = target_class
        if target_methods is None or len(target_methods) ==0:
            raise ValueError("target method must have one method name")
        else:
            self.target_methods = target_methods

        self.is_target_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        print("Refactoring started, please wait...")
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.target_class:
            self.is_target_class = True
        else:
            self.is_target_class = False

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_target_class:
            self.is_target_class = False

    def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        if self.is_target_class:
            if ctx.IDENTIFIER().getText() in self.target_methods:
                grand_parent_ctx = ctx.parentCtx.parentCtx
                if grand_parent_ctx.modifier():
                    if len(grand_parent_ctx.modifier()) == 2:
                        self.token_stream_rewriter.delete(
                            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                            from_idx=grand_parent_ctx.modifier(1).start.tokenIndex-1,
                            to_idx=grand_parent_ctx.modifier(1).stop.tokenIndex
                        )
                    else:
                        if grand_parent_ctx.modifier(0).getText() == 'static':
                            self.token_stream_rewriter.delete(
                                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                from_idx=grand_parent_ctx.modifier(0).start.tokenIndex-1,
                                to_idx=grand_parent_ctx.modifier(0).stop.tokenIndex
                            )
                else:
                    return None

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        print("Finished Processing...")