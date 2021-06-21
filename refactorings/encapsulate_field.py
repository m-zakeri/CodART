"""
The module implements encapsulate field refactoring in
response to `Deficient Encapsulation` design smell.

## References
[1] G. Suryanarayana, G. Samarthyam, and T. Sharma, Refactoring for software design smells: managing technical debt,
1st ed. San Francisco, CA, USA: Morgan Kaufmann Publishers Inc., 2014.


"""

__version__ = '0.1.0'
__author__ = 'Morteza'

import os

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaLexer import JavaLexer


class EncapsulateFiledRefactoringListener(JavaParserLabeledListener):
    """
    To implement the encapsulate filed refactored
    Encapsulate field: Make a public field private and provide accessors
    """
#
    def __init__(self, common_token_stream: CommonTokenStream = None,
                 field_identifier: str = None):
        """
        :param common_token_stream:
        """
        self.token_stream = common_token_stream
        self.field_identifier = field_identifier
        self.getter_exist = False
        self.setter_exist = False
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if ctx.variableDeclarators().getText() == self.field_identifier:
            if not ctx.parentCtx.parentCtx.modifier(0):
                self.token_stream_rewriter.insertBeforeIndex(
                     index=ctx.typeType().stop.tokenIndex,
                     text='private ')

            elif ctx.parentCtx.parentCtx.modifier(0).getText() == 'public':
                self.token_stream_rewriter.replaceRange(
                    from_idx=ctx.parentCtx.parentCtx.modifier(0).start.tokenIndex,
                    to_idx=ctx.parentCtx.parentCtx.modifier(0).stop.tokenIndex,
                    text='private')
            else:
                return

            for c in ctx.parentCtx.parentCtx.parentCtx.classBodyDeclaration():
                try:
                    print('method name: ' + c.memberDeclaration().methodDeclaration().IDENTIFIER().getText())
                    if c.memberDeclaration().methodDeclaration().IDENTIFIER().getText() == 'get' + str.capitalize(self.field_identifier):
                        self.getter_exist = True
                    if c.memberDeclaration().methodDeclaration().IDENTIFIER().getText() == 'set' + str.capitalize(self.field_identifier):
                        self.setter_exist = True
                except :
                    print("not method !!!")

            print("setter find: " + str(self.setter_exist))
            print("getter find: " + str(self.getter_exist))

            # generate accessor and mutator methods
            # Accessor body
            new_code = ''
            if not self.getter_exist:
                new_code = '\n\t// new getter method\n\t'
                new_code += 'public ' + ctx.typeType().getText() + ' get' + str.capitalize(self.field_identifier)
                new_code += '() { \n\t\treturn this.' + self.field_identifier + ';' + '\n\t}\n'

            # Mutator body
            if not self.setter_exist:
                new_code += '\n\t// new setter method\n\t'
                new_code += 'public void set' + str.capitalize(self.field_identifier)
                new_code += '(' + ctx.typeType().getText() + ' ' + self.field_identifier + ') { \n\t\t'
                new_code += 'this.' + self.field_identifier + ' = ' + self.field_identifier + ';' + '\n\t}\n'

            self.token_stream_rewriter.insertAfter(ctx.stop.tokenIndex, new_code)

            hidden = self.token_stream.getHiddenTokensToRight(ctx.stop.tokenIndex)
            # self.token_stream_rewriter.replaceRange(from_idx=hidden[0].tokenIndex,
            #                                         to_idx=hidden[-1].tokenIndex,
            #                                         text='\n\t/*End of accessor and mutator methods!*/\n\n')

#     def exitAssignment(self, ctx: Java9_v2Parser.AssignmentContext):
#         if ctx.leftHandSide().getText() == self.field_identifier or \
#                 ctx.leftHandSide().getText() == 'this.' + self.field_identifier:
#             expr_code = self.token_stream_rewriter.getText(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
#                                                            start=ctx.expression().start.tokenIndex,
#                                                            stop=ctx.expression().stop.tokenIndex)
#             # new_code = 'this.set' + str.capitalize(self.field_identifier) + '(' + ctx.expression().getText() + ')'
#             new_code = 'this.set' + str.capitalize(self.field_identifier) + '(' + expr_code + ')'
#             self.token_stream_rewriter.replaceRange(ctx.start.tokenIndex, ctx.stop.tokenIndex, new_code)
#
#     def exitPrimary(self, ctx: Java9_v2Parser.PrimaryContext):
#         if ctx.getChildCount() == 2:
#             if ctx.getText() == 'this.' + self.field_identifier or ctx.getText() == self.field_identifier:
#                 new_code = 'this.get' + str.capitalize(self.field_identifier) + '()'
#                 self.token_stream_rewriter.replaceRange(ctx.start.tokenIndex, ctx.stop.tokenIndex, new_code)
#
#     def enterCompilationUnit1(self, ctx: Java9_v2Parser.CompilationUnit1Context):
#         hidden = self.token_stream.getHiddenTokensToLeft(ctx.start.tokenIndex)
#         self.token_stream_rewriter.replaceRange(from_idx=hidden[0].tokenIndex,
#                                                 to_idx=hidden[-1].tokenIndex,
#                                                 text='/*After refactoring (Refactored version)*/\n')


def main():
    Path = "../tests/encapsulate_field_tests/"
    test_file = FileStream(str(Path + "input.java"))
    print("file opened")
    Refactored = open(os.path.join(Path, "inputRefactored1.java"), 'w', newline='')

    Lexer = JavaLexer(test_file)

    TokenStream = CommonTokenStream(Lexer)

    Parser = JavaParserLabeled(TokenStream)

    EFlistener = EncapsulateFiledRefactoringListener(TokenStream, 'f')
    Tree = Parser.compilationUnit()

    Walker = ParseTreeWalker()
    Walker.walk(t=Tree, listener=EFlistener)

    Refactored.write(EFlistener.token_stream_rewriter.getDefaultText())
    print("finished!!!!!!!!")


if __name__ == "__main__":
    main()
