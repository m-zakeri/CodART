from gen.javaLabeled.JavaLexer import JavaLexer

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class MakeAbstractClassRefactoringListener(JavaParserLabeledListener):
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

        print(ctx.IDENTIFIER().getText())
        if self.objective_class == ctx.IDENTIFIER().getText():
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(ctx.CLASS().getText())
            self.token_stream_rewriter.replaceRange(
                from_idx=0,
                to_idx=0,
                text="abstract "+ctx.CLASS().getText()
            )

    # def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
    #
    #     print(ctx.IDENTIFIER().getText())
    #     if self.objective_class == ctx.IDENTIFIER().getText():
    #         print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    #         ctxtypedeclaration = ctx.parentCtx
    #         print(ctx.classOrInterfaceModifier(0).getText())
    #         self.token_stream_rewriter.replaceRange(
    #             from_idx=ctxtypedeclaration.classOrInterfaceModifier(0).start.tokenIndex,
    #             to_idx=ctxtypedeclaration.classOrInterfaceModifier(0).stop.tokenIndex,
    #             text=ctxtypedeclaration.classOrInterfaceModifier(0).getText() + " abstract"
    #         )
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


class PropagationMakeAbstractClassRefactoringListener(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, Source_class= None, object_name=None,
                 propagated_class_name=None):

        if Source_class is None:
            self.source_class = []
        else:
            self.source_class = Source_class

        if object_name is None:
            self.object_name = []
        else:
            self.object_name = object_name

        if propagated_class_name is None:
            self.propagated_class_name = []
        else:
            self.propagated_class_name = propagated_class_name

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_class = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        print("Propagation started, please wait...")
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier in self.propagated_class_name:
            self.is_class = True
        else:
            self.is_class = False
    def enterClassBody(self, ctx:JavaParserLabeled.ClassBodyContext):
        if not self.is_class:
            return None
        self.token_stream_rewriter.insertBefore(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                index=ctx.start.tokenIndex,
                                                text=' extends '+ self.source_class
                                                )
    def enterVariableDeclarator(self, ctx:JavaParserLabeled.VariableDeclaratorContext):
        if not self.is_class:
            return None
        ctx_grandparent=ctx.parentCtx.parentCtx
        if ctx.variableDeclaratorId().IDENTIFIER().getText() in self.object_name:
            self.objectName=ctx.variableDeclaratorId().IDENTIFIER().getText()
            if ctx_grandparent.typeType().classOrInterfaceType().IDENTIFIER(0).getText() in self.source_class:
                self.token_stream_rewriter.delete(from_idx=ctx_grandparent.start.tokenIndex,
                                                  to_idx=ctx_grandparent.stop.tokenIndex,
                                                  program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME
                                                  )
    def enterExpression(self, ctx:JavaParserLabeled.ExpressionContext):
        if not self.is_class:
            return None
        if ctx.expression(0)!=None:
            if ctx.expression(0).primary() != None:
                if ctx.expression(0).primary().IDENTIFIER().getText() in self.object_name:
                    count=ctx.getChildCount()
                    if count==3:
                        self.token_stream_rewriter.replaceRange(
                            from_idx=ctx.start.tokenIndex,
                            to_idx=ctx.stop.tokenIndex,
                            text=ctx.children[count-1].getText()
                        )


class PropagationMakeAbstractClassGetObjectsRefactoringListener(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class=None,
                 propagated_class_name=None):

        if source_class is None:
            self.source_class = []
        else:
            self.source_class = source_class

        if propagated_class_name is None:
            self.propagated_class_name = []
        else:
            self.propagated_class_name = propagated_class_name

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_class = False
        self.current_class=''
        self.objects=list()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        # print("Propagation started, please wait...")
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier in self.propagated_class_name:
            self.is_class = True
            print("Propagation started, please wait...")
            self.current_class=class_identifier
        else:
            self.is_class = False

    def enterVariableDeclarator(self, ctx:JavaParserLabeled.VariableDeclaratorContext):
        if not self.is_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        if grand_parent_ctx.typeType().classOrInterfaceType() != None:
            className=grand_parent_ctx.typeType().classOrInterfaceType().IDENTIFIER(0).getText()
            if className in self.source_class:
                objectname=ctx.variableDeclaratorId().IDENTIFIER().getText()
                self.objects.append(objectname)


if __name__ == '__main__':
    udb_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    source_class = "Circle"
    # initialize with understand
    main_file = ""
    db = und.open(udb_path)
    print("Here")
    for cls in db.ents("class"):
        if cls.simplename() == source_class:
            main_file = cls.parent().longname()

    stream = FileStream(main_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = MakeAbstractClassRefactoringListener(common_token_stream=token_stream,
                                                       class_name=source_class)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(main_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())

