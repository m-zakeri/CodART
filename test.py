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

from refactorings.collapse_hierarchy import CollapseHierarchyRefactoringListener
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


def main(args):
    x = args.directory
    z = [file for file in os.listdir(x) if '.java' in file]
    source_class_data = None
    target_class = None
    target_class_data = None
    is_complete = False
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
            my_listener = CollapseHierarchyRefactoringListener(
                common_token_stream=token_stream, source_class='JSONPointerException',
                target_class=target_class, source_class_data=source_class_data,
                target_class_data=target_class_data, is_complete=is_complete
            )

            walker = ParseTreeWalker()
            walker.walk(t=tree, listener=my_listener)
            target_class = my_listener.target_class
            source_class_data = my_listener.source_class_data
            target_class_data = my_listener.target_class_data
            is_complete = my_listener.is_complete
            if i == 1:
                a = 10
            with open('testproject/refactored/' + file, mode='w+', newline='') as f:
                f.write(my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-d', '--directory',
        help='Input source', default=r'testproject/input/src/main/java/org/json')
    args = argparser.parse_args()
    main(args)
