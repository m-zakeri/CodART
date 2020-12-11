from antlr4 import *
from antlr4_java9.Java9Lexer import Java9Lexer
from utils_listener import UtilsListener, Java9Parser
from utils import get_program


def main():
    # Test
    stream = FileStream("tests/utils_test.java", encoding='utf8')
    lexer = Java9Lexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = Java9Parser(token_stream)
    tree = parser.compilationUnit()
    listener = UtilsListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    print(listener.package)
    for class_name in listener.package.classes:
        _class = listener.package.classes[class_name]
        print(_class)
        for method_name in _class.methods:
            print(_class.methods[method_name])

def testutil():
    mylist = ["tests/utils_test.java"]
    get_program(mylist)
if __name__ == "__main__":
    main()

if __name__ == "__testutil__":
    testutil()