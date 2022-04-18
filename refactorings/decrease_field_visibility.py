"""
Decrease field visibility refactoring
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
from sbse.config import logger, UDB_PATH


class DecreaseFieldVisibilityListener(JavaParserLabeledListener):
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
            # print(ctx.getText())
            if ctx.modifier(0) is not None:
                if "@" in ctx.modifier(0).getText():
                    if ctx.modifier(1) is not None:
                        self.rewriter.replaceSingleToken(
                            token=ctx.modifier(1).start,
                            text="private "
                        )
                    else:
                        self.rewriter.replaceSingleToken(
                            ctx.memberDeclaration().getChild(0).getChild(0).start,
                            text="private " + ctx.memberDeclaration().getChild(0).getChild(0).getText()
                        )
                else:
                    if ctx.modifier(0).getText() == 'public' or ctx.modifier(0).getText() == 'protected':
                        self.rewriter.replaceSingleToken(
                            token=ctx.modifier(0).start,
                            text="private "
                        )
                    else:
                        self.rewriter.insertBeforeToken(
                            token=ctx.modifier(0).start,
                            text="private "
                        )
            else:
                if ctx.memberDeclaration().getChild(0).getChild(0) is not None:
                    self.rewriter.insertBeforeToken(
                        ctx.memberDeclaration().getChild(0).getChild(0).start,
                        text="private "
                    )

            # print("private " + ctx.memberDeclaration().getText())
            self.detected_field = False


def main(udb_path, source_package, source_class, source_field, *args, **kwargs):
    db = und.open(udb_path)
    field_ent = db.lookup(f"{source_package}.{source_class}.{source_field}", "Variable")

    if len(field_ent) == 0:
        logger.error("Invalid inputs.")
        db.close()
        return False

    field_ent = field_ent[0]
    if field_ent.simplename() != source_field:
        logger.error("Invalid entity.")
        db.close()
        return False

    # Strong overlay precondition
    # if not field_ent.kind().check("Public"):
    #     logger.error("Field is not public.")
    #     db.close()
    #     return False

    for ref in field_ent.refs("Useby,Setby"):
        ent = ref.ent()
        if f"{source_package}.{source_class}" not in ent.longname():
            logger.debug(f"{source_package}.{source_class} not in {ent.longname()}")
            logger.error("Field cannot set to private.")
            db.close()
            return False

    parent = field_ent.parent()
    while parent.parent() is not None:
        parent = parent.parent()

    main_file = parent.longname()
    db.close()

    parse_and_walk(
        file_path=main_file,
        listener_class=DecreaseFieldVisibilityListener,
        has_write=True,
        source_class=source_class,
        source_field=source_field
    )

    return True


# Tests
def test1():
    main(
        udb_path="D:/IdeaProjects/JSON20201115/JSON20201115.und",
        source_package="org.json",
        source_class="JSONObject",
        source_field="Object"
    )


def test2():
    main(
        udb_path=UDB_PATH,
        source_package='technology.tabula',
        source_class='TableWithRulingLines',
        source_field='si'
    )


if __name__ == '__main__':
    # test1()
    test2()
