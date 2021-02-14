"""
Main script for grammer javaLabeled

@author: Nader Mesbah
@date: 2020/12/27
"""

from antlr4 import *

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from RefVisitorMigrated import VisitorPatternRefactoringListener

import argparse
from time import time


def main(args):
    # Step 1: Load input source into stream
    begin_time = time()
    stream = FileStream(args.file, encoding='utf8')
    # input_stream = StdinStream()
    print('Input stream:')
    print(stream)

    # Step 2: Create an instance of AssignmentStLexer
    lexer = JavaLexer(stream)
    # Step 3: Convert the input source into a list of tokens
    token_stream = CommonTokenStream(lexer)
    # Step 4: Create an instance of the AssignmentStParser
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    # Step 5: Create parse tree
    parse_tree = parser.compilationUnit()
    # Step 6: Create an instance of the refactoringListener, and send as a parameter the list of tokens to the class
    my_listener = VisitorPatternRefactoringListener(common_token_stream=token_stream,
                                                    SuperClass_identifier='SC',
                                                    SubClass_identifier=['CC1', 'CC2', 'CC3'])
    #                                                    SuperClass_identifier='ComputerPart',
    #                                                    SubClass_identifier=['Keyboard', 'Monitor', 'Mouse', 'Computer'])
    #                                                    SuperClass_identifier='Shape',
    #                                                    SubClass_identifier=['Polygon', 'Rectangle','Arrow'])

    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    print('Compiler result:')
    print(my_listener.token_stream_rewriter.getDefaultText())

    with open('VisitorExample0.refactored.java', mode='w', newline='') as f:
        #   with open('VisitorExample1.refactored.java', mode='w', newline='') as f:
        #    with open('VisitorExample2.refactored.java', mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())

    end_time = time()
    print("time execution : ", end_time - begin_time)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=r'VisitorExample0.java')
    #        help='Input source', default=r'VisitorExample1.java')
    #        help='Input source', default=r'VisitorExample2.java')
    args = argparser.parse_args()
    main(args)
