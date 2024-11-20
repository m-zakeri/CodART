import os
import antlr4
from antlr4.InputStream import InputStream
from codart.gen.JavaLexer import JavaLexer
from codart.gen.JavaParser import JavaParser
from codart.gen.JavaParserVisitor import JavaParserVisitor
from codart.refactorings.rename_method2 import main


# Visitor class to extract method names, bodies, and the class they belong to
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


# Visitor class to extract fields from classes
class FieldVisitor(JavaParserVisitor):
    def __init__(self):
        self.fields = []  # List to store field details
        self.current_class = None  # Track the current class name

    def visitClassDeclaration(self, ctx):
        """
        Visit class declarations to track the current class.
        """
        self.current_class = ctx.IDENTIFIER().getText()  # Set the current class name
        self.visitChildren(ctx)  # Process fields in the class
        self.current_class = None  # Reset class name after leaving the class

    def visitFieldDeclaration(self, ctx):
        """
        Visit field declarations and extract field information.
        """
        field_type = ctx.typeType().getText()  # Get the field type
        variable_declarators = ctx.variableDeclarators().variableDeclarator()
        for declarator in variable_declarators:
            field_name = declarator.variableDeclaratorId().getText()  # Get the field name
            self.fields.append((field_type, field_name, self.current_class))
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


def extract_fields_from_file(file_path):
    """
    Parse a Java file to extract field declarations.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    input_stream = InputStream(content)
    lexer = JavaLexer(input_stream)
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(token_stream)

    # Parse the file starting from the compilation unit
    tree = parser.compilationUnit()
    visitor = FieldVisitor()

    # Extract fields using the visitor
    visitor.visit(tree)

    return visitor.fields


def extract_package_name(file_path):
    """
    Extract the package name from a Java file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith("package "):
                return line[len("package "):].strip(";")
    return None  # No package declaration found


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
            # original_name, original_path, original_class = original_method
            # original_package = extract_package_name(original_path)  # Extract package name

            for duplicate_method in method_info[1:]:
                duplicate_methods.append(
                    (original_method[0], duplicate_method[0], original_method[2], duplicate_method[2]))
            print("Duplicate methods that need renaming:")
            for original_method, duplicate_method, original_class, duplicate_class in duplicate_methods:
                print(f"Original Method: {original_method}, Original Class: {original_class}, "
                      f"Duplicate Method: {duplicate_method}, Duplicate Class: {duplicate_class}")

            base_path = directory_path
            package_name = ""
            for original_method, duplicate_method, original_class, duplicate_class in duplicate_methods:
                class_identifier = original_class, duplicate_class
                method_identifier = original_method, duplicate_method
                method_new_name = original_method
                # Rename duplicate method using `RenameMethodRefactoringListener`
                try:
                    print(f"Renaming duplicate method '{method_identifier}' in class '{class_identifier}' "
                          f"to '{method_new_name}' (Package: {package_name})")
                    # Call the main function to perform renaming
                    refactored_path = os.path.join(base_path, "refactored")
                    os.makedirs(refactored_path, exist_ok=True)  # Ensure refactored folder exists

                    # Dynamically set parameters and call refactoring logic

                    main(base_path=directory_path, package_name=package_name, class_identifier=class_identifier,
                                method_identifier=method_identifier, method_new_name=method_new_name)
                except Exception as e:
                    print(f"Error renaming method {method_identifier}: {e}")

    return duplicate_methods


def find_duplicate_fields_in_directory(directory_path):
    """
    Scan all Java files in the given directory to identify duplicate fields across classes.
    """
    field_signatures = {}  # Map to track field signatures and associated classes
    duplicate_fields = []  # List to store duplicated fields

    # Traverse the directory and process each Java file
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".java"):  # Process only Java files
                file_path = os.path.join(root, file_name)

                # Extract fields from the Java file
                fields = extract_fields_from_file(file_path)

                # Check for duplicate fields
                for field_type, field_name, class_name in fields:
                    signature = f"{field_type} {field_name}"  # Create a unique signature for each field
                    if signature in field_signatures:
                        field_signatures[signature].append(class_name)  # Add the class to the signature
                    else:
                        field_signatures[signature] = [class_name]

    # Identify duplicated fields that exist in more than one class
    for signature, classes in field_signatures.items():
        if len(classes) > 1:
            duplicate_fields.append((signature, classes))

    # Call refactoring method for each duplicated field
    for signature, classes in duplicate_fields:
        pullUpFieldRefactoring(signature, classes)

    return duplicate_fields


def pullUpFieldRefactoring(field_signature, classes):
    """
    Perform refactoring to pull up a duplicated field to a common superclass.
    """
    print(f"Refactoring field '{field_signature}' from classes: {', '.join(classes)} to a common superclass.")
    # Add your actual refactoring logic here


# Main function
if __name__ == "__main__":
    directory_path = "C:/Users/98910/Desktop/test"  # Path to your directory with Java files

    # Find and refactor duplicate methods
    duplicate_methods = find_duplicate_methods_in_directory(directory_path)
    print("Duplicate Methods:")
    for original, duplicate, original_class, duplicate_class in duplicate_methods:
        print(f"Method: {original} (Class: {original_class}) is duplicated as {duplicate} (Class: {duplicate_class})")

    # Find and refactor duplicate fields
    duplicate_fields = find_duplicate_fields_in_directory(directory_path)
    print("Duplicate Fields:")
    for signature, classes in duplicate_fields:
        print(f"Field: {signature} is duplicated in classes: {', '.join(classes)}")
