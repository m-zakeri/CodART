import argparse
import os

from refactorings.extract_class.extract_class import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled

source_class = 'A'
new_class = 'ANew'
moved_fields = ['h']
moved_methods = ['printH']

f_iteration_flag = False
source_class_dirname = ''


def main(args):
    global f_iteration_flag
    global source_class, new_class, source_class_dirname

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
        recognizer_listener = ExtractClassRecognizerListener(common_token_stream=token_stream, class_identifier=source_class)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=recognizer_listener)

        component = sorted(moved_methods + moved_fields)
        if component in sorted(recognizer_listener.connected_components):
            my_listener = ExtractClassRefactoringListener(
                common_token_stream=token_stream, source_class=source_class, new_class=new_class,
                moved_methods=moved_methods, moved_fields=moved_fields, filename=args.file
            )
            walker.walk(t=parse_tree, listener=my_listener)

            with open(args.file, mode='w', newline='') as f:
                f.write(my_listener.token_stream_rewriter.getDefaultText())
        else:
            print(recognizer_listener.connected_components)
            raise ValueError("Can not refactor!")
    else:
        check_dirname = False
        dirname = '/'.join(args.file.split('/')[:-1])

        if dirname == source_class_dirname:
            if dirname + '/' + source_class + '.java' != args.file and\
                    dirname + '/' + new_class + '.java' != args.file:
                check_dirname = True
        else:
            file_to_check = open(file=args.file, mode='r')
            for line in file_to_check.readlines():
                text_line = line.replace('\n', '').replace('\r', '').strip()
                if text_line.startswith('import') and text_line.endswith('.' + source_class + ';'):
                    check_dirname = True
                    break

        if check_dirname:
            my_listener = ReplaceDependentObjectsListener(
                common_token_stream=token_stream, source_class=source_class, new_class=new_class,
                moved_methods=moved_methods, moved_fields=moved_fields, filename=args.file
            )
            walker = ParseTreeWalker()
            walker.walk(t=parse_tree, listener=my_listener)


def recursive_walk(directory):
    global f_iteration_flag, source_class_dirname
    for dirname, dirs, files in os.walk(directory):
        for filename in files:
            if filename != source_class + '.java':
                continue
            f_iteration_flag = True
            source_class_dirname = dirname

            filename_without_extension, extension = os.path.splitext(filename)
            if extension == '.java':
                process_file("{}/{}".format(dirname, filename))

    f_iteration_flag = False

    for dirname, dirs, files in os.walk(directory):
        for filename in files:
            filename_without_extension, extension = os.path.splitext(filename)
            if extension == '.java':
                process_file("{}/{}".format(dirname, filename))


def process_file(file):
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=file)

    args = argparser.parse_args()
    main(args)


if __name__ == '__main__':
    directory = '/home/ali/Documents/dev/CodART/'
    recursive_walk(directory)
