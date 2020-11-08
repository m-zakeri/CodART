"""
Main script for grammer Java9_v2 (version 2)

@author: Morteza Zakeri, (http://webpages.iust.ac.ir/morteza_zakeri/)
@date: 20201107

- Compiler generator:   ANTRL4.x
- Target language(s):   Python3.x,


-Changelog:
-- v4.2
--- Add name for grammar rules extensions
--- Remove Java attributes from grammar file.

- Course website:   http://parsa.iust.ac.ir/courses/compilers/
- Laboratory website:   http://reverse.iust.ac.ir/

"""

__version__ = '0.1.0'
__author__ = 'Morteza'

from antlr4 import *

from code.java9_v2.gen.Java9_v2Lexer import Java9_v2Lexer
from code.java9_v2.gen.Java9_v2Parser import Java9_v2Parser
from code.java9_v2.refactors import EncapsulateFiledRefactoringListener

import argparse


def main(args):
    # Step 1: Load input source into stream
    stream = FileStream(args.file, encoding='utf8')
    # input_stream = StdinStream()
    print('Input stream:')
    print(stream)


    # Step 2: Create an instance of AssignmentStLexer
    lexer = Java9_v2Lexer(stream)
    # Step 3: Convert the input source into a list of tokens
    token_stream = CommonTokenStream(lexer)
    # Step 4: Create an instance of the AssignmentStParser
    parser = Java9_v2Parser(token_stream)
    parser.getTokenStream()
    # Step 5: Create parse tree
    parse_tree = parser.compilationUnit()
    # Step 6: Create an instance of AssignmentStListener
    my_listener = EncapsulateFiledRefactoringListener(common_token_stream=token_stream, field_identifier='f')
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    print('Compiler result:')
    print(my_listener.token_stream_rewriter.getDefaultText())

    with open('A.refactored.java', mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())




if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=r'A.java')
    args = argparser.parse_args()
    main(args)
