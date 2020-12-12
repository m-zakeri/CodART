from antlr4 import *

from refactorings.msc_1.antlr4_java9.Java9Lexer import Java9Lexer
from refactorings.msc_1.antlr4_java9.Java9Parser import Java9Parser
from refactorings.msc_1.utils_listener import UtilsListener, Program


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

     if not str(listener.package.name) in program.packages:
      program.packages[str(listener.package.name)]=[listener.package.classes]
     else:
      program.packages[listener.package.name].append(listener.package.classes)
    for p in program.packages:
     _package = program.packages[p]
     print(_package)

    return program
