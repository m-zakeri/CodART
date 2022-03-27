"""
The script implements automated refactoring to visitor design pattern
"""
__version__ = '1.4.2'
__author__ = 'Nader Mesbah'
__date__ = '20210108'

import argparse
from time import time

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class VisitorPatternRefactoringListener(JavaParserLabeledListener):
    """
    implement the visitor pattern refactoring
    """

    def __init__(self, common_token_stream: CommonTokenStream = None,
                 SuperClass_identifier: str = None,
                 SubClass_identifier: list = None):
        """
        :param common_token_stream:
        """
        self.enter_class = False
        self.token_stream = common_token_stream
        self.SuperClass_identifier = SuperClass_identifier
        self.SubClass_identifier = SubClass_identifier
        self.InSuperClass = False
        self.InSubClass = False
        self.InMainClass = False
        self.CurrentCC = None
        self.Visitors = {}
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.SuperClass_identifier:
            self.InSuperClass = True
        elif ctx.IDENTIFIER().getText() in self.SubClass_identifier:
            self.InSubClass = True
        elif ctx.IDENTIFIER().getText() == "Main":
            self.InMainClass = True

        if ctx.EXTENDS().__str__() == "extends":
            # SubClass Headers Rename
            self.token_stream_rewriter.insertAfter(ctx.start.tokenIndex + 4, "implements")
            self.token_stream_rewriter.deleteIndex(ctx.start.tokenIndex + 4)

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.InSuperClass == True:
            # SuperClass Interface Make
            InterfaceText = "interface " + self.SuperClass_identifier + "\n{\n\tpublic void accept (Visitor" \
                            + self.SuperClass_identifier + " visitor);\n}"
            self.token_stream_rewriter.insertAfter(ctx.start.tokenIndex - 1, "\n" + InterfaceText + "\n")

            # SuperClass Visitor interface Make
            InterfaceTextVistor = "interface Visitor" + self.SuperClass_identifier + "\n{"
            index = 0
            for item in self.Visitors:
                InterfaceTextVistor += "\n\t" + "public void " + "visit(" + self.SubClass_identifier[
                    index] + " " + item + ");"
                index += 1
            InterfaceTextVistor += "\n}"
            self.token_stream_rewriter.insertAfter(ctx.start.tokenIndex - 1, "\n" + InterfaceTextVistor + "\n")
            # SuperClass DoVisitor Make
            newSC = "\nclass DoVisitor" + self.SuperClass_identifier + " implements Visitor" + self.SuperClass_identifier + "\n{"
            methodbody = ""
            index = 0
            # SuperClassDoVisitor Mathods Make
            for item in self.Visitors:
                methodbody = str_list(self.Visitors[item])
                methodbody = "{\n\t" + methodbody[2:-2] + "\n\t}"
                newSC += "\n\t" + "@Override\n\tpublic void visit(" + self.SubClass_identifier[
                    index] + " " + item + ")\n\t" + methodbody
                index += 1
            newSC += "\n}"
            self.token_stream_rewriter.replaceRange(ctx.start.tokenIndex, ctx.stop.tokenIndex, newSC)
        self.InSuperClass = False
        self.InSubClass = False
        self.InMainClass = False

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        # Extract Methods Name & Methods body of SuperClass
        if self.InSuperClass == True:
            newClassName = ctx.IDENTIFIER().getText()
            newMethodBody = ctx.methodBody().getText()
            self.Visitors[newClassName] = [newMethodBody]

    def exitClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        if self.InSubClass == True:
            # Implement Mathod of SuperClass InterFace
            OverrideText = "@Override\n\tpublic void accept(Visitor" + self.SuperClass_identifier + \
                           " visitor)\n\t{\n\t\tvisitor.visit(this);\n\t}"
            self.token_stream_rewriter.insertAfter(ctx.start.tokenIndex, "\n\t" + OverrideText)

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        if self.InMainClass == True:
            # Modify Main Method
            if ctx.IDENTIFIER().getText() in self.Visitors:
                self.token_stream_rewriter.replaceRange(
                    from_idx=ctx.start.tokenIndex,
                    to_idx=ctx.stop.tokenIndex,
                    text="accept(new DoVisitor" + self.SuperClass_identifier + "())")


def main(args):
    # Step 1: Load input source into stream
    begin_time = time()
    stream = FileStream(args.file, encoding='utf8', errors='ignore')
    # input_stream = StdinStream()
    print('Input stream:')
    print(stream)

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
    my_listener = VisitorPatternRefactoringListener(common_token_stream=token_stream,
                                                    SuperClass_identifier='SC',
                                                    SubClass_identifier=['CC1', 'CC2', 'CC3'])
    #                                                    SuperClass_identifier='ComputerPart',
    #                                                    SubClass_identifier=['Keyboard', 'Monitor', 'Mouse', 'Computer'])
    #                                                    SuperClass_identifier='Shape',
    #                                                    SubClass_identifier=['Polygon', 'Rectangle','Arrow'])

    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    print('Compiler result:')
    print(my_listener.token_stream_rewriter.getDefaultText())

    with open('../tests/visitor1/VisitorExample0.refactored.java', mode='w', newline='') as f:
        #   with open('VisitorExample1.refactored.java', mode='w', newline='') as f:
        #    with open('VisitorExample2.refactored.java', mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())

    end_time = time()
    print("time execution : ", end_time - begin_time)


# Test driver
if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=r'VisitorExample0.java')
    #        help='Input source', default=r'VisitorExample1.java')
    #        help='Input source', default=r'VisitorExample2.java')
    args = argparser.parse_args()
    main(args)
