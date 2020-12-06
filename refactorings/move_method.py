__version__ = '0.1.0'
__author__ = 'Mina'

import networkx as nx

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from refactorings.gen.Java9_v2Lexer import Java9_v2Lexer
from refactorings.gen.Java9_v2Parser import Java9_v2Parser
from refactorings.gen.Java9_v2Listener import Java9_v2Listener
from refactorings.gen.Java9_v2Visitor import Java9_v2Visitor
import visualization.graph_visualization


class MoveMethodRecognizerListener(Java9_v2Listener):
    """
    To detect whether class needs refactoring or not.
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

    # Groups methods in terms of their dependencies on the class attributes and one another
    def split_class(self):
        # 1- move the dictionary of fields into a new dictionary of methods operating on fields
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
            class_methods = [(class_.nodes[node]['method_name'], node) for node in class_.nodes if
                             class_.in_degree(node) > 0]
            print('class_fields', class_fields)
            print('class_methods', class_methods)
            print('-' * 10)

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


class MoveMethodRefactoringListener(Java9_v2Listener):
    # implement move method class
    def __init__(self, common_token_stream: CommonTokenStream = None,
                 source_class_identifier: str = None, target_class_identifier: str = None,
                 method_identifier=None, moved_fields=None):
        """
        :param common_token_stream
        """
        self.enter_class_source = False
        self.enter_class_target = False
        self.token_stream = common_token_stream

        if method_identifier is None:
            self.method_identifier = []
        else:
            self.method_identifier = method_identifier
        if moved_fields is None:
            self.moved_fields = []
        else:
            self.moved_fields = moved_fields
        if source_class_identifier is None:
            raise ValueError("source_class_identifier is None")
        else:
            self.source_class_identifier = source_class_identifier

        if target_class_identifier is None:
            raise ValueError("target_class_identifier is None")
        else:
            self.target_class_identifier = target_class_identifier

        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

        self.is_source_class = False
        self.is_target_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    def enterNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        print("Refactoring started, please wait...")
        class_identifier = ctx.identifier().getText()
        if class_identifier == self.source_class_identifier:
            self.is_source_class = True
            self.code += self.NEW_LINE * 2
            self.code += f"// Method moved to class {self.target_class_identifier}  by CodART" + self.NEW_LINE
        else:
            self.is_source_class = False

    # Exit a parse tree produced by Java9_v2Parser#normalClassDeclaration.
    def exitNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        if self.is_source_class:
            self.is_source_class = False

    def exitOrdinaryCompilation(self, ctx: Java9_v2Parser.OrdinaryCompilationContext):
        print("Finished Processing...")
        self.token_stream_rewriter.insertBefore(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            index=ctx.stop.tokenIndex,
            text=self.code
        )

    def enterVariableDeclaratorId(self, ctx: Java9_v2Parser.VariableDeclaratorIdContext):
        if not self.is_source_class:
            return None
        field_identifier = ctx.identifier().getText()
        if field_identifier in self.moved_fields:
            self.detected_field = field_identifier

    def exitFieldDeclaration(self, ctx: Java9_v2Parser.FieldDeclarationContext):
        if not self.is_source_class:
            return None
        field_names = ctx.variableDeclaratorList().getText().split(",")
        if self.detected_field in field_names:
            modifier = ctx.fieldModifier(0).getText()
            field_type = ctx.unannType().getText()
            self.code += f"{self.TAB}{modifier} {field_type} {self.detected_field};{self.NEW_LINE}"
            # delete field from source class
            field_names.remove(self.detected_field)
            if field_names:
                self.token_stream_rewriter.replaceRange(
                    from_idx=ctx.start.tokenIndex,
                    to_idx=ctx.stop.tokenIndex,
                    text=f"{modifier} {field_type} {','.join(field_names)};"
                )
            else:
                self.token_stream_rewriter.delete(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=ctx.start.tokenIndex,
                    to_idx=ctx.stop.tokenIndex
                )
            self.detected_field = None

    def enterMethodDeclarator(self, ctx: Java9_v2Parser.MethodDeclaratorContext):
        if not self.is_source_class:
            return None
        method_identifier = ctx.identifier().getText()
        if method_identifier in self.method_identifier:
            self.detected_method = method_identifier

    def exitMethodDeclaration(self, ctx: Java9_v2Parser.MethodDeclarationContext):
        if not self.is_source_class:
            return None
        method_identifier_get = ctx.methodHeader().methodDeclarator().identifier().getText()
        if self.detected_method == method_identifier_get:
            start_index = ctx.start.tokenIndex
            stop_index = ctx.stop.tokenIndex
            method_text = self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=start_index,
                stop=stop_index
            )
            self.code += (self.NEW_LINE + self.TAB + method_text + self.NEW_LINE)
            # delete method from source class
            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=start_index,
                to_idx=stop_index
            )
            self.detected_method = None
