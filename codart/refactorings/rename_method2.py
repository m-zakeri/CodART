"""
## Introduction

When the name of a method does not explain what the method does (method's functionality), it needs to be changed.

The module implements a light-weight version of Rename Method refactoring described in `rename_method.py`

### Pre-conditions:

Todo: Add pre-conditions

### Post-conditions:

Todo: Add post-conditions


"""

__author__ = 'Morteza Zakeri'
__version__ = '0.2.1'


import os
import sys

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from codart.gen.JavaParserLabeled import JavaParserLabeled
from codart.gen.JavaParserLabeledListener import JavaParserLabeledListener
from codart.gen.JavaLexer import JavaLexer

sys.path.append('../../')


class RenameMethodRefactoringListener(JavaParserLabeledListener):
    """

    The class implements Rename Method refactoring.
    The Main listener which parses the file based on the provided information, \
        using ANTLR parser generator and tokenization methods

    """
    def __init__(self,
                 common_token_stream: CommonTokenStream = None,
                 package_name: str = None,
                 scope_class_name: str = None,
                 method_identifier: str = None,
                 method_new_name: str = None):
        """

        Initializer of rename method refactoring listener

            Args:

                common_token_stream (CommonTokenStream): An instance of ANTLR4 CommonTokenStream class

                package_name(str): Name of the package in which the refactoring has to be done

                scope_class_name(str): Name of the class in which the refactoring has to be done

                method_identifier(str): Name of the method in which the refactoring has to be done

                method_new_name(str): The new name of the refactored method

            Returns:

                RenameMethodListener: An instance of RenameMethodListener class
        """

        self.token_stream = common_token_stream
        self.class_identifier = scope_class_name
        self.method_identifier = method_identifier
        self.method_new_name = method_new_name
        self.package_identifier = package_name

        self.is_package_imported = False
        self.in_class = False
        self.in_selected_package = False
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        if self.package_identifier == ctx.qualifiedName().getText():
            self.in_selected_package = True
            print("Package " + self.package_identifier + " Found")

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        if ctx.getText() == "import" + self.package_identifier + "." + self.class_identifier + ";" \
                or ctx.getText() == "import" + self.package_identifier + ".*" + ";" \
                or ctx.getText() == "import" + self.package_identifier + ";":
            self.is_package_imported = True
            print("package " + self.package_identifier + " imported")

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_package_imported or self.in_selected_package:
            if ctx.IDENTIFIER().getText() == self.class_identifier:
                self.in_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_package_imported or self.in_selected_package:
            if ctx.IDENTIFIER().getText() == self.class_identifier:
                self.in_class = False

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_package_imported or self.in_selected_package:
            if self.in_class:
                if ctx.IDENTIFIER().getText() == self.method_identifier:
                    self.token_stream_rewriter.replaceIndex(
                        index=ctx.start.tokenIndex + 2,
                        text=self.method_new_name)
                    print("method name changed !")

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        if self.is_package_imported or self.in_selected_package:
            if self.in_class:
                if ctx.IDENTIFIER().getText() == self.method_identifier:
                    self.token_stream_rewriter.replaceIndex(
                        index=ctx.start.tokenIndex,
                        text=self.method_new_name)
                    print("method call name changed !")


def main():
    Path = "../../tests/rename_tests/benchmark_projects_test"
    Package_name = "org.json"
    class_identifier = "CDL"
    method_identifier = "getValue"
    method_new_name = "test"

    FolderPath = os.listdir(Path)
    testsPath = os.listdir(Path + "/JSON_refactored/")

    # delete last refactored files
    for t in testsPath:
        os.remove(os.path.join(Path + "/JSON_refactored/", t))

    for File in FolderPath:
        # We have all of the java files in this folder now
        if File.endswith('.java'):
            EachFilePath = Path + "/" + File
            print(" ****************" + " in file : " + File + " ****************")
            EachFile = FileStream(str(EachFilePath))
            FileName = File.split(".")[0]
            Refactored = open(Path + "/JSON_refactored/" + FileName + "_Refactored.java", 'w', newline='')

            Lexer = JavaLexer(EachFile)

            TokenStream = CommonTokenStream(Lexer)

            Parser = JavaParserLabeled(TokenStream)

            Tree = Parser.compilationUnit()

            ListenerForReRenameClass = \
                RenameMethodRefactoringListener(TokenStream, Package_name, class_identifier, method_identifier,
                                                method_new_name)

            Walker = ParseTreeWalker()

            Walker.walk(ListenerForReRenameClass, Tree)

            Refactored.write(ListenerForReRenameClass.token_stream_rewriter.getDefaultText())

    print(" %%%%%%%%%%%%%" + " all files finished " + "****************")


if __name__ == "__main__":
    main()
