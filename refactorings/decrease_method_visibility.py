"""


"""

__version__ = '0.1.0'
__author__ = 'IUST-Students'

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

from utilization.setup_understand import *


class DecreaseMethodVisibilityRefactoringListener(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class=None, method_name=None):

        if method_name is None:
            self.method_name = []
        else:
            self.method_name = method_name

        if source_class is None:
            self.source_class = []
        else:
            self.source_class = source_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_source_class = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):

        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = True
        else:
            self.is_source_class = False

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.is_source_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        method_identifier = ctx.IDENTIFIER().getText()
        if self.method_name in method_identifier:
            if grand_parent_ctx.modifier() == []:
                self.token_stream_rewriter.replaceRange(
                    from_idx=ctx.typeTypeOrVoid().start.tokenIndex,
                    to_idx=ctx.typeTypeOrVoid().stop.tokenIndex,
                    text='public ' + ctx.typeTypeOrVoid().getText()
                )
            elif grand_parent_ctx.modifier(0).getText() == 'private':
                self.token_stream_rewriter.replaceRange(
                    from_idx=grand_parent_ctx.modifier(0).start.tokenIndex,
                    to_idx=grand_parent_ctx.modifier(0).stop.tokenIndex,
                    text='public')
            elif grand_parent_ctx.modifier(0).getText() != 'public':
                self.token_stream_rewriter.replaceRange(
                    from_idx=grand_parent_ctx.modifier(0).start.tokenIndex,
                    to_idx=grand_parent_ctx.modifier(0).stop.tokenIndex,
                    text='public ' + grand_parent_ctx.modifier(0).getText())


def main():
    udb_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    source_class = "App"
    method_name = "testMethod"
    # initialize with understand
    main_file = ""
    db = und.open(udb_path)
    for cls in db.ents("class"):
        if cls.simplename() == source_class:
            main_file = cls.parent().longname()

    stream = FileStream(main_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = DecreaseMethodVisibilityRefactoringListener(common_token_stream=token_stream,
                                                              source_class=source_class,
                                                              method_name=method_name)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(main_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())
