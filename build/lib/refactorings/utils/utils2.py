import os

from antlr4 import FileStream, ParseTreeWalker
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.java.JavaLexer import JavaLexer
from refactorings.utils.utils_listener_fast import *


def get_program(source_files: list, print_status = False) -> Program:
    program = Program()
    for filename in source_files:
        if print_status:
            print("Parsing " + filename)
        stream = FileStream(filename, encoding='utf8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParser(token_stream)
        tree = parser.compilationUnit()
        listener = UtilsListener(filename)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        if not listener.package.name in program.packages:
            program.packages[listener.package.name] = listener.package
        else:
            for classes_name in listener.package.classes:
                program.packages[listener.package.name].classes[classes_name]=listener.package.classes[classes_name]

    return program

def get_filenames_in_dir(directory_name: str, filter = lambda x: x.endswith(".java")) -> list:
    result = []
    for (dirname, dirnames, filenames) in os.walk(directory_name):
        result.extend([dirname + '/' + name for name in filenames if filter(name)])
    return result

class Rewriter:
    def __init__(self, program: Program, filename_mapping = lambda x: x + ".rewritten.java"):
        self.program = program
        # keys: CommonTokenStream
        # values: (old_filename, TokenStreamRewriter, _new_filename)
        self.token_streams = {}
        for package_name in program.packages:
            package = program.packages[package_name]
            for class_name in package.classes:
                _class: Class = package.classes[class_name]
                token_stream = _class.get_token_stream()
                if token_stream not in self.token_streams:
                    self.token_streams[token_stream] = (
                        _class.filename,
                        TokenStreamRewriter(token_stream),
                        filename_mapping(_class.filename)
                    )

    def get_token_stream_rewriter(self, token_stream: CommonTokenStream) -> TokenStreamRewriter:
        return self.token_streams[token_stream][1]

    def replace(self, tokens_info: TokensInfo, text: str):
        self.get_token_stream_rewriter(tokens_info.token_stream).replaceRange(tokens_info.start, tokens_info.stop, text)

    def insert_after(self, tokens_info: TokensInfo, text: str):
        self.get_token_stream_rewriter(tokens_info.token_stream).insertAfter(tokens_info.stop, text)

    def insert_before(self, tokens_info: TokensInfo, text: str):
        self.get_token_stream_rewriter(tokens_info.token_stream).insertBeforeIndex(tokens_info.stop,text)

    def insert_before_start(self, tokens_info: TokensInfo, text: str):
        self.get_token_stream_rewriter(tokens_info.token_stream).insertBeforeIndex(tokens_info.start,text)

    def insert_after_start(self, tokens_info: TokensInfo, text: str):
        self.get_token_stream_rewriter(tokens_info.token_stream).insertAfter(tokens_info.start, text)
    def apply(self):
        for token_stream in self.token_streams:
            (old_filename, token_stream_rewriter, new_filename) = self.token_streams[token_stream]
            new_filename = new_filename.replace("\\", "/")
            path = new_filename[:new_filename.rfind('/')]
            if not os.path.exists(path):
                os.makedirs(path)
            with open(new_filename, mode='w', newline='') as file:
                file.write(token_stream_rewriter.getDefaultText())
