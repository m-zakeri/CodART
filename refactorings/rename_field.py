import os
import sys

sys.path.append('../')

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaLexer import JavaLexer


class FindObjects(JavaParserLabeledListener):

    def __init__(self,
                 class_identifier: str = None):
        """
        :param common_token_stream:
        """
        self.class_identifier = class_identifier

        self.objects = []
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.

    def enterVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        print(
            "fjksdlajflkasdjfklasdjflkasjdfkljsdfkljasdklfjaslkdfjlfjksdlajflkasdjfklasdjflkasjdfkljsdfkljasdklfjaslkdfjl")
        print(ctx.variableDeclaratorId().getText())

    def exitVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        pass


class RenameFieldRefactoringListener(JavaParserLabeledListener):

    def __init__(self,
                 common_token_stream: CommonTokenStream = None,
                 scope_class_name: str = None,
                 field_identifier: str = None,
                 field_new_name: str = None):

        self.token_stream = common_token_stream
        self.scope_class_name = scope_class_name
        self.field_identifier = field_identifier
        self.field_new_name = field_new_name

        self.is_in_scope = False
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if self.is_in_scope:
            if ctx.variableDeclarators().variableDeclarator(
                    0).variableDeclaratorId().getText() == self.field_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().start.tokenIndex,
                    text=self.field_new_name)
                print("field name changed !")

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):

        if ctx.IDENTIFIER().getText() == self.scope_class_name:
            self.is_in_scope = True
            print("enter class : ", self.scope_class_name)

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.scope_class_name:
            self.is_in_scope = False
            print("exit class : ", self.scope_class_name)

    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        if self.is_in_scope:
            if ctx.expression(0).getText() == self.field_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.expression(0).start.tokenIndex,
                    text=self.field_new_name)
                print("expression21 ", ctx.expression(0).getText(), " changed to: ", self.field_new_name)
            elif ctx.expression(0).getText() == "this." + self.field_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.expression(0).start.tokenIndex + 2,
                    text=self.field_new_name)
                print("expression21 ", ctx.expression(0).getText(), " changed to: ", "this.", self.field_new_name)

            if ctx.expression(1).getText() == self.field_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.expression(1).start.tokenIndex,
                    text=self.field_new_name)
                print("expression21 ", ctx.expression(1).getText(), " changed to: ", self.field_new_name)
            elif ctx.expression(1).getText() == "this." + self.field_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.expression(1).start.tokenIndex + 2,
                    text=self.field_new_name)
                print("expression21 ", ctx.expression(1).getText(), " changed to: ", "this.", self.field_new_name)

    # def enterVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
    #     print("8888888888888888888888888888888888888888888888888888888888888888888888888888888888")
    #     x = JavaParserLabeled.VariableInitializer1Context(ctx.variableInitializer(),ctx.)
    #     y = JavaParserLabeled.Expression1Context(x.expression(), ctx)
    #     print(y.IDENTIFIER())
    #     # if self.is_in_scope:
    #     #     if ctx.variableInitializer().expression().IDENTIFIER().getText() == self.field_identifier:
    #     #         self.token_stream_rewriter.replaceIndex(
    #     #             index=ctx.expression().start.tokenIndex,
    #     #             text=self.field_new_name)
    #     #         print("8888888888888888888888888888888888888888888888888888888888888888888888888888888888")

    def enterVariableInitializer1(self, ctx: JavaParserLabeled.VariableInitializer1Context):
        if self.is_in_scope:
            if ctx.expression().getText() == self.field_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.expression().start.tokenIndex,
                    text=self.field_new_name)
                print("variable initializer changed")
            elif ctx.expression().getText() == "this." + self.field_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.expression().start.tokenIndex + 2,
                    text=self.field_new_name)
                print("variable initializer changed")

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        print(ctx.expressionList())


def main():
    Path = "../tests/rename_tests/"
    rename_method_test_file = FileStream(str(Path + "rename_field_test.java"))
    print("file opened")

    Refactored = open(os.path.join(Path, "rename_field_test_Refactored.java"), 'w', newline='')

    Lexer = JavaLexer(rename_method_test_file)

    TokenStream = CommonTokenStream(Lexer)

    Parser = JavaParserLabeled(TokenStream)

    Tree = Parser.compilationUnit()

    findObjects = FindObjects("SuggestedRoomsByFollowingsListViewAdapter")
    Walker = ParseTreeWalker()
    Walker.walk(findObjects, Tree)

    ListenerForReRename = RenameFieldRefactoringListener(TokenStream, "SuggestedRoomsByFollowingsListViewAdapter",
                                                         "mContext", "field_New")

    Walker = ParseTreeWalker()

    Walker.walk(ListenerForReRename, Tree)

    Refactored.write(ListenerForReRename.token_stream_rewriter.getDefaultText())
    print("tamam shod")


if __name__ == "__main__":
    main()
