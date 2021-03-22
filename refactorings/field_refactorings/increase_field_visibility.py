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


class IncreaseFieldVisibilityRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class=None, field_name:str = None):

        if field_name is None:
            self.field_name = ""
        else:
            self.field_name = field_name

        if source_class is None:
            self.source_class = ""
        else:
            self.source_class = source_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_source_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""
        self.tempdeclarationcode=""

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        print("Refactoring started, please wait...")
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = True
        else:
            self.is_source_class = False

    def exitFieldDeclaration(self, ctx:JavaParserLabeled.FieldDeclarationContext):
        if not self.is_source_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        # field_identifier = ctx.variableDeclarators().getText().split(",")
        field_identifier = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText()
        if self.field_name in field_identifier:
            if grand_parent_ctx.modifier()==[]:
                self.token_stream_rewriter.replaceRange(
                    from_idx=ctx.typeType().start.tokenIndex,
                    to_idx=ctx.typeType().stop.tokenIndex,
                    text='private '+ ctx.typeType().getText()
                )
            elif grand_parent_ctx.modifier(0).getText() == 'public':
                self.token_stream_rewriter.replaceRange(
                    from_idx=grand_parent_ctx.modifier(0).start.tokenIndex,
                    to_idx=grand_parent_ctx.modifier(0).stop.tokenIndex,
                    text='private')
            elif grand_parent_ctx.modifier(0).getText() != 'private':
                self.token_stream_rewriter.replaceRange(
                    from_idx=grand_parent_ctx.modifier(0).start.tokenIndex,
                    to_idx=grand_parent_ctx.modifier(0).stop.tokenIndex,
                    text='private '+grand_parent_ctx.modifier(0).getText())
            # generate accessor and mutator methods
            # Accessor body
            new_code = '\n\t'
            new_code += 'public ' + ctx.typeType().getText() + ' get' + str.capitalize(self.field_name)
            new_code += '() { \n\t\t return this.' + self.field_name + ';' + '\n\t}'

            # Mutator body
            new_code += '\n\t'
            new_code += 'public void set' + str.capitalize(self.field_name)
            new_code += '(' + ctx.typeType().getText() + ' ' + self.field_name + ') { \n\t\t'
            new_code += 'this.' + self.field_name + ' = ' + self.field_name + ';' + '\n\t}\n'

            self.token_stream_rewriter.insertAfter(ctx.stop.tokenIndex, new_code)


        print("Finished Processing...")




class PropagationIncreaseFieldVisibilityRefactoringListener(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, using_field_name= None, object_name=None,
                 propagated_class_name=None):

        if using_field_name is None:
            self.using_field_name = []
        else:
            self.using_field_name = using_field_name

        if object_name is None:
            self.object_name = []
        else:
            self.object_name = object_name

        if propagated_class_name is None:
            self.propagated_class_name = []
        else:
            self.propagated_class_name = propagated_class_name

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_class = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        # print("Propagation started, please wait...")
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.propagated_class_name:
            self.is_class = True
            print("Propagation started, please wait...")
        else:
            self.is_class = False

    def enterVariableDeclarator(self, ctx:JavaParserLabeled.VariableDeclaratorContext):
        if not self.is_class:
            return None
        usingfieldidentifier=ctx.variableDeclaratorId().IDENTIFIER().getText()
        grand_child_ctx = ctx.variableInitializer().expression()
        if usingfieldidentifier in self.using_field_name:
            objectidentifier = grand_child_ctx.expression(0).primary().IDENTIFIER().getText()
            if objectidentifier in self.object_name:
                self.token_stream_rewriter.replaceRange(
                    from_idx=grand_child_ctx.start.tokenIndex,
                    to_idx=grand_child_ctx.stop.tokenIndex,
                    text=grand_child_ctx.expression(0).primary().IDENTIFIER().getText()+'.'
                         +'get' + str.capitalize(grand_child_ctx.IDENTIFIER().getText())+'()'
                )

    def enterExpression(self, ctx:JavaParserLabeled.ExpressionContext):
        if not self.is_class:
            return
        if ctx.expression(0)!=None:
            if ctx.expression(0).primary() != None:
                if ctx.expression(0).primary().IDENTIFIER().getText() in self.object_name:
                    parent_ctx = ctx.parentCtx
                    count=parent_ctx.getChildCount()
                    if count==3:
                        expressiontext=parent_ctx.children[2].getText()
                        self.token_stream_rewriter.replaceRange(
                            from_idx=parent_ctx.start.tokenIndex,
                            to_idx=parent_ctx.stop.tokenIndex,
                            text=ctx.expression(0).primary().IDENTIFIER().getText() +
                                 '.' + 'set' + str.capitalize(ctx.IDENTIFIER().getText()) +'(' +expressiontext+')'
                        )

class PropagationIncreaseFieldVisibility_GetObjects_RefactoringListener(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class=None,
                 propagated_class_name=None):

        if source_class is None:
            self.source_class = []
        else:
            self.source_class = source_class

        if propagated_class_name is None:
            self.propagated_class_name = []
        else:
            self.propagated_class_name = propagated_class_name

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_class = False
        self.current_class=''
        self.objects=list()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        # print("Propagation started, please wait...")
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier in self.propagated_class_name:
            self.is_class = True
            print("Propagation started, please wait...")
            self.current_class=class_identifier
        else:
            self.is_class = False

    def enterVariableDeclarator(self, ctx:JavaParserLabeled.VariableDeclaratorContext):
        if not self.is_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        if grand_parent_ctx.typeType().classOrInterfaceType() != None:
            className=grand_parent_ctx.typeType().classOrInterfaceType().IDENTIFIER(0).getText()
            if className in self.source_class:
                objectname=ctx.variableDeclaratorId().IDENTIFIER().getText()
                self.objects.append(objectname)


