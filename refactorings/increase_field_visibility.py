"""
Increase field visibility refactoring

"""

__version__ = "0.2.0"
__author__ = "Morteza Zakeri"

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from codart.symbol_table import parse_and_walk
from sbse.config import logger


class IncreaseFieldVisibilityListener(JavaParserLabeledListener):
    def __init__(self, source_class, source_field, rewriter: TokenStreamRewriter):
        self.source_class = source_class
        self.source_field = source_field
        self.in_class = False
        self.in_field = False
        self.detected_field = False
        self.rewriter = rewriter

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.source_class:
            self.in_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.source_class:
            self.in_class = False

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        self.in_field = True

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        self.in_field = False

    def enterVariableDeclaratorId(self, ctx: JavaParserLabeled.VariableDeclaratorIdContext):
        if ctx.IDENTIFIER().getText() == self.source_field and self.in_field:
            self.detected_field = True

    def exitClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        if self.detected_field:
            if ctx.modifier(0) is not None:
                self.rewriter.replaceSingleToken(
                    token=ctx.modifier(0).start,
                    text="public"
                )
            else:
                self.rewriter.replaceSingleToken(
                    ctx.memberDeclaration().start,
                    text="public" + ctx.memberDeclaration().getText()
                )
            self.detected_field = False


def main(udb_path, source_package, source_class, source_field, *args, **kwargs):
    db = und.open(udb_path)
    fields = db.lookup(f"{source_package}.{source_class}.{source_field}", "Variable")

    if len(fields) == 0:
        logger.error("Invalid inputs.")
        db.close()
        return False

    field_ent = fields[0]
    if field_ent.simplename() != source_field:
        logger.error("Invalid entity.")
        db.close()
        return False

    # Strong overlay precondition
    # if not field_ent.kind().check("private"):
    #     logger.error("Field is not private.")
    #     db.close()
    #     return False

    parent = field_ent.parent()
    while parent.parent() is not None:
        parent = parent.parent()

    main_file = str(parent.longname())
    db.close()

    parse_and_walk(
        file_path=main_file,
        listener_class=IncreaseFieldVisibilityListener,
        has_write=True,
        source_class=source_class,
        source_field=source_field
    )
    # db.close()
    return True


if __name__ == '__main__':
    main(
        udb_path="D:\Dev\JavaSample\JavaSample\JavaSample.und",
        source_package="source_package",
        source_class="Sample",
        source_field="privateField"
    )
