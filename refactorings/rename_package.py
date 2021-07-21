import os
import sys

sys.path.append('../')

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaLexer import JavaLexer


class FindPackages(JavaParserLabeledListener):

    def __init__(self,
                 common_token_stream: CommonTokenStream = None):
        """
        :param common_token_stream:
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

    def __init__(self,
                 common_token_stream: CommonTokenStream = None,
                 package_identifier: str = None,
                 package_new_name: str = None,
                 packages_name: list = []):
        """
        :param common_token_stream:
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
    Path = "../tests/rename_tests/benchmark"
    package_identifier = "json"
    new_package_name = "test"

    FolderPath = os.listdir(Path)
    testsPath = os.listdir(Path + "/refactoredFiles/")

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
        os.remove(os.path.join(Path + "/refactoredFiles/", t))

    for File in FolderPath:
        # We have all of the java files in this folder now
        if File.endswith('.java'):
            EachFilePath = Path + "/" + File
            print(" ****************" + " in file : " + File + " ****************")
            EachFile = FileStream(str(EachFilePath))
            FileName = File.split(".")[0]
            Refactored = open(Path + "/refactoredFiles/" + FileName + "_Refactored.java", 'w', newline='')

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
