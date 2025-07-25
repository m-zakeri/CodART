import os
import antlr4
from antlr4.InputStream import InputStream
from codart.gen.JavaLexer import JavaLexer
from codart.gen.JavaParser import JavaParser
from codart.gen.JavaParserVisitor import JavaParserVisitor
from codart.refactorings.rename_method2 import main
from codart.refactorings.pullup_method import main as pull_up_method
from pull_up_field_identification import find_duplicate_fields_in_directory


# Visitor class to extract method names, bodies, and the class and package they belong to
class MethodBodyVisitor(JavaParserVisitor):
    def __init__(self):
        self.methods = []
        self.current_class = None  # Track the current class
        self.current_package = None  # Track the current package

    def visitPackageDeclaration(self, ctx):
        """
        Visit package declarations to track the current package.
        """
        self.current_package = ctx.qualifiedName().getText() or "default"  # Extract the package name
        return self.visitChildren(ctx)

    def visitClassDeclaration(self, ctx):
        """
        Visit class declarations to track the current class.
        """
        self.current_class = ctx.IDENTIFIER().getText()  # Set the current class name
        self.visitChildren(ctx)  # Visit children, i.e., methods in the class
        self.current_class = None  # Reset class name after processing the class

    def visitMethodDeclaration(self, ctx):
        """
        Visit method declarations, extract method names, bodies, and the class and package they belong to.
        """
        method_name = ctx.IDENTIFIER().getText()
        method_body = ''
        if ctx.methodBody():
            method_body = ctx.methodBody().getText().strip()  # Extract method body

        # Store method with its class and package name
        self.methods.append((method_name, method_body, self.current_class, self.current_package))
        return self.visitChildren(ctx)


def extract_methods(file_path):
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

    return visitor.methods  # Return the list of methods (name, body, class, package)


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
                methods = extract_methods(file_path)

                # Identify duplicate methods
                for method_name, method_body, class_name, package_name in methods:
                    # Normalize the body to remove unnecessary spaces or differences
                    normalized_body = method_body.strip()

                    if normalized_body in method_bodies:
                        method_bodies[normalized_body].append((method_name, file_path, class_name, package_name))
                    else:
                        method_bodies[normalized_body] = [(method_name, file_path, class_name, package_name)]

    # Find methods that have duplicates (more than one entry for the same body)
    for body, method_info in method_bodies.items():
        if len(method_info) > 1:
            original_method = method_info[0]

            for duplicate_method in method_info[1:]:
                duplicate_methods.append(
                    (original_method[0], duplicate_method[0], original_method[2], duplicate_method[2],
                     original_method[3], duplicate_method[3]))

            print("Duplicate methods that need renaming:")
            for (original_method, duplicate_method, original_class,
                 duplicate_class, original_package, duplicate_package) in duplicate_methods:
                print(f"Original Method: {original_method} (Class: {original_class}, Package: {original_package}), "
                      f"Duplicate Method: {duplicate_method} (Class: {duplicate_class}, Package: {duplicate_package})")

            for (original_method, duplicate_method, original_class,
                 duplicate_class, original_package, duplicate_package) in duplicate_methods:
                class_identifier = (original_class, duplicate_class)
                method_identifier = (original_method, duplicate_method)
                method_new_name = original_method  # Define your new naming convention as needed

                try:
                    print(f"Renaming duplicate method '{method_identifier}' in class '{class_identifier}' "
                          f"to '{method_new_name}'")
                    # Call the main function to perform renaming
                    refactored_path = os.path.join(directory_path, "refactored")
                    os.makedirs(refactored_path, exist_ok=True)  # Ensure refactored folder exists

                    main(base_path=directory_path, package_name=duplicate_package,
                         class_identifier=class_identifier, method_identifier=method_identifier,
                         method_new_name=method_new_name)

                    # Now call find_duplicate_fields_in_directory after renaming methods
                    print(f"Renaming done. Now scanning for duplicate fields in '{refactored_path}'")
                    find_duplicate_fields_in_directory(refactored_path)

                    # Call the pull_up_method function after renaming and pull_up_field
                    print(f"Running pull up method:")
                    udb_path = "C:/Users/98910/Desktop/test/refactored/refactored/refactored.und"
                    children_classes = [original_class, duplicate_class]
                    print(f"Pulling up method '{method_new_name}' from class '{class_identifier}'")
                    pull_up_method(udb_path=udb_path, children_classes=children_classes,
                                   method_name=method_new_name)

                except Exception as e:
                    print(f"Error renaming method {method_identifier}: {e}")

    return duplicate_methods


# Main function
if __name__ == "__main__":
    path = "C:/Users/98910/Desktop/test"  # Path to your directory with Java files
    # Find and refactor duplicate methods
    duplicated_methods = find_duplicate_methods_in_directory(path)
