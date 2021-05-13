import os
import sys
sys.path.append('../')

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaLexer import JavaLexer


class RenameMethodRefactoringListener(JavaParserLabeledListener):

    def __init__(self,
                 common_token_stream: CommonTokenStream = None,
                 scope_class_name: str = None,
                 method_identifier: str = None,
                 method_new_name: str = None):
        """
        :param common_token_stream:
        """
        self.token_stream = common_token_stream
        self.scope_class_name = scope_class_name
        self.method_identifier = method_identifier
        self.method_new_name = method_new_name

        self.is_in_scope = False
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):

        if ctx.IDENTIFIER().getText() == self.scope_class_name:
            self.is_in_scope = True
        print("class scope detected")

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.scope_class_name:
            self.is_in_scope = False
        print("class scope exited")

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_in_scope:
            if ctx.IDENTIFIER().getText() == self.method_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex+ 2,
                    text=self.method_new_name)
                print("method name changed !")

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        if self.is_in_scope:
            if ctx.IDENTIFIER().getText() == self.method_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex,
                    text=self.method_new_name)
                print("method call name changed !")

def main():
    Path = "../tests/rename_tests/"
    rename_method_test_file = FileStream(str(Path + "rename_method_test.java"))
    print("file opened")

    Refactored = open(os.path.join(Path, "rename_method_test_Refactored.java"), 'w', newline='')

    Lexer = JavaLexer(rename_method_test_file)

    TokenStream = CommonTokenStream(Lexer)

    Parser = JavaParserLabeled(TokenStream)

    Tree = Parser.compilationUnit()

    ListenerForReRename = RenameMethodRefactoringListener(TokenStream, "SuggestedRoomsByFollowingsListViewAdapter", "RoomModel", "RoomModel_changed")

    Walker = ParseTreeWalker()

    Walker.walk(ListenerForReRename, Tree)

    Refactored.write(ListenerForReRename.token_stream_rewriter.getDefaultText())
    print("tamam shod")


if __name__ == "__main__":
    main()
