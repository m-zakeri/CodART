from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.java.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class ReplaceParameterWithQueryRefactoringListener(JavaParserLabeledListener):
    """
    To implement replace parameter with query refactoring based on its actors.
    Find usages of target method and remove target parameters from these and add the removed parameters to
    top of target method.
    """

    def __init__(self, common_token_stream: CommonTokenStream = None,
                 target_class: str = None, target_method: str = None,
                 target_parameters: list = None):

        if common_token_stream is None:
            raise ValueError("common_token_stream is None")
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if target_class is None:
            raise ValueError("target class is None")
        else:
            self.target_class = target_class

        if target_method is None:
            raise ValueError("target method is None")
        else:
            self.target_method = target_method

        if target_parameters is None:
            self.target_parameters = []
        else:
            self.target_parameters = target_parameters

        self.current_class = None
        self.current_method = None
        self.current_method_call = None
        self.target_method_ctx = None
        self.removed_expressions = []
        self.all_local_variable_declarators = []
        self.add_to_top_of_target_method = []

        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.current_class = ctx.IDENTIFIER().getText()

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.current_class = None

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.current_method = ctx.IDENTIFIER().getText()
        if self.current_method == self.target_method and self.current_class == self.target_class:
            self.target_method_ctx = ctx

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.exit_method_or_constructor()

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        self.current_method = ctx.IDENTIFIER().getText()
        if self.current_method == self.target_method and self.current_class == self.target_class:
            self.target_method_ctx = ctx

    def exitConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        self.exit_method_or_constructor()

    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        self.all_local_variable_declarators.append(ctx)

    def remove_expression_declaration(self, expression):
        for lvd in self.all_local_variable_declarators:
            flag = False
            vds = lvd.variableDeclarators()
            survived_vds = []
            for i in range(len(vds.children)):
                if i % 2 == 0:
                    vd = vds.children[i]
                    if expression.getText() != vd.variableDeclaratorId().getText():
                        survived_vds.append(vd.getText())
                    else:
                        self.add_to_top_of_target_method.append(vd.variableInitializer().getText())
                        flag = True

            if len(survived_vds) == 0:
                parent_ctx = lvd.parentCtx
                print(type(parent_ctx))
                self.token_stream_rewriter.delete(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=parent_ctx.start.tokenIndex,
                    to_idx=parent_ctx.stop.tokenIndex
                )
            elif len(survived_vds) < (len(vds.children) + 1) // 2:
                self.token_stream_rewriter.replaceRange(
                    from_idx=vds.start.tokenIndex,
                    to_idx=vds.stop.tokenIndex,
                    text=f"{', '.join(survived_vds)}"
                )

            if flag:
                break

    def exit_method_or_constructor(self):
        for expression in self.removed_expressions:
            if type(expression) is JavaParserLabeled.Expression0Context and\
                    type(expression.primary()) is JavaParserLabeled.Primary4Context:
                self.remove_expression_declaration(expression)

            else:
                self.add_to_top_of_target_method.append(expression.getText())

        self.removed_expressions = []
        self.all_local_variable_declarators = []
        self.current_method = None

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        self.current_method_call = ctx.IDENTIFIER().getText()

    def exitMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        self.current_method_call = None

    def enterExpressionList(self, ctx: JavaParserLabeled.ExpressionListContext):
        if self.current_method_call == self.target_method:

            parameters = []
            for i in range(len(ctx.children)):
                if i % 2 == 0:
                    if ((i // 2) + 1) in self.target_parameters:
                        self.removed_expressions.append(ctx.children[i])
                    else:
                        parameters.append(ctx.children[i].getText())

            self.token_stream_rewriter.replaceRange(
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex,
                text=f"{', '.join(parameters)}"
            )

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        if self.target_method_ctx is not None:
            ctx = self.target_method_ctx
            text = ''
            formal_parameter_list = ctx.formalParameters().formalParameterList()
            survived_parameters = []
            for i in range(len(formal_parameter_list.children)):
                if i % 2 == 0:
                    if ((i // 2) + 1) in self.target_parameters:
                        parameter = formal_parameter_list.children[i]
                        parameter_type = parameter.typeType().getText()
                        parameter_vdi = parameter.variableDeclaratorId().getText()
                        parameter_initializer = self.add_to_top_of_target_method[0]
                        text += \
                            parameter_type + ' ' + parameter_vdi + ' = ' + parameter_initializer +\
                            ';' + self.NEW_LINE + self.TAB + self.TAB
                        self.add_to_top_of_target_method.remove(parameter_initializer)

                    else:
                        parameter = formal_parameter_list.children[i]
                        parameter_type = parameter.typeType().getText()
                        parameter_vdi = parameter.variableDeclaratorId().getText()
                        survived_parameters.append(parameter_type + ' ' + parameter_vdi)

            self.token_stream_rewriter.replaceRange(
                from_idx=formal_parameter_list.start.tokenIndex,
                to_idx=formal_parameter_list.stop.tokenIndex,
                text=f"{', '.join(survived_parameters)}"
            )

            block_statement = ctx.methodBody().block().blockStatement()[0]
            self.token_stream_rewriter.insertAfter(
                index=block_statement.start.tokenIndex - 1,
                text=text
            )


class ReplaceParameterWithQueryAPI:

    def __init__(self, file_path, target_class, target_method, target_parameters):
        self.file_path = file_path
        self.new_file_path = file_path
        self.target_class = target_class
        self.target_method = target_method
        self.target_parameters = target_parameters
        self.stream = FileStream(self.file_path, encoding="utf8")
        self.lexer = JavaLexer(self.stream)
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = JavaParserLabeled(self.token_stream)
        self.tree = self.parser.compilationUnit()
        self.walker = ParseTreeWalker()

    def do_refactor(self):
        listener = ReplaceParameterWithQueryRefactoringListener(
            common_token_stream=self.token_stream,
            target_class=self.target_class,
            target_method=self.target_method,
            target_parameters=self.target_parameters
        )
        self.walker.walk(
            listener=listener,
            t=self.tree
        )

        print(listener.add_to_top_of_target_method)
        print(listener.token_stream_rewriter.getDefaultText())

        print(type(self.new_file_path))

        with open(self.new_file_path, mode="w", newline="") as f:
            f.write(listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    ReplaceParameterWithQueryAPI(
        file_path="C:\\Users\\asus\\Desktop\\desk\\University\\99002-CD (compiler)\\Project\\CodART\\"
                  "benchmark_projects\\JSON\\src\\main\\java\\org\\json\\JSONArray.java",
        target_class='JSONArray',
        target_method="optDouble",
        target_parameters=[2],
    ).do_refactor()
