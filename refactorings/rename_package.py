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

        self.packages = []
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        if ctx.qualifiedName().IDENTIFIER()[-1].getText() not in self.packages:
            self.packages.append(ctx.qualifiedName().IDENTIFIER()[-1].getText())
            print("package", ctx.qualifiedName().IDENTIFIER()[-1].getText(), "added to list")


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


def main():
    Path = "../tests/rename_tests/"
    FolderPath = os.listdir(Path)

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


    rename_method_test_file = FileStream(str(Path + "rename_package_test.java"))
    print("file opened")

    Refactored = open(os.path.join(Path, "rename_package_test_Refactored.java"), 'w', newline='')

    Lexer = JavaLexer(rename_method_test_file)

    TokenStream = CommonTokenStream(Lexer)

    Parser = JavaParserLabeled(TokenStream)

    Tree = Parser.compilationUnit()

    ListenerForReRename = RenamePackageRefactoringListener(TokenStream, "jsoniter", "jsoniter_new",
                                                           find_packages.packages)

    Walker = ParseTreeWalker()

    Walker.walk(ListenerForReRename, Tree)

    Refactored.write(ListenerForReRename.token_stream_rewriter.getDefaultText())
    print("tamam shod")


if __name__ == "__main__":
    main()
