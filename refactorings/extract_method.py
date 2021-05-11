from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


def is_equal(a, b):
    return str(a) == str(b)


class Statement:
    def __init__(self, statement, expressions):
        self.statement = statement
        self.expressions = expressions

    def __str__(self):
        return "[\n\tstatement: {}\n\texpressions: {}\n]".format(
            self.statement.getText(),
            list(map(lambda x: x.getText(), self.expressions))
        )


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
        self.is_in_a_method = False
        self.current_method_name = ""
        self.current_statement_index = 0

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if is_equal(ctx.IDENTIFIER(), self.refactor_class_name):
            self.is_in_target_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if is_equal(ctx.IDENTIFIER(), self.refactor_class_name):
            self.is_in_target_class = False

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_in_target_class:
            self.is_in_a_method = True
            self.current_method_name = ctx.IDENTIFIER()
            self.statements[self.current_method_name] = []

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.is_in_a_method = False

    def enterStatement15(self, ctx: JavaParserLabeled.Statement0Context):
        if self.is_in_target_class:
            if self.is_in_a_method:
                self.current_statement_index = len(self.statements[self.current_method_name])
                self.statements[self.current_method_name].append(
                    Statement(ctx, [])
                )

    # def enterExpression0(self, ctx: JavaParserLabeled.Expression0Context):
    #     if self.is_in_target_class:
    #         if self.is_in_a_method:
    #             print(self.current_statement_index)
    #             print(self.statements[self.current_method_name][self.current_statement_index])
    #             print(self.statements[self.current_method_name][self.current_statement_index].expressions)
    #             self.statements[self.current_method_name][self.current_statement_index].expressions.append(ctx)

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        for method_name in self.statements.keys():
            print(method_name)
            statements = self.statements[method_name]
            for statement in statements:
                print(str(statement))
            print("---------------")

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
