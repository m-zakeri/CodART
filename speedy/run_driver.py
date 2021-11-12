"""
Benchmark driver for CodeART C++ backend

"""


__version__ = '0.3.0'
__author__ = 'Morteza'


import java8speedy
from java8speedy.parser import sa_java
from java8speedy.benchmark import benchmark
import antlr4
# file_stream_ = antlr4.FileStream('../tests/utils_test2.java')
# sa_java._cpp_parse(file_stream_, 'compilationUnit')


# quit()

# java9speedy.print_tree('../refactorings/input.java')
# java9speedy.benchmark('../refactorings/input.java', 1000)
# java9speedy.print_tree('Test_WekaPackageManager.java')
# benchmark('Test_WekaPackageManager.java', 1)
benchmark('../tests/utils_test2.java')

if sa_java.USE_CPP_IMPLEMENTATION:
    print("JAVA 8 Using C++ implementation of parser")
else:
    print("Using Python implementation of parser")
