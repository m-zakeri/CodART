from gen.javaLabeled.JavaLexer import JavaLexer

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class MakeConcreteClassRefactoringListener(JavaParserLabeledListener):
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

    def enterTypeDeclaration(self, ctx: JavaParserLabeled.TypeDeclarationContext):

        if self.objective_class == ctx.classDeclaration().IDENTIFIER().getText():
            for i in range(0, len(ctx.classOrInterfaceModifier())):
                if ctx.classOrInterfaceModifier(i).getText() == "abstract":
                    self.token_stream_rewriter.replaceRange(
                        from_idx=ctx.classOrInterfaceModifier(i).start.tokenIndex,
                        to_idx=ctx.classOrInterfaceModifier(i).stop.tokenIndex,
                        text=""
                    )

    # def enterFieldDeclaration(self, ctx:JavaParserLabeled.FieldDeclarationContext):
    #     if self.is_source_class:
    #         #get list of variable and check
    #         class_identifier = ctx.variableDeclarators().getText().split(",")
    #         if "f" in  class_identifier:
    #             ctx1=ctx.parentCtx.parentCtx
    #             start_index = ctx1.start.tokenIndex
    #             stop_index = ctx1.stop.tokenIndex
    #             self.field_text = self.token_stream_rewriter.getText(
    #                 program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
    #                 start=start_index,
    #                 stop=stop_index)
    #
    #             self.token_stream_rewriter.delete(
    #                 program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
    #                 from_idx=ctx1.start.tokenIndex,
    #                 to_idx=ctx1.stop.tokenIndex
    #             )
    #         print(self.field_text)
    #
    # def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
    #     #get class name and check
    #     class_identifier = ctx.IDENTIFIER().getText()
    #     if class_identifier == self.objective_class:
    #         self.is_objective_class = True
    #         print('mids')
    #     else:
    #         self.is_objective_class = False
    # #
    # def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
    #     ctx1=ctx.parentCtx
    #     class_identifier = ctx1.IDENTIFIER().getText()
    #     if class_identifier in self.children_class:
    #         # if not self.is_source_class:
    #             self.token_stream_rewriter.replaceRange(
    #                 from_idx=ctx.start.tokenIndex+1,
    #                 to_idx=ctx.start.tokenIndex+1,
    #                 text="\n"+self.field_text+"\n"
    #             )


class PropagationMakeConcreteClassRefactoringListener(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, Source_class=None, using_variable_name=None,
                 used_method_name=None, propagated_class_name=None):

        if Source_class is None:
            self.source_class = []
        else:
            self.source_class = Source_class

        if used_method_name is None:
            self.using_method_name = []
        else:
            self.using_method_name = used_method_name

        if using_variable_name is None:
            self.using_variable_name = []
        else:
            self.using_variable_name = using_variable_name

        if propagated_class_name is None:
            self.propagated_class_name = []
        else:
            self.propagated_class_name = propagated_class_name

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_class = False
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.object = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        print("Propagation started, please wait...")
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier in self.propagated_class_name:
            self.is_class = True
        else:
            self.is_class = False

        if class_identifier in self.propagated_class_name:
            self.token_stream_rewriter.replaceRange(from_idx=ctx.start.tokenIndex,
                                                    to_idx=ctx.typeType().stop.tokenIndex,
                                                    text=ctx.CLASS().getText() + ' ' + ctx.IDENTIFIER().getText()
                                                    )

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        if not self.is_class:
            return None
        self.object = 'obj' + str.capitalize(self.source_class)
        self.token_stream_rewriter.insertAfter(index=ctx.start.tokenIndex,
                                               text=self.NEW_LINE + self.TAB + self.TAB
                                                    + self.source_class + ' ' + self.object +
                                                    ' = ' + 'new ' + self.source_class + '(' + ')' + ';' + self.NEW_LINE,
                                               program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME
                                               )

    def enterVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        if not self.is_class:
            return None
        if ctx.variableDeclaratorId().IDENTIFIER().getText() in self.using_variable_name:
            count = ctx.getChildCount()
            if count == 3:
                self.token_stream_rewriter.insertBefore(index=ctx.variableInitializer().start.tokenIndex,
                                                        text=self.object + '.',
                                                        program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME
                                                        )

    def enterExpression(self, ctx: JavaParserLabeled.ExpressionContext):
        if not self.is_class:
            return None
        if ctx != None:
            if ctx.methodCall() != None:
                if ctx.methodCall().IDENTIFIER().getText() in self.using_method_name:
                    count = ctx.methodCall().getChildCount()
                    if count == 3:
                        self.token_stream_rewriter.insertBefore(index=ctx.start.tokenIndex,
                                                                text=self.object + '.',
                                                                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME
                                                                )


if __name__ == '__main__':
    udb_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    source_class = "Shape"
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
    my_listener = MakeConcreteClassRefactoringListener(common_token_stream=token_stream,
                                                       class_name=source_class)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(main_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())
