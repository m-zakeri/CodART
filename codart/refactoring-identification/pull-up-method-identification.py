import os
import antlr4
from antlr4 import *
from antlr4.InputStream import InputStream
from codart.gen.JavaLexer import JavaLexer
from codart.gen.JavaParser import JavaParser
from codart.gen.JavaParserVisitor import JavaParserVisitor
from codart.gen.JavaParserLabeled import JavaParserLabeled
from codart.refactorings.rename_method2 import RenameMethodRefactoringListener


# Custom visitor class to extract method names, bodies, and the class they belong to
class MethodBodyVisitor(JavaParserVisitor):
    def __init__(self):
        self.methods = []
        self.current_class = None  # Track the current class

    def visitClassDeclaration(self, ctx):
        """
        Visit class declarations to track the current class.
        """
        self.current_class = ctx.IDENTIFIER().getText()  # Set the current class name
        self.visitChildren(ctx)  # Visit children, i.e., methods in the class
        self.current_class = None  # Reset class name after processing the class

    def visitMethodDeclaration(self, ctx):
        """
        Visit method declarations, extract method names, bodies, and the class they belong to.
        """
        method_name = ctx.IDENTIFIER().getText()
        method_body = ''
        if ctx.methodBody():
            method_body = ctx.methodBody().getText().strip()  # Extract method body

        # Store method with its class name
        self.methods.append((method_name, method_body, self.current_class))
        return self.visitChildren(ctx)


def extract_methods_from_file(file_path):
    """
    Given a Java file, this function will use ANTLR to parse the file and extract method names, bodies, and classes.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    input_stream = InputStream(content)
    lexer = JavaLexer(input_stream)
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(token_stream)

    # Parse the file starting from the compilation unit
    tree = parser.compilationUnit()
    visitor = MethodBodyVisitor()

    # Extract methods using the visitor
    visitor.visit(tree)

    return visitor.methods  # Return the list of methods (name, body, class)


def find_duplicate_methods_in_directory(directory_path):
    """
    Scan all Java files in the given directory and identify duplicate methods with identical bodies.
    """
    method_bodies = {}
    duplicate_methods = []

    # Iterate over all Java files in the directory
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".java"):  # Process only .java files
                file_path = os.path.join(root, file_name)

                # Extract methods from the Java file
                methods = extract_methods_from_file(file_path)

                # Identify duplicate methods
                for method_name, method_body, class_name in methods:
                    # Normalize the body to remove unnecessary spaces or differences
                    normalized_body = method_body.strip()

                    if normalized_body in method_bodies:
                        method_bodies[normalized_body].append((method_name, file_path, class_name))
                    else:
                        method_bodies[normalized_body] = [(method_name, file_path, class_name)]

    # Find methods that have duplicates (more than one entry for the same body)
    for body, method_info in method_bodies.items():
        if len(method_info) > 1:
            original_method = method_info[0]
            for duplicate_method in method_info[1:]:
                duplicate_methods.append((original_method[0], duplicate_method[0], original_method[2], duplicate_method[2]))
    print("Duplicate methods that need renaming:")
    for original_method, duplicate_method, original_class, duplicate_class in duplicate_methods:
        print(f"Original Method: {original_method}, Original Class: {original_class}, "
              f"Duplicate Method: {duplicate_method}, Duplicate Class: {duplicate_class}")

    base_path = directory_path
    package_name = ""
    for original_method, duplicate_method, original_class, duplicate_class in duplicate_methods:
        class_identifiers = [original_class, duplicate_class]
        method_identifiers = [original_method, duplicate_method]
    method_new_name = original_method

    try:
        # Clear existing refactored files
        refactored_path = os.path.join(base_path, "refactored")
        for filename in os.listdir(refactored_path):
            file_path = os.path.join(refactored_path, filename)
            if filename.endswith(".java"):
                os.remove(file_path)

        for filename in os.listdir(base_path):
            if filename.endswith(".java"):
                file_path = os.path.join(base_path, filename)
                print(f"Processing file: {filename}")

                try:
                    with open(file_path, 'r') as file:
                        input_stream = FileStream(file_path)

                    lexer = JavaLexer(input_stream)
                    token_stream = CommonTokenStream(lexer)
                    parser = JavaParserLabeled(token_stream)
                    tree = parser.compilationUnit()

                    listener = RenameMethodRefactoringListener(
                        token_stream, package_name, class_identifiers, method_identifiers, method_new_name
                    )

                    walker = ParseTreeWalker()
                    walker.walk(listener, tree)

                    refactored_file_path = os.path.join(refactored_path, f"{filename.split('.')[0]}_Refactored.java")
                    with open(refactored_file_path, 'w') as refactored_file:
                        refactored_file.write(listener.token_stream_rewriter.getDefaultText())

                except Exception as e:
                    print(f"Error processing file {filename}: {e}")

        print("All files have been processed and refactored.")

    except Exception as e:
        print(f"An error occurred in the main function: {e}")
    return duplicate_methods


# Example usage
directory_path = "C:/Users/98910/Desktop/test"  # Path to your directory with Java files
duplicate_methods = find_duplicate_methods_in_directory(directory_path)
