from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.java.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

# get method parameters with formalParameters().formalParameterList()
# formal parameters are those which are in method declaration
# parameter in method call are from expressionList/expression
"""
To implement replace parameter with query refactoring:
with consider of removable parameters, find new object in method declaration
Delete target parameters in both method call and declaration
Insert removed parameters in method body.
"""


class ReplaceParameterWithQueryListener(JavaParserLabeledListener):
    # constructor
    def __init__(self, common_token_stream: CommonTokenStream = None,
                 target_class: str = None, target_method: str = None,
                 target_parameters: list = None):

        if common_token_stream is None:
            raise ValueError("common token stream is None")
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
        self.target_method_obj = None
        self.removed_expressions = []
        self.local_variables = []
        self.add_to_target_method = []
        self.index_of_parameter = 0

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.current_class = ctx.IDENTIFIER().getText()

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.current_class = None

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.current_method = ctx.IDENTIFIER().getText()
        if self.current_method == self.target_method and self.current_class == self.target_class:
            self.target_method_obj = ctx

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.FindObjrctIndex()

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        self.current_method = ctx.IDENTIFIER().getText()
        if self.current_method == self.target_method and self.current_class == self.target_class:
            self.target_method_obj = ctx

    def exitConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        self.FindObjrctIndex()

    def FindObjrctIndex(self):
        i = 0
        for expression in self.removed_expressions:
            # print("expression",expression.getText())
            if type(expression) is JavaParserLabeled.Expression0Context and \
                    type(expression.primary()) is JavaParserLabeled.Primary4Context:
                self.removeExpression(expression)
            else:
                self.add_to_target_method.append(expression.getText())
                # find index of target object
                self.index_of_parameter = i
            i += 1
        self.removed_expressions = []
        self.local_variables = []
        self.current_method = None

    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        self.local_variables.append(ctx.getText())
        # print(self.local_variables)

    # delete in method call
    def removeExpression(self, expression):
        for local_variable in self.local_variables:
            flag = False
            variable_declarator = local_variable.variableDeclarators()
            # print("$" ,variable_declarator.children)
            remaining_variables = []
            for i in range(len(variable_declarator.children)):
                if i % 2 == 0:
                    vd = variable_declarator.children[i]
                    if expression.getText() != vd.variableDeclaratorId().getText():
                        remaining_variables.append(vd.getText())
                    else:
                        self.add_to_target_method.append(vd.variableInitializer().getText())
                        flag = True

            if len(remaining_variables) == 0:
                parent_ctx = local_variable.parentCtx
                # print("parent",parent_ctx)
                self.token_stream_rewriter.delete(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=parent_ctx.start.tokenIndex,
                    to_idx=parent_ctx.stop.tokenIndex
                )
            elif len(remaining_variables) < (len(variable_declarator.children) + 1) // 2:
                self.token_stream_rewriter.replaceRange(
                    from_idx=variable_declarator.start.tokenIndex,
                    to_idx=variable_declarator.stop.tokenIndex,
                    text=f"{', '.join(remaining_variables)}"
                )

            if flag:
                break

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        self.current_method_call = ctx.IDENTIFIER().getText()

    def exitMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        self.current_method_call = None

    # in method call
    def enterExpressionList(self, ctx: JavaParserLabeled.ExpressionListContext):
        if self.current_method_call == self.target_method:
            # print("ex",ctx.getText())
            expressions = []
            for i in range(len(ctx.children)):
                if i % 2 == 0:
                    if (i // 2) in self.target_parameters:
                        self.removed_expressions.append(ctx.children[i])
                    else:
                        expressions.append(ctx.children[i].getText())
                        # print(expressions)
                # else => ctx.children = ,
            self.token_stream_rewriter.replaceRange(
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex,
                text=f"{', '.join(expressions)}"
            )

    # method body
    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        temp = ""
        if self.target_method_obj is not None:
            print("self", self.index_of_parameter)
            # declaration
            ctx = self.target_method_obj
            text = ''
            formal_parameter_list = ctx.formalParameters().formalParameterList()
            print("b", ctx.formalParameters().formalParameterList().getText()[1])
            survived_parameters = []
            for j in range(len(formal_parameter_list.children)):
                # find object name to gain the name, insetr obj name in local variables
                if j % 2 == 0:
                    if (j // 2) not in self.target_parameters:
                        if j // 2 == self.index_of_parameter:
                            parameter = formal_parameter_list.children[j]
                            parameter_vdi = parameter.variableDeclaratorId().getText()
                            temp = parameter_vdi
            for i in range(len(formal_parameter_list.children)):
                if i % 2 == 0:
                    if (i // 2) in self.target_parameters:
                        parameter = formal_parameter_list.children[i]
                        parameter_type = parameter.typeType().getText()
                        parameter_vdi = parameter.variableDeclaratorId().getText()
                        print("i", i)
                        print("target", parameter_vdi)
                        parameter_initializer = self.add_to_target_method[0]
                        text += parameter_type + ' ' + parameter_vdi + ' = ' + temp + '.' + parameter_vdi \
                                + ';' + "\n" + "\t" + "\t"
                        self.add_to_target_method.remove(parameter_initializer)

                    else:
                        parameter = formal_parameter_list.children[i]
                        parameter_type = parameter.typeType().getText()
                        parameter_vdi = parameter.variableDeclaratorId().getText()
                        survived_parameters.append(parameter_type + ' ' + parameter_vdi)
            # delete in declarition
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
        listener = ReplaceParameterWithQueryListener(
            common_token_stream=self.token_stream,
            target_class=self.target_class,
            target_method=self.target_method,
            target_parameters=self.target_parameters
        )
        self.walker.walk(
            listener=listener,
            t=self.tree
        )
        print(listener.add_to_target_method)
        print(listener.token_stream_rewriter.getDefaultText())
        with open(self.new_file_path, mode="w", newline="") as f:
            f.write(listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    ReplaceParameterWithQueryAPI(
        file_path="/data/Dev/JavaSample/src/ReplaceParameterWithQuery.java",
        target_class='ReplaceParameterWithQuery',
        target_method="availableVacation",
        target_parameters=[1, ],
        # index from 0
    ).do_refactor()
