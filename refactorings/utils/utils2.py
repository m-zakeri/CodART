"""

"""
from typing import Dict, Any

from gen.javaLabeled.JavaLexer import JavaLexer

from refactorings.utils.utils_listener_fast import *
from codart.utility.directory_utils import create_project_parse_tree


def get_program(source_files: list, print_status=False) -> Program:
    program = Program()
    for filename in source_files:
        if print_status:
            print("Parsing " + filename)
        stream_ = FileStream(filename, encoding='utf8', errors='ignore')
        lexer_ = JavaLexer(stream_)
        token_stream_ = CommonTokenStream(lexer_)
        parser_ = JavaParser(token_stream_)
        tree_ = parser_.compilationUnit()
        listener_ = UtilsListener(filename)
        walker_ = ParseTreeWalker()
        walker_.walk(listener_, tree_)

        listener_package_name = listener_.package.name or ""

        if not (listener_package_name in program.packages):
            program.packages[listener_package_name] = listener_.package
        else:
            for classes_name in listener_.package.classes:
                program.packages[listener_package_name].classes[classes_name] = listener_.package.classes[classes_name]
    return program


def get_objects(source_files: str) -> Dict[Any, Any]:
    objects = {}
    for filename in source_files:
        stream_ = FileStream(filename, encoding='utf8', errors='ignore')
        lexer_ = JavaLexer(stream_)
        token_stream_ = CommonTokenStream(lexer_)
        parser_ = JavaParser(token_stream_)
        tree_ = parser_.compilationUnit()
        listener_ = UtilsListener(filename)
        walker_ = ParseTreeWalker()
        walker_.walk(listener_, tree_)

        if not (listener_.package.name in objects):
            objects[listener_.package.name] = listener_.objects_declaration
        else:
            for class_name in listener_.objects_declaration:
                objects[listener_.package.name][class_name] = listener_.objects_declaration[class_name]

    return objects


def get_filenames_in_dir(directory_name: str, filter_=lambda x: x.endswith(".java")) -> list:
    result_ = []
    for (dirname, dirnames, filenames) in os.walk(directory_name):
        result_.extend([dirname + '/' + name for name in filenames if filter_(name)])
    return result_


class Rewriter:
    def __init__(self, program: Program, filename_mapping=lambda x: x + ".rewritten.java"):
        self.program = program
        # keys: CommonTokenStream
        # values: (old_filename, TokenStreamRewriter, _new_filename)
        self.token_streams = {}
        for package_name in program.packages:
            package = program.packages[package_name]
            for class_name in package.classes:
                _class: Class = package.classes[class_name]
                token_stream_ = _class.get_token_stream()
                if token_stream_ not in self.token_streams:
                    self.token_streams[token_stream_] = (
                        _class.filename,
                        TokenStreamRewriter(token_stream_),
                        filename_mapping(_class.filename)
                    )

    def get_token_stream_rewriter(self, token_stream: CommonTokenStream) -> TokenStreamRewriter:
        return self.token_streams[token_stream][1]

    def replace(self, tokens_info: TokensInfo, text: str):
        self.get_token_stream_rewriter(tokens_info.token_stream).replaceRange(tokens_info.start, tokens_info.stop, text)

    def insert_after(self, tokens_info: TokensInfo, text: str):
        self.get_token_stream_rewriter(tokens_info.token_stream).insertAfter(tokens_info.stop, text)

    def insert_before(self, tokens_info: TokensInfo, text: str):
        self.get_token_stream_rewriter(tokens_info.token_stream).insertBeforeIndex(tokens_info.stop, text)

    def insert_before_start(self, tokens_info: TokensInfo, text: str):
        self.get_token_stream_rewriter(tokens_info.token_stream).insertBeforeIndex(tokens_info.start, text)

    def insert_after_start(self, tokens_info: TokensInfo, text: str):
        self.get_token_stream_rewriter(tokens_info.token_stream).insertAfter(tokens_info.start, text)

    def apply(self):
        for token_stream in self.token_streams:
            (old_filename, token_stream_rewriter, new_filename) = self.token_streams[token_stream]
            new_filename = new_filename.replace("\\", "/")
            path = new_filename[:new_filename.rfind('/')]
            if not os.path.exists(path):
                os.makedirs(path)
            with open(new_filename, mode='w', encoding='utf-8', newline='') as file:
                file.write(token_stream_rewriter.getDefaultText())


def get_program_with_field_usage(source_files: list, field_name: str, source_class: str, print_status=False) -> Program:
    program = Program()
    for filename in source_files:
        if print_status:
            print("Parsing " + filename)
        stream_ = FileStream(filename, encoding='utf8', errors='ignore')
        lexer_ = JavaLexer(stream_)
        token_stream_ = CommonTokenStream(lexer_)
        parser_ = JavaParser(token_stream_)
        tree_ = parser_.compilationUnit()
        listener_ = StaticFieldUsageListener(filename, field_name, source_class)
        walker_ = ParseTreeWalker()
        walker_.walk(listener_, tree_)

        if not (listener_.package.name in program.packages):
            program.packages[listener_.package.name] = listener_.package
        else:
            for classes_name in listener_.package.classes:
                program.packages[listener_.package.name].classes[classes_name] = listener_.package.classes[classes_name]
    return program


def parse_and_walk(file_path: str, listener_class, has_write=False, debug=False, **kwargs):
    tree_, rewriter = create_project_parse_tree(file_path)
    if has_write:
        if rewriter is None:
            raise Exception("Failed to create rewriter.")
        kwargs.update({'rewriter': rewriter})
    listener_ = listener_class(**kwargs)
    ParseTreeWalker().walk(
        listener_,
        tree_
    )

    if has_write:
        if not debug:
            with open(file_path, mode='w', encoding='utf-8') as f_:
                f_.write(listener_.rewriter.getDefaultText())
        else:
            print(listener_.rewriter.getDefaultText())

    return listener_
