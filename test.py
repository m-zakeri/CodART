"""

The main module of CodART

-changelog
-- Add C++ backend support

"""

version = '0.2.0'
author = 'Morteza'

import argparse
import os

from antlr4 import *

from refactorings.make_method_static import MakeMethodStaticRefactoringListener
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


def main(args):
    x = args.directory
    z = [file for file in os.listdir(x) if '.java' in file]
    for i in range(2):
        for file in z:

            # Step 1: Load input source into stream
            if i == 0:
                stream = FileStream(x + '/' + file, encoding='utf8')
            else:
                stream = FileStream('testproject/refactored/' + '/' + file, encoding='utf8')
            # input_stream = StdinStream()

            # Step 2: Create an instance of AssignmentStLexer
            lexer = JavaLexer(stream)
            # Step 3: Convert the input source into a list of tokens
            token_stream = CommonTokenStream(lexer)
            # Step 4: Create an instance of the AssignmentStParser
            parser = JavaParserLabeled(token_stream)
            tree = parser.compilationUnit()
            # Step 6: Create an instance of AssignmentStListener
            my_listener = MakeMethodStaticRefactoringListener(
                common_token_stream=token_stream,
                target_class='JSONPointer', target_methods=['toURIFragment']
            )

            walker = ParseTreeWalker()
            walker.walk(t=tree, listener=my_listener)
            with open('testproject/refactored/' + file, mode='w+', newline='') as f:
                f.write(my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-d', '--directory',
        help='Input source', default=r'testproject/input/src/main/java/org/json')
    args = argparser.parse_args()
    main(args)