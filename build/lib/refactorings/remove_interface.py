from gen.javaLabeled.JavaLexer import JavaLexer

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class RemoveInterfaceRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, interface_name: str = None):


        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if interface_name is None:
            raise ValueError("source_class is None")
        else:
            self.objective_interface = interface_name

        self.is_objective_class = False

        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    def enterInterfaceDeclaration(self, ctx: JavaParserLabeled.InterfaceDeclarationContext):

        interface_identifier = ctx.IDENTIFIER().getText()
        print(interface_identifier)
        if self.objective_interface == interface_identifier:
            start_index = ctx.start.tokenIndex
            stop_index = ctx.stop.tokenIndex

            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=start_index,
                to_idx=stop_index
            )
            self.detected_method = None
    # def enterTypeDeclaration(self, ctx:JavaParserLabeled.TypeDeclarationContext):
    #
    #     interface_identifier = ctx.interfaceDeclaration().IDENTIFIER().getText()
    #     print(interface_identifier)
    #     if self.objective_interface == interface_identifier:
    #         start_index = ctx.start.tokenIndex
    #         stop_index = ctx.stop.tokenIndex
    #
    #         self.token_stream_rewriter.delete(
    #             program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
    #             from_idx=start_index,
    #             to_idx=stop_index
    #         )
    #         self.detected_method = None


if __name__ == '__main__':
    udb_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    source_class = "ExtractedInterface"
    # initialize with understand
    main_file = ""
    db = und.open(udb_path)
    for cls in db.ents("Interface"):
        if cls.simplename() == source_class:
            main_file = cls.parent().longname()

    stream = FileStream(main_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = RemoveInterfaceRefactoringListener(common_token_stream=token_stream,
                                                     interface_name=source_class)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(main_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())
