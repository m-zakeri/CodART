"""

## Introduction

Increase field visibility refactoring

Increase the visibility of a field from private to package, package to protected or protected to public.

## Pre and post-conditions

### Pre-conditions:

User must enter the field's name, and the source class's name for the refactoring in order to increase
the target field's visibility.

### Post-conditions:

No specific post-condition


"""

__version__ = "0.2.0"
__author__ = "Morteza Zakeri"

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4.TokenStreamRewriter import TokenStreamRewriter

from codart.gen.JavaParserLabeled import JavaParserLabeled
from codart.gen.JavaParserLabeledListener import JavaParserLabeledListener
from codart.symbol_table import parse_and_walk
from codart.config import logger


class IncreaseFieldVisibilityListener(JavaParserLabeledListener):
    """

    To implement ِIncrease Field Visibility refactoring based on its actors.

    Detects the required field and increases/changes its visibility status.

    """
    def __init__(self, source_class, source_field, rewriter: TokenStreamRewriter):
        """
        Args:

            source_class (str): Name of the class in which the refactoring has to be done

            source_field (str): Name of the field whose visibility status has to be changed

            rewriter (CommonTokenStream): An instance of TokenStreamRewriter


        Returns:

            object (IncreaseFieldVisibilityListener): An instance of IncreaseFieldVisibilityListener

        """

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
                if "@" in ctx.modifier(0).getText():
                    if ctx.modifier(1) is not None:
                        self.rewriter.replaceSingleToken(
                            token=ctx.modifier(1).start,
                            text="public "
                        )
                    else:
                        self.rewriter.replaceSingleToken(
                            ctx.memberDeclaration().getChild(0).getChild(0).start,
                            text="public " + ctx.memberDeclaration().getChild(0).getChild(0).getText()
                        )
                else:
                    if ctx.modifier(0).getText() == 'private' or ctx.modifier(0).getText() == 'protected':
                        self.rewriter.replaceSingleToken(
                            token=ctx.modifier(0).start,
                            text="public "
                        )
                    else:
                        self.rewriter.insertBeforeToken(
                            token=ctx.modifier(0).start,
                            text="public "
                        )
            else:
                if ctx.memberDeclaration().getChild(0).getChild(0) is not None:
                    self.rewriter.insertBeforeToken(
                        ctx.memberDeclaration().getChild(0).getChild(0).start,
                        text="public "
                    )
            self.detected_field = False


def main(udb_path, source_package, source_class, source_field, *args, **kwargs):
    """


    """

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


# Tests
if __name__ == '__main__':
    main(
        udb_path="D:/Dev/JavaSample/JavaSample/JavaSample.und",
        source_package="source_package",
        source_class="Sample",
        source_field="privateField"
    )
