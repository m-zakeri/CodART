import os
import sys
import re
import antlr4
from antlr4.InputStream import InputStream
from codart.gen.JavaLexer import JavaLexer
from codart.gen.JavaParser import JavaParser
from codart.gen.JavaParserVisitor import JavaParserVisitor
os.add_dll_directory("C:\\Program Files\\SciTools\\bin\\pc-win64\\")
sys.path.append("C:\\Program Files\\SciTools\\bin\\pc-win64\\python")
import understand as und


class MethodBodyVisitor(JavaParserVisitor):
    def visitMethodBody(self, ctx):
        # Convert the method body context into a canonical form (for normalization)
        return ctx.getText()  # This can be more complex depending on requirements


def extract_body_inside_braces(method_content):
    """
    Extracts and returns the code inside the first pair of braces {} in the given method content.
    """
    # Use regex to find the first set of braces and capture everything inside
    match = re.search(r'\{(.*)}', method_content, re.DOTALL)
    return match.group(1).strip() if match else ""


def parse_method_body(body_content):
    """
    Parse the given Java method body using ANTLR and return a normalized representation.
    """
    input_stream = InputStream(body_content)
    lexer = JavaLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(stream)
    tree = parser.methodBody()  # Parse the body as a 'methodBody' rule (from the grammar)

    # Visit and normalize the method body AST
    visitor = MethodBodyVisitor()
    return visitor.visit(tree)


def get_java_class_info_and_identify_duplicates(udb_path):
    """
    Returns Java classes with methods, identifying duplicate methods with identical bodies
    across all classes. Prints the names of methods that need renaming due to identical
    implementations inside the braces.

    Args:
        udb_path (str): Path to the Understand database (.udb file).

    Returns:
        dict: A dictionary with the total class count and a list of classes with their superclasses,
              subclasses, and methods, along with a log of duplicate methods that need renaming.
    """
    # Open the Understand database
    db = und.open(udb_path)

    # Initialize counters and storage for class information
    class_count = 0
    classes_info = []
    method_bodies = {}  # To store normalized method bodies and corresponding method entities
    duplicate_methods = []  # To store methods that need renaming due to duplicate bodies

    # Iterate over all entities of type "Class"
    for clazz in db.ents("Class"):
        if clazz.language() == "Java":  # Ensure it's a Java class
            class_count += 1
            superclass = clazz.ref("Extendby")  # Get superclass if it exists
            subclasses = clazz.refs("Extend")  # Get all subclasses

            methods_info = []

            # Process each method in the class
            for method in clazz.ents("Define", "Java Method"):
                # Retrieve the full method content
                full_content = method.contents() or ""

                # Extract only the body inside the braces
                body_content = extract_body_inside_braces(full_content)

                # Parse and normalize the method body using ANTLR
                normalized_body = parse_method_body(body_content)

                # Check if another method has the same normalized body
                if normalized_body in method_bodies:
                    # Duplicate found, add the current method to duplicates list
                    original_method = method_bodies[normalized_body]
                    duplicate_methods.append((original_method.longname(), method.longname()))
                    methods_info.append(method.name())
                else:
                    # No duplicate found, add to the dictionary
                    method_bodies[normalized_body] = method
                    methods_info.append(method.name())

            # Append class details to the list
            classes_info.append({
                "class_name": clazz.name(),
                "superclass": superclass.ent().name() if superclass else None,
                "subclasses": [sub.ent().name() for sub in subclasses],
                "methods": methods_info
            })

    # Close the database
    db.close()

    # Return the count and class information, including duplicate methods log
    return {
        "total_classes": class_count,
        "classes_info": classes_info,
        "duplicate_methods": duplicate_methods  # Add duplicate methods log to the return value
    }


# Example usage
udb_path_ = "C:/Users/98910/Desktop/pull-up-method-example/pull-up-method-example.und"
result = get_java_class_info_and_identify_duplicates(udb_path_)
print(result["total_classes"])
for class_info in result["classes_info"]:
    print(f"Class: {class_info['class_name']}, Superclass: {class_info['superclass']},"
          f" Subclasses: {class_info['subclasses']}, Methods: {class_info['methods']}")
print("Duplicate methods that need renaming:")
for original_name, duplicate_name in result["duplicate_methods"]:
    print(f"{duplicate_name} (duplicate of {original_name})")
