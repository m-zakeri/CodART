__version__ = '0.1.0'
__author__ = 'Mina'

import networkx as nx

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from refactorings.gen.Java9_v2Lexer import Java9_v2Lexer
from refactorings.gen.Java9_v2Parser import Java9_v2Parser
from refactorings.gen.Java9_v2Listener import Java9_v2Listener
from refactorings.gen.Java9_v2Visitor import Java9_v2Visitor


class MoveMethodRefactoringListener(Java9_v2Listener):
    # implement move method class
    def __init__(self, common_token_stream: CommonTokenStream = None,
                 source_class_identifier: str = None, target_class_identifier: str = None,
                 method_identifier: str = None, ):
        """
        :param common_token_stream
        """
        self.enter_class = False
        self.token_stream = common_token_stream
        self.method_identifier = method_identifier
        self.source_class_identifier = source_class_identifier
        self.target_class_identifier = target_class_identifier

        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')
        self.field_dict = {}
        self.method_name = []
        self.method_no = 0

    # Groups methods in terms of their dependencies on the class attributes and one another
    def split_class(self):
        # 1- move the dictionary of fields into a new dictionary of methods operating on fields
        # method_dict = {}
        methods = []
        for key, value in self.field_dict.items():
            for method in value:
                # print(method)
                if method[0] == self.method_identifier:
                    methods.append(method[0])
                    print(methods)
            #     if not str(method) in method_dict:
            #         method_dict[str(method)] = [key]
            #     else:
            #         method_dict[str(method)].append(key)
            # print("methods dic.", method_dict)

    def enterNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        if ctx.identifier().getText() != self.source_class_identifier:
            return
        self.enter_class = True

        # Exit a parse tree produced by Java9_v2Parser#normalClassDeclaration.

    def exitNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        self.enter_class = False
        # print("----------------------------")
        # print("Class attributes and methods using each attribute ")
        # print("field dictionary =", self.field_dict)
        # print("----------------------------")
        self.split_class()
        self.field_dict = {}
        self.method_name = []
        self.method_no = 0

        # when exiting from a class attribute (field) declaration this method is invoked.
        # This method adds attributes of the source class to a dictionary

    def enterFieldDeclaration(self, ctx: Java9_v2Parser.FieldDeclarationContext):
        if not self.enter_class:
            return
        field_id = ctx.variableDeclaratorList().variableDeclarator(i=0).variableDeclaratorId().identifier().getText()
        self.field_dict[field_id] = []

        # Enter a parse tree produced by Java9_v2Parser#methodDeclaration.

    def enterMethodDeclaration(self, ctx: Java9_v2Parser.MethodDeclarationContext):
        if not self.enter_class:
            return
        m = []
        m_name = ctx.methodHeader().methodDeclarator().identifier().getText()
        self.method_no = self.method_no + 1
        m.append(m_name)
        m.append(self.method_no)
        self.method_name.append(m)

        # Exit a parse tree produced by Java9_v2Parser#methodDeclaration.

    def exitMethodDeclaration(self, ctx: Java9_v2Parser.MethodDeclarationContext):
        if not self.enter_class:
            return

        # Exit a parse tree produced by Java9_v2Parser#identifier.

    def exitIdentifier(self, ctx: Java9_v2Parser.IdentifierContext):
        if not self.enter_class:
            return
        if self.method_no == 0:
            return
        current_method = self.method_name[-1]
        variable_name = ctx.getText()
        if variable_name not in self.field_dict:
            return
        if not current_method in self.field_dict[variable_name]:
            self.field_dict[variable_name].append(current_method)
