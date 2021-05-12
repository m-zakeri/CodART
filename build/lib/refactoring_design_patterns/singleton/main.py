from antlr4 import *
import os
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from Singleton import SingletonRefactoringListener
import argparse
import time
from shutil import copy2


def main(args, i):
    # Step 1: Load input source into stream
    stream = FileStream(args.file, encoding='utf8')
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
    # my_listener = EncapsulateFiledRefactoringListener(common_token_stream=token_stream, class_identifier='A')
    my_listener = SingletonRefactoringListener(common_token_stream=token_stream, class_identifier='GeneralPurposeBit')
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    newpath = "Refactored" + args.file
    if not os.path.exists(os.path.dirname(newpath)):
        try:
            os.makedirs(os.path.dirname(newpath))
        except OSError as exc:  # Guard against race condition
            pass
    with open(newpath, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    start_time = time.time()
    ProgramPath = r"."
    i = 0
    for root, d, f in os.walk(ProgramPath):
        for file in f:
            if file.endswith(".java"):
                try:
                    FilePath = os.path.join(root, file)
                    print("Success: ", FilePath)
                    argparser = argparse.ArgumentParser()
                    argparser.add_argument(
                        '-n', '--file', default=FilePath)
                    args = argparser.parse_args()
                    main(args, i)
                except:
                    print("Error: ", os.path.join(root, file))
            else:
                FilePath = os.path.join(root, file)
                NewFilePath = "Refactored" + root
                if not os.path.exists(NewFilePath):
                    os.makedirs(NewFilePath)

                copy2(FilePath, NewFilePath)

    print("--- %s seconds ---" % (time.time() - start_time))
