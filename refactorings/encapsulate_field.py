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
        self.set_field = False
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')
#
#     def exitFieldDeclaration(self, ctx: Java9_v2Parser.FieldDeclarationContext):
#         if ctx.variableDeclaratorList().getText() == self.field_identifier:
#             if ctx.fieldModifier(0).getText() == 'public':
#                 self.token_stream_rewriter.replaceRange(
#                     from_idx=ctx.fieldModifier(0).start.tokenIndex,
#                     to_idx=ctx.fieldModifier(0).stop.tokenIndex,
#                     text='private')
#
#             # generate accessor and mutator methods
#             # Accessor body
#             new_code = '\n\t'
#             new_code += 'public ' + ctx.unannType().getText() + ' get' + str.capitalize(self.field_identifier)
#             new_code += '() { \n\t\t return this.' + self.field_identifier + ';' + '\n\t}'
#
#             # Mutator body
#             new_code += '\n\t'
#             new_code += 'public void set' + str.capitalize(self.field_identifier)
#             new_code += '(' + ctx.unannType().getText() + ' ' + self.field_identifier + ') { \n\t\t'
#             new_code += 'this.' + self.field_identifier + ' = ' + self.field_identifier + ';' + '\n\t}\n'
#
#             self.token_stream_rewriter.insertAfter(ctx.stop.tokenIndex, new_code)
#
#             hidden = self.token_stream.getHiddenTokensToRight(ctx.stop.tokenIndex)
#             self.token_stream_rewriter.replaceRange(from_idx=hidden[0].tokenIndex,
#                                                     to_idx=hidden[-1].tokenIndex,
#                                                     text='\t/*End of accessor and mutator methods!*/\n\n')
#
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
    def exitExpression0(self, ctx:JavaParserLabeled.Expression0Context):
        # if ctx.getChildCount() == 2:
        try:
            if ctx.parentCtx.getChild(1).getText() in ('=','+=', '-=', '*=', '/=',
                                                       '&=', '|=', '^=', '>>=',
                                                       '>>>=', '<<=', '%=') and \
                    ctx.parentCtx.getChild(0) == ctx:
                return
        except:
            pass
        if ctx.getText() == self.field_identifier:
            new_code = 'this.get' + str.capitalize(self.field_identifier) + '()'
            self.token_stream_rewriter.replaceRange(ctx.start.tokenIndex, ctx.stop.tokenIndex, new_code)

    def exitExpression1(self, ctx:JavaParserLabeled.Expression1Context):
        # if ctx.getChildCount() == 2:
        try:
            if ctx.parentCtx.getChild(1).getText() in ('=','+=', '-=', '*=', '/=',
                                                       '&=', '|=', '^=', '>>=',
                                                       '>>>=', '<<=', '%=') and \
                    ctx.parentCtx.getChild(0) == ctx:
                return
        except:
            pass
        if ctx.getText() == 'this.' + self.field_identifier:
            new_code = 'this.get' + str.capitalize(self.field_identifier) + '()'
            self.token_stream_rewriter.replaceRange(ctx.start.tokenIndex, ctx.stop.tokenIndex, new_code)

    def enterCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        hidden = self.token_stream.getHiddenTokensToLeft(ctx.start.tokenIndex)
        self.token_stream_rewriter.replaceRange(from_idx=hidden[0].tokenIndex,
                                                to_idx=hidden[-1].tokenIndex,
                                                text='/*After refactoring (Refactored version)*/\n')



def main():
    Path = "../tests/encapsulate_field_tests/"
    test_file = FileStream(str(Path + "use_field_propagation_test.java"))
    print("file opened")
    Refactored = open(os.path.join(Path, "use_field_propagation_test_refactored.java"), 'w', newline='')

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
