"""

When the name of a class field does not explain what the field hold, it needs to be changed.


### Pre-conditions:

Todo: Add pre-conditions

### Post-conditions:

Todo: Add post-conditions


"""

__author__ = 'Morteza Zakeri'
__version__ = '0.1.1'

import os
import sys

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from codart.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from codart.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from codart.gen.javaLabeled.JavaLexer import JavaLexer

sys.path.append('../../')


class RenameFieldRefactoringListener(JavaParserLabeledListener):
    """
    The class performs Rename Field Refactoring

    """

    def __init__(self,
                 common_token_stream: CommonTokenStream = None,
                 package_name: str = None,
                 scope_class_name: str = None,
                 field_identifier: str = None,
                 field_new_name: str = None):

        """
        Args:

            common_token_stream (CommonTokenStream): An instance of ANTLR4 CommonTokenStream class

            package_name(str): Name of the packages in which the refactoring has to be done

            scope_class_name(str): Name of the class in which the refactoring has to be done

            field_identifier(str): Name of the package in which the refactoring has to be done

            field_new_name(str): The new name of the refactored method

        Returns:

            RenameFieldListener: An instance of RenameFieldListener class

        """

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
    path_ = "../../tests/rename_tests/benchmark_projects_test"
    package_name_ = "org.json"
    class_identifier_ = "HTTP"
    field_identifier_ = "CRLF"
    field_new_name_ = "test"

    folder_path = os.listdir(path_)
    tests_path = os.listdir(path_ + "/JSON_refactored/")

    # delete last refactored files
    for t in tests_path:
        os.remove(os.path.join(path_ + "/JSON_refactored/", t))

    for file_ in folder_path:
        # We have all java files in this folder now
        if file_.endswith('.java'):
            file_path = path_ + "/" + file_
            file_stream = FileStream(str(file_path))
            file_name = file_.split(".")[0]
            refactored = open(path_ + "/JSON_refactored/" + file_name + "_Refactored.java", 'w', newline='')

            lexer = JavaLexer(file_stream)
            token_stream = CommonTokenStream(lexer)
            parser = JavaParserLabeled(token_stream)
            tree = parser.compilationUnit()
            rename_field_refactoring_listener = RenameFieldRefactoringListener(
                token_stream,
                package_name_,
                class_identifier_,
                field_identifier_,
                field_new_name_
            )

            walker = ParseTreeWalker()
            walker.walk(rename_field_refactoring_listener, tree)
            refactored.write(rename_field_refactoring_listener.token_stream_rewriter.getDefaultText())

    print(" %%%%%%%%%%%%%" + " all files finished " + "****************")


if __name__ == "__main__":
    main()
