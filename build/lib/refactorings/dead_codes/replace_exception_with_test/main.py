import os


import argparse


from refactorings.dead_codes.replace_exception_with_test import \
    ReplaceExceptionWithTestClassRefactoringListener
from gen.javaLabeled.JavaLexer import *
from gen.javaLabeled.JavaParserLabeled import *

directory = 'E:/git/CodART/benchmark_projects/input/src/main/java/org/json/CDL.java'


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

    print("=====Enter Create ParseTree=====")
    # Step 5: Create parse tree
    parse_tree = parser.compilationUnit()
    print("=====Create ParseTree Finished=====")

    # Step 6: Create an instance of AssignmentStListener
    my_listener = ReplaceExceptionWithTestClassRefactoringListener(common_token_stream=token_stream,
                                                                   class_identifier='CDL', filename=args.file)

    # return
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open('input.refactored.java', mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())


def process_file(file):
    argparser = argparse.ArgumentParser()
    # argparser.add_argument(
    #     '-n', '--file',
    #     help='Input source', default=r'refactorings/test/test3.java')
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=file)
    args = argparser.parse_args()
    main(args)


if __name__ == '__main__':
    for dirname, dirs, files in os.walk(directory):
        for file in files:
            name, extension = os.path.splitext(file)
            if extension == '.java':
                process_file("{}/{}".format(dirname, file))
