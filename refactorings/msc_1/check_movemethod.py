from antlr4 import *

from antlr4_java9.Java9Lexer import Java9Lexer
from antlr4_java9.Java9Parser import Java9Parser
from utils_listener import UtilsListener, Program
from utils import get_program

def move_method():
    mylist = ["tests/utils_test.java"]
    program = get_program(mylist)
    movemethods={}
     #print(program)
    for package_name in program.packages:
        package = program.packages[package_name]
        #print(package)
        for class_name in package.classes:
            _class = package.classes[class_name]
          #  print(_class)
            for method_name in _class.methods:
             method = _class.methods[method_name]
           #  print(_class.methods[method_name])
             for _param in method.parameters:
               if _param[0] in package.classes:
                 if _param[0] not in movemethods:
                  movemethods[str(_param[0])]=[method_name]
                 else:
                     movemethods[str(_param[0])].append(method_name)

    return movemethods



