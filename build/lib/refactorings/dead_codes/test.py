"""

The main module of CodART

-changelog
-- Add C++ backend support

"""

__version__ = '0.2.0'
__author__ = 'Morteza'

import argparse
import os
import time

from antlr4 import *

from refactorings.collapse_hierarchy import CollapseHierarchyRefactoringListener
from refactorings.inline_class import InlineClassRefactoringListener
from refactorings.make_method_static import MakeMethodStaticRefactoringListener
from refactorings.make_method_non_static import MakeMethodNonStaticRefactoringListener
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


def main(args):
    input_directory = args.directory
    input_java_files = [file for file in os.listdir(input_directory) if '.java' in file]
    refactoring_id = args.refactor
    source_class_data = None
    target_class = None
    target_class_data = None
    is_complete = False
    print("Process started")
    for i in range(2):
        for file in input_java_files:

            # Step 1: Load input source into stream
            if i == 0:
                stream = FileStream(input_directory + '/' + file, encoding='utf8')
            else:
                stream = FileStream('benchmark_projects/refactored/' + '/' + file, encoding='utf8')
            # input_stream = StdinStream()

            # Step 2: Create an instance of AssignmentStLexer
            lexer = JavaLexer(stream)
            # Step 3: Convert the input source into a list of tokens
            token_stream = CommonTokenStream(lexer)
            # Step 4: Create an instance of the AssignmentStParser
            parser = JavaParserLabeled(token_stream)
            tree = parser.compilationUnit()
            # Step 6: Create an instance of AssignmentStListener
            if refactoring_id == 'c':
                my_listener = CollapseHierarchyRefactoringListener(
                    common_token_stream=token_stream, source_class='JSONStringer',
                    target_class=target_class, source_class_data=source_class_data,
                    target_class_data=target_class_data, is_complete=is_complete
                )

                walker = ParseTreeWalker()
                walker.walk(t=tree, listener=my_listener)
                target_class = my_listener.target_class
                source_class_data = my_listener.source_class_data
                target_class_data = my_listener.target_class_data
                is_complete = my_listener.is_complete
            elif refactoring_id == 'i':
                my_listener = InlineClassRefactoringListener(
                    common_token_stream=token_stream, source_class='HTTPTokener',
                    target_class='JSONTokener', source_class_data=source_class_data,
                    target_class_data=target_class_data, is_complete=is_complete
                )
                walker = ParseTreeWalker()
                walker.walk(t=tree, listener=my_listener)
                target_class = my_listener.target_class
                source_class_data = my_listener.source_class_data
                target_class_data = my_listener.target_class_data
                is_complete = my_listener.is_complete
            elif refactoring_id == 'ms':
                my_listener = MakeMethodStaticRefactoringListener(
                    common_token_stream=token_stream, target_class='JSONPointer',
                    target_methods=['toURIFragment']
                )
                walker = ParseTreeWalker()
                walker.walk(t=tree, listener=my_listener)
            else:
                my_listener = MakeMethodNonStaticRefactoringListener(
                    common_token_stream=token_stream, target_class='JSONPointer',
                    target_methods=['builder']
                )
            with open('benchmark_projects/refactored/' + file, mode='w+', newline='') as f:
                f.write(my_listener.token_stream_rewriter.getDefaultText())
            print("/\\", end='')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-d', '--directory',
        help='Input source', default=r'benchmark_projects/input/src/main/java/org/json')
    argparser.add_argument(
        '-r', '--refactor',
        help='i: inline class & c: collapse hierarchy & ms: make method static & mn: make method non static',
        default='c')
    args = argparser.parse_args()
    start_time = time.time()
    main(args)
    print(f"\n finished in {time.time() - start_time}'s")
