"""
When the name of a package does not explain what the class does (package's functionality), it needs to be changed.

### Pre-conditions:

Todo: Add pre-conditions

### Post-conditions:

Todo: Add post-conditions


"""

__author__ = 'Morteza Zakeri'
__version__ = '0.1.2'


import os
import sys

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from codart.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from codart.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from codart.gen.javaLabeled.JavaLexer import JavaLexer


sys.path.append('../../')


class FindPackages(JavaParserLabeledListener):
    """
    The class find packages

    """

    def __init__(self, common_token_stream: CommonTokenStream = None):
        """

        """

        self.token_stream = common_token_stream

        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        if ctx.qualifiedName().IDENTIFIER()[-1].getText() not in packages:
            packages.append(ctx.qualifiedName().IDENTIFIER()[-1].getText())
            print("package", ctx.qualifiedName().IDENTIFIER()[-1].getText(), "added to list")


packages = []


class RenamePackageRefactoringListener(JavaParserLabeledListener):
    """
        The class implements Rename Package refactoring.
    """
    def __init__(self,
                 common_token_stream: CommonTokenStream = None,
                 package_identifier: str = None,
                 package_new_name: str = None,
                 packages_name: list = []):
        """
         Args:

             common_token_stream (CommonTokenStream): An instance of ANTLR4 CommonTokenStream class

             package_identifier(str): Name of the package in which the refactoring has to be done

             package_new_name(str): The new name of the refactored method

             packages_name(str): Name of the packages in which the refactoring has to be done

        Returns:

            RenamePackageRefactoringListener: An instance of RenamePackageRefactoringListener class

        """

        self.token_stream = common_token_stream
        self.package_identifier = package_identifier
        self.package_new_name = package_new_name
        self.packages_name = packages_name
        self.is_in_scope = False
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        if self.package_identifier == ctx.qualifiedName().IDENTIFIER()[-1].getText():
            if self.package_new_name not in self.packages_name:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.qualifiedName().start.tokenIndex + (2 * len(ctx.qualifiedName().IDENTIFIER()) - 2),
                    text=self.package_new_name)
                print("package changed")

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        if ctx.qualifiedName().IDENTIFIER()[-1].getText() == self.package_identifier:
            if self.package_new_name not in self.packages_name:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.qualifiedName().start.tokenIndex + (2 * len(ctx.qualifiedName().IDENTIFIER()) - 2),
                    text=self.package_new_name)
                print("package name in import changed")



def main():
    Path = "../../tests/rename_tests/benchmark_projects_test"
    package_identifier = "json"
    new_package_name = "test"

    FolderPath = os.listdir(Path)
    testsPath = os.listdir(Path + "/JSON_refactored/")

    for File in FolderPath:
        # We have all of the java files in this folder now
        if File.endswith('.java'):
            EachFilePath = Path + "\\" + File
            EachFile = FileStream(str(EachFilePath))

            Lexer = JavaLexer(EachFile)

            TokenStream = CommonTokenStream(Lexer)

            Parser = JavaParserLabeled(TokenStream)

            Tree = Parser.compilationUnit()

            find_packages = FindPackages(TokenStream)
            Walker = ParseTreeWalker()
            Walker.walk(find_packages, Tree)

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
                RenamePackageRefactoringListener(TokenStream, package_identifier, new_package_name,
                                                 packages)

            Walker = ParseTreeWalker()

            Walker.walk(ListenerForReRenameClass, Tree)

            Refactored.write(ListenerForReRenameClass.token_stream_rewriter.getDefaultText())

    print(" %%%%%%%%%%%%%" + " all files finished " + "****************")


if __name__ == "__main__":
    main()
