import time
import sys
from pathlib import Path

from antlr4 import FileStream, CommonTokenStream

from gen.java.JavaLexer import JavaLexer
from gen.java.JavaParser import JavaParser


class ProjectParseUsage:
    def __init__(self, project_dir):
        """
        This by calling this class you can measure:
            - Total consumed memory for keeping all parse trees
            - Total consumed time for parsing in seconds
        """
        self.project_root = project_dir
        self.parse_trees = []
        self.counter = 0

    @staticmethod
    def java_explorer(path):
        result = list(Path(path).rglob("*.java"))
        for file_path in result:
            yield file_path.absolute()

    @staticmethod
    def generate_tree(file_path):
        # Step 1: Load input source into stream
        stream = FileStream(file_path, encoding='utf8')
        # Step 2: Create an instance of AssignmentStLexer
        lexer = JavaLexer(stream)
        # Step 3: Convert the input source into a list of tokens
        token_stream = CommonTokenStream(lexer)
        # Step 4: Create an instance of the AssignmentStParser
        parser = JavaParser(token_stream)
        # Step 5: Create parse tree
        parse_tree = parser.compilationUnit()
        return parse_tree

    def run(self):
        print("Parsing...")
        total_time = 0
        generator = self.java_explorer(self.project_root)
        for file_path in generator:
            self.counter += 1
            print(f"Parsing {self.counter}: {file_path}")
            start = time.time()
            tree = self.generate_tree(file_path)
            end = time.time()
            self.parse_trees.append(tree)
            total_time += end - start
        print(f"Execute time is {total_time} seconds.")
        print(f"Memory used for all trees is {sys.getsizeof(self.parse_trees) / 1000} KB")


if __name__ == '__main__':
    project_parse_usage = ProjectParseUsage("E:\\Documents\\University\\Compilers\\Research\\xerces2-j")
    project_parse_usage.run()
