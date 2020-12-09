from antlr4 import *
from antlr4_java9.Java9Lexer import Java9Lexer
from utils_listener import UtilsListener, Java9Parser

def main():
    # Test
    stream = FileStream("antlr4_java9/Test.java", encoding='utf8')
    lexer = Java9Lexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = Java9Parser(token_stream)
    tree = parser.compilationUnit()
    listener = UtilsListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

if __name__ == "__main__":
    main()
