__version__ = '0.1.0'
__author__ = 'MIna'

import networkx as nx

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from refactorings.gen.Java9_v2Lexer import Java9_v2Lexer
from refactorings.gen.Java9_v2Parser import Java9_v2Parser
from refactorings.gen.Java9_v2Listener import Java9_v2Listener
from refactorings.gen.Java9_v2Visitor import Java9_v2Visitor

import visualization.graph_visualization


class MoveMethodRefactoringListener(Java9_v2Listener):
    #implement move method class
    def __init__(self,common_token_stream: CommonTokenStream = None,
                 method_identifier: str = None, source_class: str = None, target_class:str = None):
        """
        :param common_token_stream
        """
        self.enter_class = False
        self.token_stream = common_token_stream
        self.method_identifier = method_identifier
        self.source_class = source_class
        self.target_class = target_class
        
         # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')
        self.field_dict = {}
        self.method_name = []  #
        self.method_no = 0
