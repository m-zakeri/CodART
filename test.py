"""

The main module of CodART

-changelog
-- Add C++ backend support

"""

__version__ = '0.2.0'
__author__ = 'Morteza'


import argparse

from antlr4 import *

from refactorings.make_method_static import MakeMethodStaticRefactoringListener
from gen.java.JavaLexer import JavaLexer
from gen.java.JavaParser import JavaParser



def main(args):
    # Step 1: Load input source into stream
    stream = FileStream(args.file, encoding='utf8')
    # input_stream = StdinStream()

    # Step 2: Create an instance of AssignmentStLexer
    lexer = JavaLexer(stream)
    # Step 3: Convert the input source into a list of tokens
    token_stream = CommonTokenStream(lexer)
    # Step 4: Create an instance of the AssignmentStParser
    parser = JavaParser(token_stream)
    tree = parser.compilationUnit()

    # Step 6: Create an instance of AssignmentStListener
    my_listener = MakeMethodStaticRefactoringListener(
        common_token_stream=token_stream, target_class='A',
        target_methods=['printF', 'printH']
    )

    walker = ParseTreeWalker()
    walker.walk(t=tree, listener=my_listener)

    with open('input.refactored.java', mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=r'./input.java')
    args = argparser.parse_args()
    main(args)