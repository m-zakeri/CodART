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
    def __init__(self, common_token_stream: CommonTokenStream, source_class: str, source_method_text: str):
        self.source_method_text = source_method_text
        self.source_class = source_class
        self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        self.is_safe = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.is_safe = ctx.IDENTIFIER().getText() == self.source_class

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.is_safe = not self.is_safe

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        if self.is_safe:
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


class PropagationListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream, source_class: str, child_class: str, class_name: str,
                 method_name: str, ref_line: int, target_package: str):
        self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        self.source_class = source_class
        self.child_class = child_class
        self.class_name = class_name
        self.method_name = method_name
        self.ref_line = ref_line
        self.target_package = target_package

        self.start = None
        self.stop = None
        self.is_safe = False
        self.need_cast = False
        self.variable = None
        self.detected_class = False
        self.detected_package = False
        self.import_end = None

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.is_safe = ctx.IDENTIFIER().getText() == self.class_name

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.is_safe = not self.is_safe

    def exitCreatedName0(self, ctx: JavaParserLabeled.CreatedName0Context):
        if ctx.IDENTIFIER(0).getText() == self.source_class and self.is_safe:
            self.detected_class = True
            self.start = ctx.start
            self.stop = ctx.stop

    def exitVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        if self.detected_class and self.is_safe:
            self.variable = ctx.variableDeclaratorId().IDENTIFIER().getText()
            self.detected_class = False

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        if ctx.IDENTIFIER().getText() == self.method_name and self.is_safe:
            # Change Name
            if ctx.start.line == self.ref_line:
                self.token_stream_rewriter.replaceRange(
                    from_idx=self.start.tokenIndex,
                    to_idx=self.stop.tokenIndex,
                    text=self.child_class
                )

    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        if ctx.start.line == self.ref_line and self.is_safe:
            self.need_cast = True

    def exitExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        if ctx.start.line == self.ref_line and self.is_safe:
            self.need_cast = False

    def enterExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        self.enterExpression21(ctx)

    def exitExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        if self.is_safe and self.need_cast and self.variable is not None:
            # Type casting
            child = ctx.getChild(0).getChild(0)
            self.token_stream_rewriter.replaceRange(
                from_idx=child.start.tokenIndex,
                to_idx=child.stop.tokenIndex,
                text=f"(({self.child_class}) {self.variable})"
            )
            self.need_cast = False

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        if self.target_package in ctx.getText():
            self.detected_package = True
        self.import_end = ctx.stop

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        if f"{self.target_package}.{self.child_class}" in ctx.getText():
            self.detected_package = True
        self.import_end = ctx.stop

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        if not self.detected_package and self.import_end is not None:
            self.token_stream_rewriter.insertAfterToken(
                token=self.import_end,
                text=f"\nimport {self.target_package}.{self.child_class};\n",
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME
            )


if __name__ == '__main__':
    udb_path = "/data/Dev/JavaSample/JavaSample.udb"
    source_package = "your_package"
    source_class = "Unit"
    source_method = "getFuel"
    source_method_entity = None
    target_package = "your_package"
    target_classes = ["Soldier", ]

    main_file = ""
    propagation_files = []
    propagation_classes = []
    propagation_lines = []
    children_classes = []
    children_files = []

    # initialize with understand
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
            for ref in mth.refs("Callby"):
                propagation_files.append(ref.ent().parent().parent().longname())
                propagation_classes.append(ref.ent().parent().simplename())
                propagation_lines.append(ref.line())

    print("propagation_files :", propagation_files)
    print("propagation_classes : ", propagation_classes)
    print("children_classes :", children_classes)
    print("children_files :", children_files)
    print("==============================================================================")
    # Check pre-condition
    assert len(target_classes) == 1
    assert len(children_classes) == 1
    assert len(children_files) == 1
    for mth in db.ents("Java Method"):
        if mth.simplename() == source_method:
            if mth.parent().simplename() in target_classes:
                if mth.type() == source_method_entity.type():
                    if mth.kind() == source_method_entity.kind():
                        if mth.parameters() == source_method_entity.parameters():
                            raise Exception("Duplicate method")
    #  get text
    method_text = source_method_entity.contents()
    # Delete source method
    stream = FileStream(main_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = DeleteSourceListener(common_token_stream=token_stream, source_method=source_method)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)
    # print(my_listener.token_stream_rewriter.getDefaultText())
    with open(main_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())

    # Do the push down
    for child_file, child_class in zip(children_files, children_classes):
        stream = FileStream(child_file, encoding='utf8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        my_listener = PushDownMethodRefactoringListener(common_token_stream=token_stream,
                                                        source_class=child_class,
                                                        source_method_text=method_text)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)
        # print(my_listener.token_stream_rewriter.getDefaultText())
        with open(child_file, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

    # Propagation
    for file, _class, line in zip(propagation_files, propagation_classes, propagation_lines):
        stream = FileStream(file, encoding='utf8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        my_listener = PropagationListener(common_token_stream=token_stream, source_class=source_class,
                                          child_class=children_classes[0], class_name=_class, method_name=source_method,
                                          ref_line=line, target_package=target_package)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)
        # print(my_listener.token_stream_rewriter.getDefaultText())
        with open(file, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())
