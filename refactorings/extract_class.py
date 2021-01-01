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

import visualization.graph_visualization


class ExtractClassRefactoringListener(Java9_v2Listener):
    """
    To implement the extract class refactoring
    Encapsulate field: Make a public field private and provide accessors
    a stream of tokens is sent to the listener, to build an object token_stream_rewriter
    field addresses the field of the class, tobe encapsulated.
    """

    def __init__(self, common_token_stream: CommonTokenStream = None,
                 class_identifier: str = None):
        """
        :param common_token_stream:
        """
        self.enter_class = False
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')
        self.field_dict = {}
        self.method_name = []  #
        self.method_no = 0

    # Groups methods in terms of their dependncies on the class attributes and one another
    def split_class(self):
        # 1- move the dictionay of fields into a new dictionary of methods operating on fields
        method_dict = {}
        for key, value in self.field_dict.items():
            for method in value:
                if not str(method) in method_dict:
                    method_dict[str(method)] = [key]
                else:
                    method_dict[str(method)].append(key)
        print("methods dic.", method_dict)
        # 2- Group methods in terms of their dependencies on one another
        method_group = dict()
        # _____________________To be modified ________________________
        # 3- Group methods in terms of their dependencies on the class attributes
        for key, value in method_dict.items():
            if not str(value) in method_group:
                method_group[str(value)] = [key]
            else:
                method_group[str(value)].append(key)
        print("methods group", method_group)

        # --------------------------------------
        # 4- Create graph
        G = nx.DiGraph()
        for field, methods in self.field_dict.items():
            for method in methods:
                print('add edge {0} --> {1}'.format(field, method))
                G.add_node(method[1], method_name=method[0])
                G.add_edge(field, method[1])

        print('---------\nExtracted classes:')
        visualization.graph_visualization.draw(g=G)
        # CC = nx.connected_components(G)
        S = [G.subgraph(c).copy() for c in nx.weakly_connected_components(G)]

        for class_ in S:
            # print('class_', class_.nodes.data())
            class_fields = [node for node in class_.nodes if class_.in_degree(node) == 0]
            class_methods = [(class_.nodes[node]['method_name'], node) for node in class_.nodes if class_.in_degree(node) > 0]
            print('class_fields', class_fields)
            print('class_methods', class_methods)
            print('-'*10)

# Enter a parse tree produced by Java9_v2Parser#normalClassDeclaration.
    def enterNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        if ctx.identifier().getText() != self.class_identifier:
            return
        self.enter_class = True

# Exit a parse tree produced by Java9_v2Parser#normalClassDeclaration.
    def exitNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        self.enter_class = False
        print("----------------------------")
        print("Class attributes and methods using each attribute ")
        print("field dictionary =", self.field_dict)
        print("----------------------------")
        self.split_class()
        self.field_dict = {}
        self.method_name = []
        self.method_no = 0

    # when exiting from a class attribute (field) declaration this method is invoked.
    # This method adds attributes of the target class to a dictionary
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
