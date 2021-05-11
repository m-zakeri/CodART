from antlr4 import *

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from Factory import FactoryMethodRefactoringListener

import argparse


def main(args):
    # Step 1: Load input source into stream
    stream = FileStream(args.file, encoding='utf8')
    # input_stream = StdinStream()

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
    my_listener = FactoryMethodRefactoringListener(common_token_stream=token_stream,
                                                   creator_identifier='FactoryMethod',
                                                   products_identifier=['JpegReader', 'GifReader'])
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open('FactoryExample.refactored.java', mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=r'FactoryExample.java')
    args = argparser.parse_args()
    main(args)
