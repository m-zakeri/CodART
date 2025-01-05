
"""

## Introduction

The module implements pull-up method refactoring operation.


### Pre-conditions:

Todo: Add pre-conditions

### Post-conditions:

Todo: Add post-conditions

"""

__version__ = '0.2.0'
__author__ = 'Morteza Zakeri'

import os
import os.path
import antlr4
import re

from codart.symbol_table import Program

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from codart.gen.JavaLexer import JavaLexer
from codart.gen.JavaParserLabeled import JavaParserLabeled
from codart.gen.JavaParserLabeledListener import JavaParserLabeledListener
from codart.config import logger

from antlr4.InputStream import InputStream
from codart.gen.JavaParser import JavaParser
from codart.gen.JavaParserVisitor import JavaParserVisitor
from codart.refactorings.rename_method2 import main as rename_method
from codart.refactorings.pullup_field import pull_up_field
from codart.utility.directory_utils import create_understand_database


class PullUpMethodIdentification:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.method_bodies = {}
        self.duplicate_methods = []

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

    def extract_methods(self, file_path):
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
        visitor = self.MethodBodyVisitor()

        # Extract methods using the visitor
        visitor.visit(tree)

        return visitor.methods  # Return the list of methods (name, body, class, package)

    def find_duplicate_methods_in_directory(self):
        """
        Scan all Java files in the given directory and identify duplicate methods with identical bodies.
        """

        # Iterate over all Java files in the directory
        for root, _, files in os.walk(self.directory_path):
            for file_name in files:
                if file_name.endswith(".java"):  # Process only .java files
                    file_path = os.path.join(root, file_name)

                    # Extract methods from the Java file
                    methods = self.extract_methods(file_path)

                    # Identify duplicate methods
                    for method_name, method_body, class_name, package_name in methods:
                        # Normalize the body to remove unnecessary spaces or differences
                        normalized_body = method_body.strip()

                        if normalized_body in self.method_bodies:
                            self.method_bodies[normalized_body].append((method_name, file_path, class_name, package_name))
                        else:
                            self.method_bodies[normalized_body] = [(method_name, file_path, class_name, package_name)]

        # Find methods that have duplicates (more than one entry for the same body)
        for body, method_info in self.method_bodies.items():
            if len(method_info) > 1:
                original_method = method_info[0]

                for duplicate_method in method_info[1:]:
                    self.duplicate_methods.append(
                        (original_method[0], duplicate_method[0], original_method[2], duplicate_method[2],
                         original_method[3], duplicate_method[3]))

                print("Duplicate methods that need renaming:")
                for (original_method, duplicate_method, original_class,
                     duplicate_class, original_package, duplicate_package) in self.duplicate_methods:
                    print(f"Original Method: {original_method} (Class: {original_class}, Package: {original_package}), "
                          f"Duplicate Method: {duplicate_method} (Class: {duplicate_class}, Package: {duplicate_package})")
                for (original_method, duplicate_method, original_class,
                     duplicate_class, original_package, duplicate_package) in self.duplicate_methods:
                    class_identifier = (original_class, duplicate_class)
                    method_identifier = (original_method, duplicate_method)
                    method_new_name = original_method  # Define your new naming convention as needed
                    try:
                        print(f"Renaming duplicate method '{method_identifier}' in class '{class_identifier}' "
                              f"to '{method_new_name}'")
                        # Call the main function to perform renaming
                        refactored_path = os.path.join(self.directory_path, "refactored")
                        os.makedirs(refactored_path, exist_ok=True)  # Ensure refactored folder exists

                        rename_method(base_path=self.directory_path, package_name=duplicate_package,
                                      class_identifier=class_identifier, method_identifier=method_identifier,
                                      method_new_name=method_new_name)
                        # Now call find_duplicate_fields_in_directory after renaming methods
                        print(f"Renaming done. Now scanning for duplicate fields in '{refactored_path}'")
                        pull_up_field(refactored_path)
                    except Exception as e:
                        print(f"Error renaming method {method_identifier}: {e}")
                return self.duplicate_methods


class CheckOverrideListener(JavaParserLabeledListener):
    pass


class PullUpMethodRefactoringListener(JavaParserLabeledListener):
    """

    To implement pull-up method refactoring based on its actors.

    """

    def __init__(self, common_token_stream: CommonTokenStream = None, destination_class: str = None,
                 children_class: list = None, moved_methods=None, method_text: str = None):
        """


        """

        if method_text is None:
            self.mothod_text = []
        else:
            self.method_text = method_text

        if moved_methods is None:
            self.moved_methods = []
        else:
            self.moved_methods = moved_methods
        if children_class is None:
            self.children_class = []
        else:
            self.children_class = children_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if destination_class is None:
            raise ValueError("source_class is None")
        else:
            self.destination_class = destination_class

        self.is_children_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""
        self.tempdeclarationcode = ""

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):

        if self.is_children_class:

            method_identifier = ctx.IDENTIFIER().getText()
            if self.moved_methods == method_identifier:
                method_defctx = ctx.parentCtx.parentCtx
                start_index = method_defctx.start.tokenIndex
                stop_index = method_defctx.stop.tokenIndex
                self.method_text = self.token_stream_rewriter.getText(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    start=start_index,
                    stop=stop_index)

                self.token_stream_rewriter.delete(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=method_defctx.start.tokenIndex,
                    to_idx=method_defctx.stop.tokenIndex
                )
        else:
            return None

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier in self.children_class:
            self.is_children_class = True

        else:
            # Enter another class
            self.is_children_class = False

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        class_decctx = ctx.parentCtx
        if hasattr(class_decctx, "IDENTIFIER"):
            class_identifier = class_decctx.IDENTIFIER().getText()

            if class_identifier in self.destination_class:
                self.token_stream_rewriter.replaceRange(
                    from_idx=ctx.start.tokenIndex + 1,
                    to_idx=ctx.start.tokenIndex + 1,
                    text="\n" + self.method_text + "\n"
                )

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_children_class:
            self.is_children_class = False

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):

        self.token_stream_rewriter.insertAfter(
            index=ctx.stop.tokenIndex,
            text=self.code
        )


class PropagationPullUpMethodRefactoringListener(JavaParserLabeledListener):
    def __init__(self, token_stream_rewriter: CommonTokenStream = None, old_class_name: list = None,
                 new_class_name: str = None, propagated_class_name: list = None):

        if propagated_class_name is None:
            self.propagated_class_name = []
        else:
            self.propagated_class_name = propagated_class_name

        if new_class_name is None:
            self.new_class_name = []
        else:
            self.new_class_name = new_class_name

        if old_class_name is None:
            self.old_class_name = []
        else:
            self.old_class_name = old_class_name

        if token_stream_rewriter is None:
            raise ValueError('token_stream_rewriter is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(token_stream_rewriter)

        self.is_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""
        self.tempdeclarationcode = ""
        self.method_text = ""

    def enterVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        if not self.is_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        class_identifier = grand_parent_ctx.typeType().getText()
        if class_identifier in self.old_class_name:
            self.token_stream_rewriter.replaceRange(
                from_idx=grand_parent_ctx.typeType().start.tokenIndex,
                to_idx=grand_parent_ctx.typeType().stop.tokenIndex,
                text=self.new_class_name
            )
            grand_child_ctx = ctx.variableInitializer().expression().creator().createdName()
            self.token_stream_rewriter.replaceRange(
                from_idx=grand_child_ctx.start.tokenIndex,
                to_idx=grand_child_ctx.stop.tokenIndex,
                text=self.new_class_name
            )

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier in self.propagated_class_name:
            self.is_class = True

        else:
            # Enter other class
            self.is_class = False


def get_removed_methods(program: Program, packagename: str, superclassname: str, methodkey: str, classname: str):
    extendedclass = []
    removemethods = {}

    met = program.packages[packagename].classes[classname].methods[methodkey]
    body_text_method = met.body_text
    parammethod = met.parameters
    returntypeofmethod = met.returntype
    nameofmethod = met.name
    # print(program)
    for package_name in program.packages:
        package = program.packages[package_name]
        # print(package)
        for class_name in package.classes:
            _class = package.classes[class_name]

            if _class.superclass_name == superclassname:
                extendedclass.append(_class)

    i = 0
    for d in extendedclass:
        class_ = extendedclass[i]
        i = i + 1
        for mk in class_.methods:
            m_ = class_.methods[mk]
            m = mk[:mk.find('(')]
            if (
                    m_.body_text == body_text_method and m_.returntype == returntypeofmethod
                    and m_.parameters == parammethod and m_.name == nameofmethod and m_.is_constructor == False):
                if class_.name not in removemethods:
                    removemethods[class_.name] = [methodkey]
                else:

                    removemethods[class_.name].append(methodkey)
    # removemethods[classname]=[nameofmethod]
    removemethods[classname] = [methodkey]
    return removemethods


def main(udb_path: str, children_classes: list, method_name: str):
    """


    """

    if len(children_classes) <= 1:
        logger.error("len(children_classes) should be gte 2")
        return False

    # Initialize with understand
    destination_class = ""
    fileslist_to_be_rafeactored = set()
    fileslist_to_be_propagate = set()
    propagation_classes = set()

    def normalize_method_content(content):
        """
        Normalize method content by:
        - Removing comments (single-line and multi-line)
        - Removing unnecessary whitespace and newlines
        """
        # Remove single-line comments (e.g., // comment)
        content = re.sub(r"//.*", "", content)
        # Remove multi-line comments (e.g., /* comment */)
        content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
        # Remove excess whitespace and newlines
        content = re.sub(r"\s+", " ", content).strip()
        return content

    db = und.open(udb_path)
    try:
        method_ents = [db.lookup(i + "." + method_name, "method")[0] for i in children_classes]
    except IndexError:
        # print([db.lookup(i + "." + method_name, "method") for i in children_classes])
        logger.error(f"Method {method_name} does not exists in all children_classes.")
        db.close()
        return False

    # Get method text
    method_text = normalize_method_content(method_ents[0].contents())
    # print('*******', len(method_text))

    for method_ent in method_ents[1:]:
        normalized_content = normalize_method_content(method_ent.contents())
        # print('*******', len(normalized_content))
        if normalized_content != method_text:
            logger.error("Method content is different.")
            db.close()
            return False

        for ref in method_ent.refs("Use,Call"):
            if ref.ent().parent() is not None:
                if ref.ent().parent().simplename() in children_classes:
                    logger.error("Method has internal dependencies.")
                    db.close()
                    return False

    for mth in db.ents("Java Method"):
        for child in children_classes:
            if mth.longname().endswith(child + "." + method_name):
                fileslist_to_be_rafeactored.add(mth.parent().parent().longname())
                for fth in mth.parent().refs("Extend"):
                    destination_class = fth.ent().longname()
                    fileslist_to_be_rafeactored.add(fth.ent().parent().longname())
                for ref in mth.refs("Java Callby"):
                    propagation_classes.add(ref.ent().parent().longname())
                    fileslist_to_be_propagate.add(ref.ent().parent().parent().longname())

    db.close()

    # print("=========================================")
    # print("fileslist_to_be_propagate :", fileslist_to_be_propagate)
    # print("propagation_classes : ", propagation_classes)
    # print("fileslist_to_be_rafeactored :", fileslist_to_be_rafeactored)
    # print("father class :", destination_class)

    fileslist_to_be_rafeactored = list(fileslist_to_be_rafeactored)
    fileslist_to_be_propagate = list(fileslist_to_be_propagate)
    propagation_class = list(propagation_classes)

    # refactored start
    for file in fileslist_to_be_rafeactored:
        try:
            stream = FileStream(file, encoding='utf-8', errors='ignore')
        except:
            continue
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        my_listener_refactor = PullUpMethodRefactoringListener(common_token_stream=token_stream,
                                                               destination_class=destination_class,
                                                               children_class=children_classes,
                                                               moved_methods=method_name,
                                                               method_text=method_text)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener_refactor)

        with open(file, mode='w', encoding='utf-8', newline='') as f:
            f.write(my_listener_refactor.token_stream_rewriter.getDefaultText())
    # end refactoring

    # beginning of propagate
    for file in fileslist_to_be_propagate:
        if not os.path.exists(file):
            continue
        stream = FileStream(file, encoding='utf-8', errors='ignore')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        my_listener_propagate = PropagationPullUpMethodRefactoringListener(token_stream_rewriter=token_stream,
                                                                           old_class_name=children_classes,
                                                                           new_class_name=destination_class,
                                                                           propagated_class_name=propagation_class)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener_propagate)

        with open(file, mode='w', encoding='utf8', errors='ignore', newline='') as f:
            f.write(my_listener_propagate.token_stream_rewriter.getDefaultText())
    # end of propagate

    return True


# Tests
if __name__ == '__main__':
    path = "C:/Users/98910/Desktop/test"
    identifier = PullUpMethodIdentification(directory_path=path)
    duplicate_methods = identifier.find_duplicate_methods_in_directory()
    udb_path = create_understand_database(path + '/refactored', path + '/refactored')
    for (original_method, duplicate_method, original_class,
         duplicate_class, original_package, duplicate_package) in duplicate_methods:
        children_classes_ = [original_class, duplicate_class]
        class_identifier = (original_class, duplicate_class)
        method_identifier = (original_method, duplicate_method)
        method_new_name = original_method
        print(f"Pulling up method '{method_new_name}' from class '{class_identifier}'")
        main(udb_path=udb_path, children_classes=children_classes_, method_name=method_new_name)

    # udb_path_ = "C:/Users/98910/Desktop/test/refactored/refactored/refactored.und"
    # children_class_ = ['Employee', 'Department']
    # moved_method_ = "getTotalAnnualCost"
    # main(
    #     udb_path=udb_path_,
    #     children_classes=children_class_,
    #     method_name=moved_method_
    # )
