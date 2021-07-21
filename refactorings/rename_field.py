import os
import sys

sys.path.append('../')

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaLexer import JavaLexer


class RenameFieldRefactoringListener(JavaParserLabeledListener):

    def __init__(self,
                 common_token_stream: CommonTokenStream = None,
                 package_name: str = None,
                 scope_class_name: str = None,
                 field_identifier: str = None,
                 field_new_name: str = None):

        self.token_stream = common_token_stream
        self.class_identifier = scope_class_name
        self.field_identifier = field_identifier
        self.field_new_name = field_new_name
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

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if self.in_class:
            if ctx.variableDeclarators().variableDeclarator(
                    0).variableDeclaratorId().getText() == self.field_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().start.tokenIndex,
                    text=self.field_new_name)
                print("field name changed !")

    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        if self.in_class:
            if ctx.expression(0).getText() == self.field_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.expression(0).start.tokenIndex,
                    text=self.field_new_name)
                print("expression21 changed! ")
            elif ctx.expression(0).getText() == "this." + self.field_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.expression(0).start.tokenIndex + 2,
                    text=self.field_new_name)
                # print("expression21 ", ctx.expression(0).getText(), " changed to: ", "this.", self.field_new_name)
                print("expression21 changed! ")

            if ctx.expression(1).getText() == self.field_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.expression(1).start.tokenIndex,
                    text=self.field_new_name)
                # print("expression21 ", ctx.expression(1).getText(), " changed to: ", self.field_new_name)
                print("expression21 changed! ")

            elif ctx.expression(1).getText() == "this." + self.field_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.expression(1).start.tokenIndex + 2,
                    text=self.field_new_name)
                # print("expression21 ", ctx.expression(1).getText(), " changed to: ", "this.", self.field_new_name)
                print("expression21 changed! ")

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
        if self.in_class:
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
    #
    # def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
    #     print(ctx.expressionList())


def main():
    Path = "../tests/rename_tests/benchmark"
    Package_name = "org.json"
    class_identifier = "HTTP"
    field_identifier = "CRLF"
    field_new_name = "test"

    FolderPath = os.listdir(Path)
    testsPath = os.listdir(Path + "/refactoredFiles/")

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
                RenameFieldRefactoringListener(TokenStream, Package_name, class_identifier, field_identifier,
                                               field_new_name)

            Walker = ParseTreeWalker()

            Walker.walk(ListenerForReRenameClass, Tree)

            Refactored.write(ListenerForReRenameClass.token_stream_rewriter.getDefaultText())

    print(" %%%%%%%%%%%%%" + " all files finished " + "****************")


if __name__ == "__main__":
    main()
