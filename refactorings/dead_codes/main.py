"""

The main module of CodART
This module implements CodART CLI
To find and run more unit and integration tests please look at `benchmark_projects` and `test` directory

-changelog
-- Add support switching between different Java grammar
-- Add JavaParserLabeled.g4
-- Add C++ backend support for Java9_v2.g2
-- Start with encapsulate field refactoring

"""

__version__ = '0.2.1'
__author__ = 'Morteza'

import argparse

from antlr4 import *

# Import different grammars
# from gen.java9.Java9_v2Lexer import Java9_v2Lexer  # Old slow grammar lexer
# from gen.java9.Java9_v2Parser import Java9_v2Parser  # Old slow grammar parser
# from java9speedy.parser import sa_java9_v2  # Old slow grammar enhanced by CPP backend

from gen.javaLabeled.JavaLexer import JavaLexer  # Java8 grammar efficient lexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled  # Java8 grammar efficient parser labeled

# Import refactorings listeners
from refactorings.encapsulate_field import EncapsulateFiledRefactoringListener  # CodART first refactoring :)
from refactorings.extract_class import ExtractClassRefactoringListener


def main(args):
    # Step 1: Load input source into stream
    stream = FileStream(args.file, encoding='utf8')
    # input_stream = StdinStream()

    # Step 2: Create an instance of AssignmentStLexer
    # lexer = Java9_v2Lexer(stream)  # Deprecated
    lexer = JavaLexer(stream) # Current lexer

    # Step 3: Convert the input source into a list of tokens
    common_token_stream = CommonTokenStream(lexer)

    # Step 4: Create an instance of the AssignmentStParser
    # parser = Java9_v2Parser(common_token_stream)  # Deprecated
    parser = JavaParserLabeled(common_token_stream)  # Current parser
    # parser.getTokenStream()

    # Step 5: Create parse tree
    # 5.1. Python backend --> Low speed
    parse_tree = parser.compilationUnit()

    # 5.2. C++ backend --> high speed
    # parse_tree = sa_java9_v2.parse(stream, 'compilationUnit', None) # Deprecated

    # Step 6: Create an instance of AssignmentStListener
    my_listener = EncapsulateFiledRefactoringListener(common_token_stream=common_token_stream, field_identifier='f')
    # my_listener = ExtractClassRefactoringListener(common_token_stream=token_stream, class_identifier='Worker')

    # return
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open('../../tests/encapsulate_field_tests/input.refactored.java', mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    '''Simple CodART CLI'''
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=r'tests/encapsulate_field_tests/input.java')  # Please use only relative and relevant (e.g. point to tests) path
    args = argparser.parse_args()
    main(args)
