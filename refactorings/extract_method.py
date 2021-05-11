from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class ExtractMethodRefactoring(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, class_name: str = "Main"):
        self.code = ""
        self.refactor_class_name = class_name
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_re_writer = TokenStreamRewriter(common_token_stream)

        self.statements = {}
        self.is_in_target_class = False
        self.current_method_name = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER() == self.refactor_class_name:
            self.is_in_target_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER() == self.refactor_class_name:
            self.is_in_target_class = False

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.current_method_name = ctx.IDENTIFIER()
        self.statements[self.current_method_name] = []

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        pass

    def enterStatement15(self, ctx: JavaParserLabeled.Statement0Context):
        self.statements[self.current_method_name].append(ctx)

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        s = []
        for method_name in self.statements.keys():
            print(method_name)
            statements = self.statements[method_name]
            for statement in statements:
                s.append(statement)
                print(statement.getText())
            print("------------------")

        print(list(map(lambda x: x.getText(), s)))

        self.token_stream_re_writer.insertAfter(
            index=ctx.stop.tokenIndex,
            text=self.code
        )


if __name__ == "__main__":
    input_file = r"C:\Users\Amin\MAG\_term_6\CodART\tests\extract_method\input_file.java"
    output_file = r"C:\Users\Amin\MAG\_term_6\CodART\tests\extract_method\output_file.java"

    stream = FileStream(input_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = ExtractMethodRefactoring(common_token_stream=token_stream, class_name="Student")
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(output_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_re_writer.getDefaultText())
