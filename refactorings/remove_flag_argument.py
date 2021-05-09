from gen.javaLabeled.JavaLexer import JavaLexer

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class RemoveFlagArgumentListener(JavaParserLabeledListener):
    """

    To remove boolean flag argument which specifies method logic in if and else block .
    For more information visit Martin Frauler book .

    if(flag)
    {

    }
    else
    {

    }

    """

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class="", source_method="",
                 argument_name: str = ""):

        self.argument_name = argument_name
        self.source_method = source_method
        self.source_class = source_class

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_source_class = False
        self.is_source_method = False
        self.is_if_block = False
        self.is_else_block = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        print("Refactoring started, please wait...")
        self.is_source_class = (ctx.IDENTIFIER().getText() == self.source_class)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.is_source_method = (ctx.IDENTIFIER().getText() == self.source_method)

    def enterMethodBody(self, ctx: JavaParserLabeled.MethodBodyContext):
        pass

    def enterStatement0(self, ctx: JavaParserLabeled.Statement0Context):

        if self.is_source_method:
            self.body_1 = ctx.block().getText()

    def enterStatement2(self, ctx: JavaParserLabeled.Statement2Context):

        if self.is_source_method:
            primary = ctx.parExpression().expression().primary()
            if hasattr(primary, "IDENTIFIER"):
                if ctx.parExpression().expression().primary().IDENTIFIER().getText() == self.argument_name :

                    iterator = iter(ctx.statement())

                    # self.body_1 = next(iterator).block().getText()
                    # self.body_2 = next(iterator).block().getText()

                    self.body_1 = ctx.statement()[0].block().getText()
                    self.body_2 = ctx.statement()[1].block().getText()

                    # for s in ctx.statement():
                    #     print(s.block().getText())

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        if not self.is_source_class:
            return None
        field_identifier = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText()
        # print("field_identifier:::::::::",field_identifier)
        if self.field_name in field_identifier:
            grand_parent_ctx = ctx.parentCtx.parentCtx
            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=grand_parent_ctx.start.tokenIndex,
                to_idx=grand_parent_ctx.stop.tokenIndex
            )
            self.detected_field = None

            print("Finished Processing...")


if __name__ == '__main__':
    # udb_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    source_class = "Playground"
    field_name = "push_down_field"
    source_method = "DeliveryDate"
    # initialize with understand
    main_file = "playground.java"

    # db = und.open(udb_path)
    # for cls in db.ents("class"):
    #     if cls.simplename() == source_class:
    #         main_file = cls.parent().longname()

    stream = FileStream(main_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = RemoveFlagArgumentListener(common_token_stream=token_stream, source_class=source_class,
                                             source_method=source_method,
                                             argument_name='b')
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    print(my_listener.body_1)
    print(my_listener.body_2)


    # with open(main_file, mode='w', newline='') as f:
    #     f.write(my_listener.token_stream_rewriter.getDefaultText())
