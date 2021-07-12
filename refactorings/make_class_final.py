from gen.javaLabeled.JavaLexer import JavaLexer

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class MakeFinalClassRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, class_name: str = None):


        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if class_name is None:
            raise ValueError("source_class is None")
        else:
            self.objective_class = class_name

        self.is_objective_class = False

        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):

        if self.objective_class == ctx.IDENTIFIER().getText():
            self.token_stream_rewriter.replaceRange(
                from_idx=0,
                to_idx=0,
                text= "final "+ctx.CLASS().getText()
            )
    # def enterTypeDeclaration(self, ctx:JavaParserLabeled.TypeDeclarationContext):
    #
    #     if self.objective_class == ctx.classDeclaration().IDENTIFIER().getText():
    #
    #         self.token_stream_rewriter.replaceRange(
    #             from_idx=ctx.classOrInterfaceModifier(0).start.tokenIndex,
    #             to_idx=ctx.classOrInterfaceModifier(0).stop.tokenIndex,
    #             text=ctx.classOrInterfaceModifier(0).getText()+" final"
    #         )


if __name__ == '__main__':
    udb_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    source_class = "Circle"
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
    my_listener = MakeFinalClassRefactoringListener(common_token_stream=token_stream,
                                                    class_name=source_class)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(main_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())
