from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from antlr4_java9.Java9Lexer import Java9Lexer
from antlr4_java9.Java9Parser import Java9Parser
from utils_listener import *


def get_program(source_files: list) -> Program:
    program = Program()
    for filename in source_files:
        stream = FileStream(filename, encoding='utf8')
        lexer = Java9Lexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = Java9Parser(token_stream)
        tree = parser.compilationUnit()
        listener = UtilsListener(filename)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        if not listener.package.name in program.packages:
            program.packages[listener.package.name] = listener.package
        else:
            for classes_name in listener.package.classes:
                program.packages[listener.package.name].append(classes_name)

    return program

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

    def apply(self):
        for token_stream in self.token_streams:
            (old_filename, token_stream_rewriter, new_filename) = self.token_streams[token_stream]
            with open(new_filename, mode='w', newline='') as file:
                file.write(token_stream_rewriter.getDefaultText())
