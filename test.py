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
    for i in range(3):
        for file in z:

            # Step 1: Load input source into stream
            stream = FileStream(x+'/'+file, encoding='utf8')
            # input_stream = StdinStream()

            # Step 2: Create an instance of AssignmentStLexer
            lexer = JavaLexer(stream)
            # Step 3: Convert the input source into a list of tokens
            token_stream = CommonTokenStream(lexer)
            # Step 4: Create an instance of the AssignmentStParser
            parser = JavaParserLabeled(token_stream)
            tree = parser.compilationUnit()
            if file == 'JSONPointer.java':
                a = 10
            # Step 6: Create an instance of AssignmentStListener
            my_listener = CollapseHierarchyRefactoringListener(
                common_token_stream=token_stream, source_class='JSONPointerException',
                target_class=target_class, source_class_data=source_class_data,
                target_class_data=target_class_data
            )

            walker = ParseTreeWalker()
            walker.walk(t=tree, listener=my_listener)
            target_class = my_listener.target_class
            source_class_data = my_listener.source_class_data
            target_class_data = my_listener.target_class_data

            with open('testproject/refactored/'+file, mode='w+', newline='') as f:
                f.write(my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-d', '--directory',
        help='Input source', default=r'testproject/input/src/main/java/org/json')
    args = argparser.parse_args()
    main(args)
