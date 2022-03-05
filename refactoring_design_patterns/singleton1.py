"""
This module implements automated refactoring to singleton design pattern

"""

__version__ = '1.0.0'
__author__ = 'Morteza Zakeri'

import os
import time
import argparse
from shutil import copy2


from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener



class SingletonRefactoringListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream = None,
                 class_identifier: str = None):
        """
        :param common_token_stream:
        """
        self.enter_class = False
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        self.ObjectIndex = []
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.class_identifier:
            self.enter_class = True
            new_code = "\n\tprivate static " + self.class_identifier + " Instance = null;\n\t"
            self.token_stream_rewriter.insertAfter(ctx.classBody().start.tokenIndex + 1, new_code)
            self.addInstance = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.enter_class == True:
            self.enter_class = False
            new_code = "\n\tpublic static " + self.class_identifier + " getInstance()\n\t{\n\t\tif (Instance == null)" \
                                                                      "\n\t\t\tInstance = new " + self.class_identifier + "();" \
                                                                                                                          "\n\t\treturn Instance;\n\t}\n"
            self.token_stream_rewriter.insertAfter(ctx.stop.tokenIndex - 1, new_code)

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        if self.enter_class == True:
            constructorModifier = ctx.parentCtx.parentCtx
            if constructorModifier.start.text == 'public':
                self.token_stream_rewriter.replaceRange(
                    from_idx=constructorModifier.start.tokenIndex,
                    to_idx=constructorModifier.start.tokenIndex,
                    text='private')

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if self.enter_class == False:
            A = ctx.parentCtx.parentCtx
            B = ctx.variableDeclarators()
            if ctx.start.text == self.class_identifier:
                start = ctx.variableDeclarators().variableDeclarator(0).ASSIGN().symbol.tokenIndex + 1
                end = ctx.stop.tokenIndex
                self.ObjectIndex.append([start, end])

    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        if self.enter_class == False:
            if ctx.start.text == self.class_identifier:
                start = ctx.variableDeclarators().variableDeclarator(0).ASSIGN().symbol.tokenIndex + 1
                end = ctx.stop.tokenIndex
                self.ObjectIndex.append([start, end])

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        for item in self.ObjectIndex:
            self.token_stream_rewriter.replaceRange(from_idx=item[0],
                                                    to_idx=item[1],
                                                    text=" " + self.class_identifier + ".getInstance()")




def main(args, i):
    # Step 1: Load input source into stream
    stream = FileStream(args.file, encoding='utf8')
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
    # my_listener = EncapsulateFiledRefactoringListener(common_token_stream=token_stream, class_identifier='A')
    my_listener = SingletonRefactoringListener(common_token_stream=token_stream, class_identifier='GeneralPurposeBit')
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    newpath = "Refactored" + args.file
    if not os.path.exists(os.path.dirname(newpath)):
        try:
            os.makedirs(os.path.dirname(newpath))
        except OSError as exc:  # Guard against race condition
            pass
    with open(newpath, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())


# Test driver
if __name__ == '__main__':
    start_time = time.time()
    ProgramPath = r"."
    i = 0
    for root, d, f in os.walk(ProgramPath):
        for file in f:
            if file.endswith(".java"):
                try:
                    FilePath = os.path.join(root, file)
                    print("Success: ", FilePath)
                    argparser = argparse.ArgumentParser()
                    argparser.add_argument(
                        '-n', '--file', default=FilePath)
                    args = argparser.parse_args()
                    main(args, i)
                except:
                    print("Error: ", os.path.join(root, file))
            else:
                FilePath = os.path.join(root, file)
                NewFilePath = "Refactored" + root
                if not os.path.exists(NewFilePath):
                    os.makedirs(NewFilePath)

                copy2(FilePath, NewFilePath)

    print("--- %s seconds ---" % (time.time() - start_time))
