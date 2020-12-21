from antlr4 import *
from antlr4_java9.Java9Lexer import Java9Lexer
from utils_listener import UtilsListener, Java9Parser
from utils import get_program
from move_method import move_method
from pullup_method import pullup_method


def test_utils_listener():
    # Test
    filename = "tests/utils_test.java"
    stream = FileStream(filename, encoding='utf8')
    lexer = Java9Lexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = Java9Parser(token_stream)
    tree = parser.compilationUnit()
    listener = UtilsListener(filename)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    print(listener.package)
    for class_name in listener.package.classes:
        _class = listener.package.classes[class_name]
        print(_class)
        for field_name in _class.fields:
            print(_class.fields[field_name])
        for method_name in _class.methods:
            print(_class.methods[method_name])

def test_utils():
    mylist = ["tests/utils_test.java"]
    movemethods = move_method(mylist)
    program = get_program(mylist)
    print(program)
    for package_name in program.packages:
        package = program.packages[package_name]
        print(package)
        for class_name in package.classes:
            _class = package.classes[class_name]
            print(_class)
            for method_name in _class.methods:
                method = _class.methods[method_name]
                print(_class.methods[method_name])
                for _param in method.parameters:
                 print(_param[0])
    for key in movemethods:
        n=movemethods[key]
        print("......")
        print(key)
        print(n)

def pullup_methods():
    mylist = ["tests/utils_test.java"]
    pullupmethods=pullup_method(mylist)
    for key in pullupmethods:
      print(key)
      print(pullupmethods[key])

if __name__ == "__main__":
    #test_utils_listener()
    #test_utils()
    pullup_methods()
