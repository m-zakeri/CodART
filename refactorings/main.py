import argparse

from antlr4 import *

from refactorings.encapsulate_field import EncapsulateFiledRefactoringListener
# from refactorings.extract_class import ExtractClassRefactoringListener
from refactorings.move_method import MoveMethodRefactoringListener
from refactorings.gen.Java9_v2Lexer import Java9_v2Lexer
from refactorings.gen.Java9_v2Parser import Java9_v2Parser


def main(args):
    # Step 1: Load input source into stream
    stream = FileStream(args.file, encoding='utf8')
    # input_stream = StdinStream()

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
    # my_listener = ExtractClassRefactoringListener(common_token_stream=token_stream, class_identifier='A')
    my_listener = MoveMethodRefactoringListener(common_token_stream=token_stream, source_class_identifier='A',
                                                target_class_identifier='B', method_identifier='printG')
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open('input.refactored.java', mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=r'input.java')
    args = argparser.parse_args()
    main(args)
