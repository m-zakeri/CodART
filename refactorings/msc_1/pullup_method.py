from antlr4 import *

from antlr4_java9.Java9Lexer import Java9Lexer
from antlr4_java9.Java9Parser import Java9Parser
from utils_listener import UtilsListener, Program
from utils import get_program

def pullup_method(mylist : list):

    program = get_program(mylist)
    extendedclass={}
    methodsofclass=[]
    pullupmethods={}
     #print(program)
    for package_name in program.packages:
        package = program.packages[package_name]
        #print(package)
        for class_name in package.classes:
            _class = package.classes[class_name]
            if _class.superclass_name != None:
             if _class.superclass_name not in extendedclass:
              extendedclass[_class.superclass_name] = [_class]
             else:
               extendedclass[_class.superclass_name].append(_class)
             for key in extendedclass:
                _class1=extendedclass[key]
                for c in _class1:
                 for _method in c.methods:
                    method=c.methods[_method]
                    if method.name not in methodsofclass:
                     methodsofclass.append(method.name)
                    else:
                        pullupmethods[_class.superclass_name]=[method.name]
    return pullupmethods
