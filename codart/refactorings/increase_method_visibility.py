"""

## Introduction

Increase method visibility refactoring

Increase the visibility of a method from private to package, package to protected or protected to public.

## Pre and post-conditions

### Pre-conditions:

User must enter the method's name, and the source class's name for the refactoring in order to increase
the target method's visibility.

### Post-conditions:

No specific post-condition


"""

__version__ = '0.2.0'
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


class IncreaseMethodVisibilityListener(JavaParserLabeledListener):
    """

    To implement ِIncrease Method Visibility refactoring based on its actors.

    Detects the required method and increases/changes its visibility status.

    """

    def __init__(self, source_class, source_method, rewriter: TokenStreamRewriter):
        """

        Args:

            source_class (str): Name of the class in which the refactoring has to be done

            source_method (str): Name of the field whose visibility status has to be changed

            rewriter (CommonTokenStream): An instance of TokenStreamRewriter


        Returns:

            object (IncreaseMethodVisibilityListener): An instance of IncreaseMethodVisibilityListener

        """

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
            self.detected_method = False


def main(udb_path, source_package, source_class, source_method, *args, **kwargs):
    """


    """

    db = und.open(udb_path)
    methods = db.lookup(f"{source_package}.{source_class}.{source_method}", "Method")

    if methods is None or len(methods) == 0:
        logger.error("Invalid inputs.")
        db.close()
        return False

    method_entity = methods[0]
    if method_entity.simplename() != source_method:
        logger.error("Invalid entity.")
        db.close()
        return False

    # Strong overlay precondition
    # if not method_entity.kind().check("Private"):
    #     logger.error("Method is not private.")
    #     db.close()
    #     return False

    parent = method_entity.parent()
    while parent.parent() is not None:
        parent = parent.parent()

    main_file = parent.longname()  # The file that contain the method
    db.close()

    parse_and_walk(
        file_path=main_file,
        listener_class=IncreaseMethodVisibilityListener,
        has_write=True,
        source_class=source_class,
        source_method=source_method
    )
    # db.close()
    return True


# Tests
if __name__ == '__main__':
    main(
        udb_path="D:\Dev\JavaSample\JavaSample\JavaSample.und",
        source_package="source_package",
        source_class="Sample",
        source_method="testMethod"
    )
