from antlr4 import *

from antlr4_java9.Java9Lexer import Java9Lexer
from antlr4_java9.Java9Parser import Java9Parser
from utils_listener import UtilsListener, Program


def get_program(source_files: list):
    program = Program()
    for file in source_files:
        stream = FileStream(file, encoding='utf8')
        lexer = Java9Lexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = Java9Parser(token_stream)
        tree = parser.compilationUnit()
        listener = UtilsListener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        if not listener.package.name in program.packages:
            program.packages[listener.package.name] = listener.package
        else:
            for classes_name in listener.package.classes:
                program.packages[listener.package.name].append(classes_name)

    return program
