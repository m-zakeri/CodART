from gen.javaLabeled.JavaLexer import JavaLexer

try:
    import understand as und
except ImportError as e:
    print(e)
from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class RemoveMethodRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class=None, method_name:str = None):

        if method_name is None:
            self.method_name = ""
        else:
            self.method_name = method_name

        if source_class is None:
            self.source_class = ""
        else:
            self.source_class = source_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_source_class = False
        self.nested_level = -1
        self.method_found = False
        self.is_static = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = False

    def enterClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        if self.is_source_class is True:
            self.nested_level += 1

    def exitClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        if self.is_source_class is True:
            self.nested_level -= 1
        if not self.method_found or self.nested_level != -1:
            return None
        self.token_stream_rewriter.delete(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            from_idx=ctx.start.tokenIndex,
            to_idx=ctx.stop.tokenIndex
        )
        self.method_found = False

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.is_source_class or self.nested_level != 0:
            return None
        method_identifier = ctx.IDENTIFIER().getText()
        if self.method_name == method_identifier:
            self.method_found = True


if __name__ == '__main__':
    #udb_path = '/home/ali/Desktop/code/TestProject/TestProject.udb'
    source_class = "JSONArray"
    method_name = "optLong"
    # initialize with understand
    main_file = r"E:\UNI\Term6\Compiler\Project\CodART\benchmark_projects\JSON\src\main\java\org\json\JSONArray.java"
    #db = und.open(udb_path)
    #for cls in db.ents("class"):
    #    if cls.simplename() == source_class:
    #        main_file = cls.parent().longname()

    stream = FileStream(main_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = RemoveMethodRefactoringListener(common_token_stream=token_stream,
                                                  source_class=source_class,
                                                  method_name=method_name)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(main_file, mode='w', newline='', encoding='utf8') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())
