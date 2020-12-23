from antlr4 import *
from antlr4_java9.Java9Lexer import Java9Lexer
from utils_listener import UtilsListener, Java9Parser

from refactorings.msc_1.pullup_method1 import pullup_method
from refactorings.msc_1.tests.move_method.move_method1 import move_method
from utils import get_program


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
    mylist = ["tests/pullup_method/Test.java", "tests/pullup_method/sourceclass.java",
              "tests/pullup_method/superclass.java"]
    pullupmethods=pullup_method(mylist,"tests.utils_test2","superclass","b","sourceclass")
    for key in pullupmethods:
      print(key)
      print(pullupmethods[key])
def test():
    source_filenames = ["tests/move_method_test/source.java", "tests/move_method_test/target.java"]
    program = get_program(source_filenames)
    print(program.packages["tests.utils_test2"].classes["source"].methods["c"].get_text_from_file())

if __name__ == "__main__":
    #test_utils_listener()
    #test_utils()
    pullup_methods()
  #  test()
