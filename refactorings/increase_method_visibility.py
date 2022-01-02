import logging

from refactorings.utils.utils2 import parse_and_walk

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

logger = logging.getLogger()


class IncreaseMethodVisibilityListener(JavaParserLabeledListener):
    def __init__(self, source_class, source_method, rewriter: TokenStreamRewriter):
        self.source_class = source_class
        self.source_method = source_method
        self.in_class = False
        self.detected_method = False
        self.rewriter = rewriter

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.source_class:
            self.in_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.source_class:
            self.in_class = False

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.source_method:
            self.detected_method = True

    def exitClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        if self.detected_method:
            self.rewriter.replaceSingleToken(
                token=ctx.modifier(0).start,
                text="public"
            )
            self.detected_method = False


def main(udb_path, source_package, source_class, source_method):
    db = und.open(udb_path)
    method_ent = db.lookup(f"{source_package}.{source_class}.{source_method}", "Method")

    if len(method_ent) == 0:
        logger.error("Invalid inputs.")
        return
    method_ent = method_ent[0]

    if method_ent.simplename() != source_method:
        logger.error("Invalid entity.")
        return

    if not method_ent.kind().check("Private"):
        logger.error("Method is not private.")
        return

    parent = method_ent.parent()
    while parent.parent() is not None:
        parent = parent.parent()

    main_file = parent.longname()
    parse_and_walk(
        file_path=main_file,
        listener_class=IncreaseMethodVisibilityListener,
        has_write=True,
        source_class=source_class,
        source_method=source_method
    )
    db.close()


if __name__ == '__main__':
    main(
        udb_path="D:\Dev\JavaSample\JavaSample\JavaSample.und",
        source_package="source_package",
        source_class="Sample",
        source_method="testMethod"
    )
