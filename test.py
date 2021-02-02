"""

The main module of CodART

-changelog
-- Add C++ backend support

"""

__version__ = '0.2.0'
__author__ = 'Morteza'


import argparse
import os

from antlr4 import *

from refactorings.inline_class import InlineClassRefactoringListener
from gen.java.JavaLexer import JavaLexer
from gen.java.JavaParser import JavaParser



def main(args):
    input1_className = input()
    input2_className = input()
    x = args.directory
    z = [file for file in os.listdir(x) if '.java' in file]
    for file in z:
        # Step 1: Load input source into stream
        stream = FileStream(x + '/' + file, encoding='utf8')
        # input_stream = StdinStream()

        # Step 2: Create an instance of AssignmentStLexer
        lexer = JavaLexer(stream)
        # Step 3: Convert the input source into a list of tokens
        token_stream = CommonTokenStream(lexer)
        # Step 4: Create an instance of the AssignmentStParser
        parser = JavaParser(token_stream)
        tree = parser.compilationUnit()


    my_listener = InlineClassRefactoringListener(
        common_token_stream=token_stream, source_class=input1_className, target_class=input2_className
    )

    walker = ParseTreeWalker()
    walker.walk(t=tree, listener=my_listener)

    with open('input.refactored.java', mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-d', '--directory',
        help='Input source', default=r'testproject/input/src/main/java/org/json')
    args = argparser.parse_args()
    main(args)
