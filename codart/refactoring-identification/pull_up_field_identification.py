import os
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.InputStream import InputStream
from codart.gen.JavaParserListener import JavaParserListener
from codart.gen.JavaParserVisitor import JavaParserVisitor
from codart.gen.JavaLexer import JavaLexer
from codart.gen.JavaParser import JavaParser
from codart.refactorings.pullup_field import main as pull_up_field


class PackageExtractor(JavaParserListener):
    def __init__(self):
        self.package_name = None

    def enterPackageDeclaration(self, ctx):
        """
        Capture the package declaration from the parse tree.
        """
        self.package_name = ctx.qualifiedName().getText()


def extract_packages(directory_path):
    """
    Extract package declarations from all Java files in the directory.
    Returns a dictionary mapping file paths to their package names.
    """
    package_map = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                try:
                    # Parse the Java file
                    input_stream = FileStream(file_path, encoding="utf-8")
                    lexer = JavaLexer(input_stream)
                    token_stream = CommonTokenStream(lexer)
                    parser = JavaParser(token_stream)
                    tree = parser.compilationUnit()

                    # Walk the parse tree to extract the package name
                    extractor = PackageExtractor()
                    walker = ParseTreeWalker()
                    walker.walk(extractor, tree)

                    # Store the package name in the map
                    package_map[file_path] = extractor.package_name or "default"
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
    return package_map


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


def extract_fields(file_path):
    """
    Parse a Java file to extract field declarations.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    input_stream = InputStream(content)
    lexer = JavaLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParser(token_stream)

    # Parse the file starting from the compilation unit
    tree = parser.compilationUnit()
    visitor = FieldVisitor()

    # Extract fields using the visitor
    visitor.visit(tree)

    return visitor.fields


def find_duplicate_fields_in_directory(directory_path):
    """
    Scan all Java files in the given directory to identify duplicate fields across classes.
    """
    field_signatures = {}  # Map to track field signatures and associated classes
    duplicate_fields = []  # List to store duplicated fields
    packages = extract_packages(directory_path)

    # Traverse the directory and process each Java file
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".java"):  # Process only Java files
                file_path = os.path.join(root, file_name)

                # Extract fields from the Java file
                fields = extract_fields(file_path)

                # Check for duplicate fields
                for field_type, field_name, class_name in fields:
                    signature = f"{field_type} {field_name}"  # Create a unique signature for each field
                    package_name = packages.get(file_path, "default")
                    if signature in field_signatures:
                        field_signatures[signature].append((class_name, package_name))  # Add the class to the signature
                    else:
                        field_signatures[signature] = [(class_name, package_name)]

    # Identify duplicated fields that exist in more than one class
    for signature, class_info in field_signatures.items():
        if len(class_info) > 1:
            # Extract the field name from the signature (split on space and take the second part)
            field_name = signature.split(" ")[1]  # Assuming the signature format is "fieldType fieldName"
            duplicate_fields.append((field_name, class_info))  # Store only the field name

    # Call refactoring method for each duplicated field
    for field_name, class_info in duplicate_fields:
        pull_up(directory_path, field_name, class_info)

    return duplicate_fields


def pull_up(dir_path, field, class_info):
    """
    Perform refactoring to pull up a duplicated field to a common superclass.
    """
    print(f"Refactoring field '{field}' from the following classes to a common superclass:")
    for class_name, package_name in class_info:
        print(f"Package: {package_name}, Class: {class_name}")
        # pull up field using the first class and its package
        first_class, first_package = class_info[0]

    pull_up_field(
        project_dir=dir_path,
        package_name=first_package,
        children_class=first_class,
        field_name=field
    )


if __name__ == "__main__":
    # Path to your directory with Java files
    path = "C:/Users/98910/Desktop/pull_up_field_test"
    # Find and refactor duplicate fields
    duplicated_fields = find_duplicate_fields_in_directory(path)
