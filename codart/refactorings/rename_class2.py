"""
## Introduction

When the name of a class does not explain what the class does (class's functionality), it needs to be changed.

The module implements a Rename Class refactoring.

### Pre-conditions:

Todo: Add pre-conditions

### Post-conditions:

Todo: Add post-conditions


"""

import os
import sys

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from codart.gen.JavaParserLabeled import JavaParserLabeled
from codart.gen.JavaParserLabeledListener import JavaParserLabeledListener
from codart.gen.JavaLexer import JavaLexer

sys.path.append('../../')


class RenameClassRefactoringListener(JavaParserLabeledListener):
    """

    The class implements rename class refactoring

    """

    def __init__(self,
                 common_token_stream: CommonTokenStream = None,
                 package_name: str = None,
                 class_identifier: str = None,
                 class_new_name: str = None):

        """
        Args:

            common_token_stream (CommonTokenStream): An instance of ANTLR4 CommonTokenStream class

            package_name(str): Name of the package in which the refactoring has to be done

            class_identifier(str): Name of the class in which the refactoring has to be done

            class_new_name(str): The new name of the refactored class


        Returns:

            RenameMethodListener: An instance of RenameClassRefactoringListener class

        """

        self.token_stream = common_token_stream
        self.class_new_name = class_new_name
        self.class_identifier = class_identifier
        self.package_identifier = package_name

        self.is_package_imported = False
        self.in_selected_package = False
        self.in_selected_class = False
        self.in_some_package = False

        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.in_some_package = True
        if self.package_identifier == ctx.qualifiedName().getText():
            self.in_selected_package = True
            print("Package " + self.package_identifier + " Found")

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        if ctx.getText() == "import" + self.package_identifier + "." + self.class_identifier + ";" \
                or ctx.getText() == "import" + self.package_identifier + ".*" + ";" \
                or ctx.getText() == "import" + self.package_identifier + ";":
            self.is_package_imported = True
            print("package " + self.package_identifier + " imported")
        if ctx.getText() == "import" + self.package_identifier + "." + self.class_identifier + ";":
            self.token_stream_rewriter.replaceIndex(
                index=ctx.qualifiedName().start.tokenIndex + 2 * len(ctx.qualifiedName().IDENTIFIER()) - 2,
                text=self.class_new_name)
            print("class name in package changed")

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_package_imported or self.in_selected_package:
            if ctx.IDENTIFIER().getText() == self.class_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex + 2,
                    text=self.class_new_name)
                change_file_name(self.class_identifier, self.class_new_name)
                print("class name : " + self.class_identifier + " in class declaration changed ")

    def enterCreatedName0(self, ctx: JavaParserLabeled.CreatedName0Context):
        if self.is_package_imported or self.in_selected_package:
            if ctx.IDENTIFIER(0).getText() == self.class_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex,
                    text=self.class_new_name)
                print("class name in creator changed")

    def enterClassOrInterfaceType(self, ctx: JavaParserLabeled.ClassOrInterfaceTypeContext):
        if self.is_package_imported or self.in_selected_package:
            if ctx.IDENTIFIER(0).getText() == self.class_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex,
                    text=self.class_new_name)
                print("class type changed")

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        if self.is_package_imported or self.in_selected_package:
            if ctx.IDENTIFIER().getText() == self.class_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex,
                    text=self.class_new_name)
                print("constructor name changed !")


old_names = []
new_names = []


def change_file_name(old, new):
    old_names.append(old)
    new_names.append(new)


def main(project_path, package_name, class_identifier, new_class_name, output_dir):
    """

    The main API for rename class refactoring

    """
    print(project_path)
    directories = os.listdir(project_path)
    output_path = os.listdir(os.path.join(project_path, output_dir))

    # delete last refactored files
    for t in output_path:
        os.remove(os.path.join(project_path, output_dir, t))

    for file_ in directories:
        # We have all Java files in this folder now
        if file_.endswith('.java'):
            print(f"Processing java source file: {file_}")
            file_stream = FileStream(str(os.path.join(project_path, file_)), encoding='utf8')
            java_lexer = JavaLexer(file_stream)
            token_stream = CommonTokenStream(java_lexer)
            parser = JavaParserLabeled(token_stream)
            parse_tree = parser.compilationUnit()
            renamer_listener = RenameClassRefactoringListener(token_stream,
                                                              package_name,
                                                              class_identifier,
                                                              new_class_name)
            walker = ParseTreeWalker()
            walker.walk(renamer_listener, parse_tree)
            refactored_file_path = os.path.join(project_path, output_dir, file_.split(".")[0] + '.java')
            with open(refactored_file_path, 'w', newline='') as f:
                f.write(renamer_listener.token_stream_rewriter.getDefaultText())

    print("Changing public class files names ... ")
    for i in range(len(old_names)):
        os.rename(os.path.join(project_path, output_dir, old_names[i] + ".java"),
                  os.path.join(project_path, output_dir, new_names[i] + ".java")
                  )

    print("Finished.")


# Test module
if __name__ == "__main__":
    from codart.refactorings.rename_class2 import main
    project_path_ = r"/JSON/"  # Project source files root
    package_name_ = r"org.json"  # Class package name
    class_identifier_ = r"CDL"  # Old class name
    new_class_name_ = r"CDL_Renamed"  # New class name
    output_dir_ = r"JSON_Refactored"  # Refactored project source files root
    main(project_path_, package_name_, class_identifier_, new_class_name_, output_dir_)
