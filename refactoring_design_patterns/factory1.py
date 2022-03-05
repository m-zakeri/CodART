"""
This module implements automated refactoring to factory method design pattern

"""

__version__ = '1.0.0'
__author__ = 'Morteza Zakeri'

import os
import time
import argparse

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class FactoryMethodRefactoringListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream = None,
                 creator_identifier: str = None,
                 products_identifier: list = None):
        self.enter_class = False
        self.token_stream = common_token_stream
        self.creator_identifier = creator_identifier
        self.products_identifier = products_identifier
        self.interfaceName = "ProductsAbstract"
        self.inCreator = False
        self.inProducts = False
        self.productsMethod = {}
        self.productsClassIndex = []
        self.productVarTypeIndex = []
        self.productVarValueIndex = []
        self.productConstructorMethod = []
        self.productConstructorParam = {}
        self.currentClass = None
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.creator_identifier:
            self.inCreator = True
            self.CretorStartIndex = ctx.classBody().start.tokenIndex
            self.currentClass = ctx.IDENTIFIER().symbol.text


        elif ctx.IDENTIFIER().getText() in self.products_identifier:
            self.inProducts = True
            self.productsClassIndex.append(ctx.IDENTIFIER().symbol.tokenIndex)
            self.currentClass = ctx.IDENTIFIER().symbol.text

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.inCreator = False
        self.inProducts = False

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.inProducts == True:
            methodModifire = ctx.parentCtx.parentCtx.start.text
            if methodModifire == 'public':
                MethodText = self.token_stream_rewriter.getText(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    start=ctx.parentCtx.parentCtx.start.tokenIndex,
                    stop=ctx.formalParameters().RPAREN().symbol.tokenIndex) + ";"
                if MethodText not in self.productsMethod:
                    self.productsMethod[MethodText] = [self.currentClass]
                else:
                    self.productsMethod[MethodText].append(self.currentClass)

    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        if self.inCreator == True:
            variableType = ctx.typeType().classOrInterfaceType().IDENTIFIER(0)
            if variableType.symbol.text in self.products_identifier:
                self.productVarTypeIndex.append(variableType.symbol.tokenIndex)
                self.productVarValueIndex.append([variableType.symbol.text,
                                                  ctx.variableDeclarators().variableDeclarator(
                                                      0).ASSIGN().symbol.tokenIndex, ctx.stop.tokenIndex])

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if self.inCreator == True:
            variableType = ctx.typeType().classOrInterfaceType().IDENTIFIER(0)
            if variableType.symbol.text in self.products_identifier:
                self.productVarTypeIndex.append(variableType.symbol.tokenIndex)
                self.productVarValueIndex.append([variableType.symbol.text,
                                                  ctx.variableDeclarators().variableDeclarator(
                                                      0).ASSIGN().symbol.tokenIndex, ctx.stop.tokenIndex])

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        if self.inProducts == True:
            Parameter = ""
            if ctx.formalParameters().children.__len__() > 0:
                ParamChild = ctx.formalParameters().children[1]
                for i in range(0, ParamChild.children.__len__(), 2):
                    Parameter += ParamChild.children[i].stop.text + ","
                Parameter = Parameter[:-1]

            self.productConstructorParam[self.currentClass] = Parameter

            ParamList = self.token_stream_rewriter.getText(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                           start=ctx.formalParameters().LPAREN().symbol.tokenIndex,
                                                           stop=ctx.formalParameters().RPAREN().symbol.tokenIndex)

            Method = "\t" + self.interfaceName + " create" + \
                     self.currentClass + ParamList + \
                     "{\n\t\t" + "return new " + self.currentClass + "(" + Parameter + ");\n\t}\n"

            self.productConstructorMethod.append(Method)

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        # InterfaceChecked
        interfaceMethodList = []
        for key, value in self.productsMethod.items():
            if sorted(value) == sorted(self.products_identifier):
                interfaceMethodList.append(key)
        if interfaceMethodList.__len__() > 0:
            intefaceText = "public interface " + self.interfaceName + "{"
            for item in interfaceMethodList:
                intefaceText += "\n\t" + item
            intefaceText += "\n}\n\n"
            self.token_stream_rewriter.insertBefore(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                    index=1,
                                                    text=intefaceText)

            for item in self.productsClassIndex:
                self.token_stream_rewriter.insertAfter(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                       index=item,
                                                       text=" implements " + self.interfaceName)

            for item in self.productVarTypeIndex:
                self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                   from_idx=item,
                                                   to_idx=item,
                                                   text=self.interfaceName)
            for item in self.productVarValueIndex:
                self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                   from_idx=item[1] + 1,
                                                   to_idx=item[2],
                                                   text="create" + item[0] + " (" +
                                                        self.productConstructorParam[item[0]] + ")")

            newProductMethod = "\n"
            for item in self.productConstructorMethod:
                newProductMethod += item
            self.token_stream_rewriter.insertAfter(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                   index=self.CretorStartIndex,
                                                   text=newProductMethod)


def main(args):
    # Step 1: Load input source into stream
    stream = FileStream(args.file, encoding='utf8')
    # input_stream = StdinStream()

    # Step 2: Create an instance of AssignmentStLexer
    lexer = JavaLexer(stream)
    # Step 3: Convert the input source into a list of tokens
    token_stream = CommonTokenStream(lexer)
    # Step 4: Create an instance of the AssignmentStParser
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    # Step 5: Create parse tree
    parse_tree = parser.compilationUnit()
    # Step 6: Create an instance of the refactoringListener, and send as a parameter the list of tokens to the class
    my_listener = FactoryMethodRefactoringListener(common_token_stream=token_stream,
                                                   creator_identifier='FactoryMethod',
                                                   products_identifier=['JpegReader', 'GifReader'])
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open('../tests/factory1/FactoryExample.refactored.java', mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())


# Test driver
if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=r'FactoryExample.java')
    args = argparser.parse_args()
    main(args)
