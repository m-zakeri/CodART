"""
Benchmark driver for CodeART C++ backend

"""


__version__ = '0.2.0'
__author__ = 'Morteza'


import java9speedy
from java9speedy.parser import sa_java9_v2

# java9speedy.print_tree('../refactorings/input.java')
# java9speedy.benchmark('../refactorings/input.java', 1000)
# java9speedy.print_tree('Test_WekaPackageManager.java')
java9speedy.benchmark('../grammars/Test.java', 1)

if sa_java9_v2.USE_CPP_IMPLEMENTATION:
    print("JAVA 9 Using C++ implementation of parser")
else:
    print("Using Python implementation of parser")
