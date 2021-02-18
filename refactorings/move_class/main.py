import argparse
import os

from gen.javaLabeled.JavaLexer import *
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from refactorings.move_class import MoveClassRefactoringListener, ReplaceDependentObjectsListener

filename = 'A.java'
class_identifier = 'A'
source_package = 'a.aa'
target_package = 'c'

f_iteration_flag = False
directory = '../../src'
file_counter = 0


def main(args):
    global f_iteration_flag

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
    # Step 6: Create an instance of AssignmentStListener
    if f_iteration_flag:
        my_listener = MoveClassRefactoringListener(
            common_token_stream=token_stream, source_package=source_package, target_package=target_package,
            class_identifier=class_identifier, filename=args.file, dirname=directory
        )
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        with open(args.file, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText().replace("\r", ""))

    else:
        has_import = False
        has_exact_import = False

        file_to_check = open(file=args.file, mode='r')
        for line in file_to_check.readlines():
            text_line = line.replace('\n', '').replace('\r', '').strip()
            if text_line.startswith('import') and text_line.endswith(source_package + '.' + class_identifier + ';'):
                has_import = True
                break
            if text_line.startswith('import') and text_line.endswith(target_package + '.' + class_identifier + ';'):
                has_exact_import = True
                break

        if not has_exact_import:
            print(f"Start checking file \"{file_to_check.name}\" *** {file_counter}/100")

            my_listener = ReplaceDependentObjectsListener(
                common_token_stream=token_stream, source_package=source_package, target_package=target_package,
                class_identifier=class_identifier, filename=args.file, has_import=has_import
            )
            walker = ParseTreeWalker()
            walker.walk(t=parse_tree, listener=my_listener)

            with open(args.file, mode='w', newline='') as f:
                f.write(my_listener.token_stream_rewriter.getDefaultText().replace("\r", ""))

            print(f"Finish checking file \"{file_to_check.name}\" *** {file_counter}/100")


def recursive_walk(dir):
    global f_iteration_flag, filename
    f_iteration_flag = True

    filename_without_extension, extension = os.path.splitext(filename)
    if extension == '.java':
        process_file("{}/{}".format(dir + '/' + source_package.replace('.', '/'), filename))
    else:
        raise ValueError(f"The filename format must be \".java\", but found {extension}!")

    f_iteration_flag = False

    for dirname, dirs, files in os.walk(dir):
        for file in files:
            if file == filename or file == class_identifier + '.java':
                continue
            file_without_extension, extension = os.path.splitext(file)
            if extension == '.java':
                process_file("{}/{}".format(dirname, file))


def process_file(file):
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=file)

    args = argparser.parse_args()
    main(args)


if __name__ == '__main__':
    if not os.path.exists(directory + '/' + source_package.replace('.', '/')):
        raise NotADirectoryError(f"The package \"{source_package}\" NOT FOUND!")

    if not os.path.exists(directory + '/' + target_package.replace('.', '/')):
        raise NotADirectoryError(f"The package \"{target_package}\" NOT FOUND!")

    if not os.path.isfile(directory + '/' + source_package.replace('.', '/') + '/' + filename):
        raise FileNotFoundError(f"The file \"{filename}\" NOT FOUND in package {source_package}!")

    if os.path.isfile(directory + '/' + target_package.replace('.', '/') + '/' + class_identifier + '.java'):
        print(f"[Redundant]: doesn't need to refactor")
        print(f"The class \"{class_identifier}\" already exists in package \"{target_package}\"!")
        exit(0)

    recursive_walk(directory)
