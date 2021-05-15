from gen.javaLabeled.JavaLexer import JavaLexer
import os

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
    This listener is used to capture needed pattern and edit source method and extract two distinct logic
    in if and else blog there are several key assumption made at this momenent that the argument should be
    boolean and there must only been used in if else block and the structure of if and else should be in
    block format and single line if and else are not supported
        
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class="", source_method="",
                 argument_name: str = ""):
        """create removeflaglistener to extract and edit needed pattern

        Args:
            common_token_stream (CommonTokenStream, optional): default token stream passed by higher level api. Defaults to None.
            source_class (str, optional): name of the class which method rests in. Defaults to "".
            source_method (str, optional): name of the method to be edited. Defaults to "".
            argument_name (str, optional): name of the boolean argument which branchs the logic. Defaults to "".

        Raises:
            ValueError: if no common token stream is find will be raised since its is essential to the process
        """
        self.argument_name = argument_name
        self.source_method = source_method
        self.source_class = source_class
        self.token_stream_rewriter_changed = False

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
            self.common_token_stream = common_token_stream

        self.is_source_class = False
        self.is_source_method = False
        self.is_if_block = False
        self.is_else_block = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        """check if the class is the source class
        Args:
            ctx (JavaParserLabeled.ClassDeclarationContext)
        """
        print("Refactoring started, please wait...")
        self.is_source_class = (ctx.IDENTIFIER().getText() == self.source_class)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        """check if this is the intended method if so capture signature and remove boolean argument
            
        Args:
            ctx (JavaParserLabeled.MethodDeclarationContext): 
        """
        self.is_source_method = (ctx.IDENTIFIER().getText() == self.source_method)
        if self.is_source_method:

            nextParam = None

            for idx, formalParameter in enumerate(ctx.formalParameters().formalParameterList().formalParameter()):
                if formalParameter.variableDeclaratorId().IDENTIFIER().getText() == self.argument_name:
                    self.argument_token = formalParameter
                    nextParam = ctx.formalParameters().formalParameterList().formalParameter()[idx + 1] \
                        if idx != len(ctx.formalParameters().formalParameterList().formalParameter()) - 1 else None
                    break

            if nextParam:
                self.token_stream_rewriter.replaceRange(self.argument_token.start.tokenIndex,
                                                        nextParam.start.tokenIndex - 1, '')
            else:
                self.token_stream_rewriter.replaceRange(self.argument_token.start.tokenIndex,
                                                        self.argument_token.stop.tokenIndex, '')

            self.signature = self.token_stream_rewriter.getText(self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                                ctx.start.tokenIndex, ctx.methodBody().start.tokenIndex)

            if self.token_stream_rewriter_changed == False:
                self.token_stream_rewriter = TokenStreamRewriter(self.common_token_stream)
                self.token_stream_rewriter_changed = True


    def exitMethodBody(self, ctx: JavaParserLabeled.MethodBodyContext):
        """after exiting the soure method create two new method for new method logics and call these in if and
        else block in the source method
        Args:
            ctx (JavaParserLabeled.MethodBodyContext)
        """
        if self.is_source_method:
            signature1 = self.signature.split('(')[0].rstrip() + 'IsTrue' + ' (' + ''.join(
                self.signature.split('(')[1:])
            signature2 = self.signature.split('(')[0].rstrip() + 'IsFalse' + ' (' + ''.join(
                self.signature.split('(')[1:])

            res = '\n\t' + signature1 + self.body_1 + '\n\t' + signature2 + self.body_2
            self.token_stream_rewriter.insertAfter(index=ctx.stop.tokenIndex, text=res)
            # self.token_stream_rewriter.insertAfter(index=ctx.stop.tokenIndex, text=self.body_2)
            # self.token_stream_rewriter.insertAfter(index=ctx.stop.tokenIndex, text=self.signature)
            # print(self.signature)

            arguments = [s.rstrip().split(' ')[-1] for s in signature1.split('(')[1].split(')')[0].split(',')]
            print("exit method")
            signature1_name = signature1.split('(')[0].rstrip().split()[-1]
            signature2_name = signature2.split('(')[0].rstrip().split()[-1]

            self.token_stream_rewriter.replaceRange(self.body_1_token.start.tokenIndex,
                                                    self.body_1_token.stop.tokenIndex,
                                                    '\t' + signature1_name + '( ' + ','.join(arguments) + ')')
            self.token_stream_rewriter.replaceRange(self.body_2_token.start.tokenIndex,
                                                    self.body_2_token.stop.tokenIndex,
                                                    '\t' + signature2_name + '( ' + ','.join(arguments) + ')')

    def enterStatement0(self, ctx: JavaParserLabeled.Statement0Context):
        if self.is_source_method:
            pass

    def enterStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        """when entering if else block we get both of the logic in the block if this was source method
            and capture the token which is needed later to do the refactoring
        Args:
            ctx (JavaParserLabeled.Statement2Context)
        """
        if self.is_source_method:

            try :
                primary = ctx.parExpression().expression().primary()
                if hasattr(primary, "IDENTIFIER"):
                    if ctx.parExpression().expression().primary().IDENTIFIER().getText() == self.argument_name:
                        iterator = iter(ctx.statement())

                        # TODO : handle on statements blocks .e.g. {}

                        self.body_1, self.body_2 = [self.common_token_stream.getText(s.block().start, s.block().stop)[1:]
                                                    for s
                                                    in ctx.statement()]

                        self.body_1_token, self.body_2_token = [s.block() for s in ctx.statement()]

                        # print(ctx.getPayload())
                        # print(self.common_token_stream.getText(ctx.start, ctx.stop))
                        # print(dir(ctx.statement()[0].block()))

                        # for s in ctx.statement():
                        #     print(s.block().getText())

            except :
                pass


class RemoveFlagArgument:
    """Refactoring API that can be used to to do remove flag argument 

    """

    def __init__(self, source_class="Playground", source_method="DeliveryDate", argument_name="b",
                 main_file="playground.java"):
        """create a removeflagargument refactor 

        Args:
            source_class (str): class name contaminated by code smell.
            source_mathod (str): method name contaminated.
            argument_name (str): boolean argument in method.
            main_file (str): path of main file containing source class.
        """

        self.source_class = source_class
        self.source_method = source_method
        self.arguemnt_name = argument_name
        self.main_file = main_file

        self.stream = FileStream(self.main_file, encoding='utf8')
        self.lexer = JavaLexer(self.stream)
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = JavaParserLabeled(self.token_stream)
        self.parser.getTokenStream()
        self.parse_tree = self.parser.compilationUnit()
        self.my_listener = RemoveFlagArgumentListener(common_token_stream=self.token_stream,
                                                      source_class=self.source_class,
                                                      source_method=self.source_method,
                                                      argument_name=self.arguemnt_name)

    def do_refactor(self):
        """removes flag argument logic and replace it by two method call of the new method generated from extracted
            login in if else block
        """
        walker = ParseTreeWalker()
        walker.walk(t=self.parse_tree, listener=self.my_listener)

        # self.my_listener.body_1

        with open(self.main_file, 'w') as f:
            f.write(self.my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    RemoveFlagArgument().do_refactor()

    RemoveFlagArgument("JSONArray", "addAll", "wrap",r"D:\Uni\Compiler\project\CodART\benchmark_projects\JSON\src\main\java\org\json\JSONArray.java" ).do_refactor()

