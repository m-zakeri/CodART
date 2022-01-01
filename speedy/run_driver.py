"""
Benchmark driver for CodeART C++ backend

"""


__version__ = '0.4.0'
__author__ = 'Morteza'

import antlr4
import java8speedy
from java8speedy.parser import sa_javalabeled
from java8speedy.benchmark import benchmark



if __name__ == '__main__':
    if sa_javalabeled.USE_CPP_IMPLEMENTATION:
        print("JAVA 8 Using C++ implementation of parser")
    else:
        print("Using Python implementation of parser")

    file_stream = antlr4.FileStream('../tests/utils_test2.java')
    file_stream = antlr4.FileStream('Test_WekaPackageManager.java')
    sa_javalabeled._cpp_parse(file_stream, 'compilationUnit')

    # java9speedy.print_tree('../refactorings/input.java')
    # java9speedy.benchmark('../refactorings/input.java', 1000)
    # java9speedy.print_tree('Test_WekaPackageManager.java')

    benchmark('Test_WekaPackageManager.java', 5)
    # benchmark('../tests/utils_test2.java')
