from antlr4 import *
from antlr4_java9.Java9Lexer import Java9Lexer
from utils_listener import UtilsListener, Java9Parser
from utils import get_program


def test_utils_listener():
    # Test
    #stream = FileStream("tests/utils_test.java", encoding='utf8')
    stream = FileStream("antlr4_java9/Test.java", encoding='utf8')
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

def test_utils():
    mylist = ["tests/utils_test.java"]
    program = get_program(mylist)
    print(program)
    for package_name in program.packages:
        package = program.packages[package_name]
        print(package)
        for class_name in package.classes:
            _class = package.classes[class_name]
            print(_class)
            for method_name in _class.methods:
                print(_class.methods[method_name])

if __name__ == "__main__":
    #test_utils_listener()
    test_utils()
