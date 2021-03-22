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



class GetMethodTextMoveMethodUpRefactoringListener(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, child_class=None, moved_methods=None):

        if moved_methods is None:
            self.moved_methods = []
        else:
            self.moved_methods = moved_methods
        if child_class is None:
            self.moved_methods = []
        else:
            self.children_class = child_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_children_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""
        self.tempdeclarationcode=""
        self.method_text= ""

    def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        print("Refactoring started, please wait...")
        if self.is_children_class:

            method_identifier = ctx.IDENTIFIER().getText()
            if self.moved_methods == method_identifier:
                methodDefctx = ctx.parentCtx.parentCtx
                start_index = methodDefctx.start.tokenIndex
                stop_index = methodDefctx.stop.tokenIndex
                self.method_text = self.token_stream_rewriter.getText(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    start=start_index,
                    stop=stop_index)

        else:
            return None

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        print("children class in get text refactor:",self.children_class)
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier in self.children_class:
            self.is_children_class = True

        else:
            print("enter other class")
            self.is_children_class = False


class MoveMethodUpRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, destination_class: str = None,
                 children_class:list=None, moved_methods=None, method_text:str = None):

        if method_text is None:
            self.mothod_text = []
        else:
            self.method_text = method_text

        if moved_methods is None:
            self.moved_methods = []
        else:
            self.moved_methods = moved_methods
        if children_class is None:
            self.children_class = []
        else:
            self.children_class = children_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if destination_class is None:
            raise ValueError("source_class is None")
        else:
            self.destination_class = destination_class

        self.is_children_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""
        self.tempdeclarationcode=""

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        print("Refactoring started, please wait...")
        if self.is_children_class:

            method_identifier = ctx.IDENTIFIER().getText()
            if self.moved_methods == method_identifier:
                methodDefctx = ctx.parentCtx.parentCtx
                start_index = methodDefctx.start.tokenIndex
                stop_index = methodDefctx.stop.tokenIndex
                self.method_text = self.token_stream_rewriter.getText(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    start=start_index,
                    stop=stop_index)

                self.token_stream_rewriter.delete(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=methodDefctx.start.tokenIndex,
                    to_idx=methodDefctx.stop.tokenIndex
                )
        else:
            return None

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier in self.children_class:
            self.is_children_class = True

        else:
            print("enter other class")
            self.is_children_class = False

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        classDecctx=ctx.parentCtx
        class_identifier = classDecctx.IDENTIFIER().getText()
        if class_identifier in self.destination_class:
                self.token_stream_rewriter.replaceRange(
                    from_idx=ctx.start.tokenIndex+1,
                    to_idx=ctx.start.tokenIndex+1,
                    text="\n" + self.method_text + "\n"
                )
    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        if self.is_children_class:
            self.is_children_class = False

    def exitCompilationUnit(self, ctx:JavaParserLabeled.CompilationUnitContext):
        print("Finished Processing...")
        self.token_stream_rewriter.insertAfter(
            index=ctx.stop.tokenIndex,
            text=self.code
        )


class PropagationMoveMethodUpRefactoringListener(JavaParserLabeledListener):

    def __init__(self, token_stream_rewriter: CommonTokenStream = None, old_class_name:list=None,
                 new_class_name:str=None,propagated_class_name:list=None):

        if propagated_class_name is None:
            self.propagated_class_name = []
        else:
            self.propagated_class_name = propagated_class_name

        if new_class_name is None:
            self.new_class_name = []
        else:
            self.new_class_name = new_class_name

        if old_class_name is None:
            self.old_class_name = []
        else:
            self.old_class_name = old_class_name

        if token_stream_rewriter is None:
            raise ValueError('token_stream_rewriter is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(token_stream_rewriter)

        self.is_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""
        self.tempdeclarationcode=""
        self.method_text= ""

    def enterVariableDeclarator(self, ctx:JavaParserLabeled.VariableDeclaratorContext):
        print("Propagation started, please wait...")
        if not self.is_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        class_identifier = grand_parent_ctx.typeType().getText()
        if class_identifier in self.old_class_name:
            self.token_stream_rewriter.replaceRange(
                from_idx=grand_parent_ctx.typeType().start.tokenIndex,
                to_idx=grand_parent_ctx.typeType().stop.tokenIndex,
                text=self.new_class_name
            )
            grand_child_ctx = ctx.variableInitializer().expression().creator().createdName()
            self.token_stream_rewriter.replaceRange(
                from_idx=grand_child_ctx.start.tokenIndex,
                to_idx=grand_child_ctx.stop.tokenIndex,
                text=self.new_class_name
            )

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier in self.propagated_class_name:
            self.is_class = True

        else:
            print("enter other class")
            self.is_class = False
