from gen.javaLabeled.JavaLexer import JavaLexer

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class PushDownMethodRefactoringListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream, source_method_text: str):
        self.common_token_stream = common_token_stream
        self.source_method_text = source_method_text
        self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        self.token_stream_rewriter.insertBefore(
            index=ctx.stop.tokenIndex,
            text=self.source_method_text + "\n",
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME
        )


class DeleteSourceListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream, source_method: str):
        self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        self.source_method = source_method

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.source_method == ctx.IDENTIFIER().getText():
            self.token_stream_rewriter.replaceRange(
                from_idx=ctx.parentCtx.parentCtx.start.tokenIndex,
                to_idx=ctx.parentCtx.parentCtx.stop.tokenIndex,
                text=""
            )


if __name__ == '__main__':
    udb_path = "/data/Dev/JavaSample/JavaSample.udb"
    source_package = "your_package"
    source_class = "Unit"
    source_method = "getFuel"
    source_method_entity = None
    target_package = "your_package"
    target_classes = ["Tank", ]
    passed_preconditions = True
    # initialize with understand
    main_file = ""
    propagation_files = []
    propagation_classes = []
    children_classes = []
    children_files = []
    db = und.open(udb_path)
    for mth in db.ents("Java Method"):
        if mth.longname() == source_package + "." + source_class + "." + source_method:
            source_method_entity = mth
            for child_ref in mth.parent().refs("Extendby"):
                child_ref = child_ref.ent()
                if child_ref.simplename() in target_classes:
                    children_classes.append(child_ref.simplename())
                    children_files.append(child_ref.parent().longname())
            print("mainfile : ", mth.parent().parent().longname())
            main_file = mth.parent().parent().longname()
            print(mth)
            for ref in mth.refs("Callby"):
                propagation_files.append(ref.ent().parent().parent().longname())
                propagation_classes.append(ref.ent().parent().simplename())

    print("propagation_files :", propagation_files)
    print("propagation_classes : ", propagation_classes)
    print("children_classes :", children_classes)
    print("children_files :", children_files)
    print("==============================================================================")
    # Check pre-condition
    for mth in db.ents("Java Method"):
        if mth.simplename() == source_method:
            if mth.parent().simplename() in target_classes:
                if mth.type() == source_method_entity.type():
                    if mth.kind() == source_method_entity.kind():
                        if mth.parameters() == source_method_entity.parameters():
                            raise Exception("Duplicate method")
    #  get text
    method_text = source_method_entity.contents()
    # print(method_text)
    # end get text

    stream = FileStream(main_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = DeleteSourceListener(common_token_stream=token_stream, source_method=source_method)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)
    print(my_listener.token_stream_rewriter.getDefaultText())
    # with open(main_file, mode='w', newline='') as f:
    #     f.write(my_listener.token_stream_rewriter.getDefaultText())

    # begin refactoring...
    for child_file, child_class in zip(children_files, children_classes):
        stream = FileStream(child_file, encoding='utf8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        my_listener = PushDownMethodRefactoringListener(common_token_stream=token_stream,
                                                        source_method_text=method_text)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)
        print(my_listener.token_stream_rewriter.getDefaultText())
        # with open(child_file, mode='w', newline='') as f:
        #     f.write(my_listener.token_stream_rewriter.getDefaultText())
