from antlr4 import *
from antlr4_java9.Java9Lexer import Java9Lexer
from utils_listener import *

def get_program(source_files: list):
    program = Program()
    for file in list:
     stream = FileStream(file, encoding='utf8')
     lexer = Java9Lexer(stream)
     token_stream = CommonTokenStream(lexer)
     parser = Java9Parser(token_stream)
     tree = parser.compilationUnit()
     listener = UtilsListener()
     walker = ParseTreeWalker()
     walker.walk(listener, tree)
     for class_name in listener.package.classes:
      if not str(listener.package.name) in program.packages:
       program.packages[listener.package.name].classes[class_name] = listener.package.classes[class_name]
      else:
       program.packages[listener.package.name].classes[class_name] = listener.package.classes[class_name].append(listener.package.classes[class_name])
       for p in program.packages:
        _package = program.packages[p]
        print(_package)
        for class_name in _package.classes:
         print(_package.classes[class_name])
     return program
