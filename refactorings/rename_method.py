import os

try:
    import understand as und
except ModuleNotFoundError:
    # Error handling
    pass

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class RenameMethodListener(JavaParserLabeledListener):
    """
    ## Introduction

    When the name of a method does not explain what the method does (method's functionality), it needs to be changed.

    ## Pre and Post Conditions

    ### Pre Conditions:

    1. User must enter the existing method's name, The source class's name for the refactoring, and the new method name
         in order to rename.

    2. Check if the method exist, then rename it.

    ### Post Conditions:

    1. After refactoring, all the old method names in the project should be changed.

    See whether the method is defined in a superclass or subclass. If so, you must repeat all steps in these classes too.

    The next method is important for maintaining the functionality of the program during the refactoring process. Create
    a new method with a new name. Copy the code of the old method to it. Delete all the code in the old method and,
    instead of it, insert a call for the new method.

    Find all references to the old method and replace them with references to the new one.

    Delete the old method. If the old method is part of a public interface, don’t perform this step. Instead,
    mark the old method as deprecated.
    """

    def __init__(self, java_file_path, common_token_stream, scope_class_name, target_method_name, new_name,
                 reference=None):
        """The Main listener which parses the file based on the provided information,
            using ANTLR parser generator and tokenization methods

            Args:
                java_file_path(str): Address path to the test/source file

                scope_class_name(str): Name of the class in which the refactoring has to be done

                target_method_name(str): Name of the method in which the refactoring has to be done

                new_name(str): The new name of the refactored method

            Returns:
                No returns
        """
        self.file_path = java_file_path
        self.token_stream = common_token_stream
        self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        self.class_name = scope_class_name
        self.method_name = target_method_name
        self.new_method_name = new_name
        self.in_class = False
        self.changed = False
        self.reference = reference

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        name = ctx.IDENTIFIER().getText()
        if name == self.class_name:
            self.in_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        name = ctx.IDENTIFIER().getText()
        if name == self.class_name:
            self.in_class = False

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.in_class:
            name = ctx.IDENTIFIER()
            if name.getText() == self.method_name:
                node = name.getSymbol()
                self.token_stream_rewriter.replaceIndex(
                    node.tokenIndex,
                    self.new_method_name
                )
                self.changed = True

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        if self.in_class and self.reference:
            name = ctx.IDENTIFIER()
            if name.getText() == self.method_name:
                node = name.getSymbol()
                if node.line == self.reference["line"]:
                    self.token_stream_rewriter.replaceIndex(
                        node.tokenIndex,
                        self.new_method_name
                    )
                    self.changed = True

    def enterMethodCall1(self, ctx: JavaParserLabeled.MethodCall1Context):
        if self.in_class and self.reference:
            name = ctx.IDENTIFIER()
            if name.getText() == self.method_name:
                node = name.getSymbol()
                if node.line == self.reference["line"]:
                    self.token_stream_rewriter.replaceIndex(
                        node.tokenIndex,
                        self.new_method_name
                    )
                    self.changed = True


def get_method_calls(udb_path, scope_class_name, new_name):
    # Open Database
    """Finds all of the refactored method calls in the database file
       and returns all of the correct references

        Args:
            udb_path (str): Address path to the database file

            scope_class_name (str): Name of the class in which the refactoring has to be done

            new_name (str): The new name of the refactored method

        Returns:
            References
    """
    if not os.path.exists(path=udb_path):
        raise ValueError("Database file does not exist!")
    db = und.open(udb_path)
    method_scope = scope_class_name + "." + new_name
    references = []
    # Find All Method Calls
    for ent in sorted(db.ents(), key=lambda ent: ent.name()):
        for ref in ent.refs(refkindstring="Call"):
            scope = str(ref.ent())
            if scope == method_scope:
                references.append({
                    "scope": str(ref.scope()),
                    "file_name": str(ref.file()),
                    "file_path": str(ref.file().longname()),
                    "line": ref.line(),
                    "column": ref.column()
                })
    return references


def rename_method(java_file_path, scope_class_name, target_method_name, new_name, reference=None):
    """Main Entry Point to the Listener and Tree Walker

    Args:
        java_file_path(str): Address path to the test/source file

        scope_class_name(str): Name of the class in which the refactoring has to be done

        target_method_name(str): Name of the method in which the refactoring has to be done

        new_name(str): The new name of the refactored method

        reference(str): Keeping track for all of the method references in the project scope

    Returns:
        No Returns
   """
    stream = FileStream(java_file_path)
    lexer = JavaLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    tree = parser.compilationUnit()
    listener = RenameMethodListener(
        java_file_path=java_file_path,
        common_token_stream=tokens,
        scope_class_name=scope_class_name,
        target_method_name=target_method_name,
        new_name=new_name,
        reference=reference
    )
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    if listener.changed:
        print(java_file_path)
        new_file = open(file=java_file_path, mode='w')
        new_file.write(listener.token_stream_rewriter.getDefaultText().replace('\r', ''))


def main():
    # TODO: Create UDB File automatically
    # db_path = "/home/ali/Documents/compiler/Research/xerces2-j/xerces2-j.udb"
    file_path = "D:/archive/uni/CD/project/CodART/tests/simpleCode.java"
    class_name = "C"
    method_name = "printG"
    new_method_name = "printFUCK"
    # references = get_method_calls(db_path, class_name, method_name)
    rename_method(file_path, class_name, method_name, new_method_name)

    # for ref in references:
        # rename_method(ref["file_path"], ref["scope"].split(".")[0], target_method_name=method_name,
        #               new_name=new_method_name, reference=ref)

if __name__ == '__main__':
    main()