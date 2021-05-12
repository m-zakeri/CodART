"""
Main script for grammer javaLabeled

@author: Nader Mesbah
@date: 2021/01/08
"""
from time import time

from antlr4 import *

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from RefStrategyMigrated import StrategyPatternRefactoringListener

import argparse


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
    my_listener = StrategyPatternRefactoringListener(common_token_stream=token_stream,
                                                     method_identifier='execute')
    #                                                     method_identifier='read')
    #                                                     method_identifier='write')

    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    print('Compiler result:')
    print(my_listener.token_stream_rewriter.getDefaultText())

    with open('StrategyExample0.refactored.java', mode='w', newline='') as f:
        #    with open('StrategyExample1.refactored.java', mode='w', newline='') as f:
        #    with open('StrategyExample2.refactored.java', mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())

    end_time = time()
    print("execute time : ", end_time - begin_time)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=r'StrategyExample0.java')
    #        help = 'Input source', default = r'StrategyExample1.java')
    #        help = 'Input source', default = r'StrategyExample2.java')
    args = argparser.parse_args()
    main(args)
