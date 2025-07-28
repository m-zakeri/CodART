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

        # If no package is specified, assume it’s already in the correct scope
        self.is_package_imported = package_name == ""
        self.in_class = False
        self.in_selected_package = package_name == ""

        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        # Only check package if a package name is provided
        if self.package_identifier and self.package_identifier == ctx.qualifiedName().getText():
            self.in_selected_package = True
            print("Package " + self.package_identifier + " Found")

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        # Only check import if a package name is provided
        if self.package_identifier and any([
            ctx.getText() == f"import {self.package_identifier}.{self.class_identifier};",
            ctx.getText() == f"import {self.package_identifier}.*;",
            ctx.getText() == f"import {self.package_identifier};"
        ]):
            self.is_package_imported = True
            print("package " + self.package_identifier + " imported")

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_package_imported or self.in_selected_package:
            if ctx.IDENTIFIER().getText() in self.class_identifier:
                self.in_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_package_imported or self.in_selected_package:
            if ctx.IDENTIFIER().getText() in self.class_identifier:
                self.in_class = False

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if (self.is_package_imported or self.in_selected_package) and self.in_class:
            if ctx.getChild(1).getText() in self.method_identifier:
                start_token = ctx.getChild(1).getSymbol()  # Get the method name token directly
                stop_token = start_token  # This assumes that the name is a single token

                # Replace the old method name with the new method name
                self.token_stream_rewriter.replaceRange(
                    from_idx=start_token.tokenIndex,
                    to_idx=stop_token.tokenIndex,
                    text=self.method_new_name
                )
                print(f"Method name '{ctx.getChild(1).getText()}' changed to '{self.method_new_name}'!")

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        if self.is_package_imported or self.in_selected_package:
            if self.in_class and ctx.IDENTIFIER().getText() in self.method_identifier:
                start_token = ctx.IDENTIFIER().getSymbol()
                stop_token = start_token

                # Replace the old method call name with the new method name
                self.token_stream_rewriter.replaceRange(
                    from_idx=start_token.tokenIndex,
                    to_idx=stop_token.tokenIndex,
                    text=self.method_new_name
                )
                print(f"Method call name '{ctx.IDENTIFIER().getText()}' changed to '{self.method_new_name}'!")


def main(base_path, package_name, class_identifier, method_identifier, method_new_name):
    # base_path = "C:/Users/98910/Desktop/pull-up-method-example - Copy"
    # package_name = "org.json"
    # class_identifier = "CDL"
    # method_identifier = "getValue"
    # method_new_name = "test"

    try:
        # Clear existing refactored files
        refactored_path = os.path.join(base_path, "refactored")
        for filename in os.listdir(refactored_path):
            file_path = os.path.join(refactored_path, filename)
            if filename.endswith(".java"):
                os.remove(file_path)

        for filename in os.listdir(base_path):
            if filename.endswith(".java"):
                file_path = os.path.join(base_path, filename)
                print(f"Processing file: {filename}")

                try:
                    with open(file_path, 'r') as file:
                        input_stream = FileStream(file_path)
                    lexer = JavaLexer(input_stream)
                    token_stream = CommonTokenStream(lexer)
                    parser = JavaParserLabeled(token_stream)
                    tree = parser.compilationUnit()
                    listener = RenameMethodRefactoringListener(
                        token_stream, package_name, class_identifier, method_identifier, method_new_name
                    )
                    walker = ParseTreeWalker()
                    walker.walk(listener, tree)
                    refactored_file_path = os.path.join(refactored_path, f"{filename.split('.')[0]}_Refactored.java")
                    with open(refactored_file_path, 'w') as refactored_file:
                        refactored_file.write(listener.token_stream_rewriter.getDefaultText())
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")

        print("All files have been processed and refactored.")

    except Exception as e:
        print(f"An error occurred in the main function: {e}")


if __name__ == "__main__":
    main()
