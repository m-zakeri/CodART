"""

## Introduction

The module implements a light-weight version of push-down field refactoring described in `pushdown_field.py`.


### Pre-conditions:

Todo: Add pre-conditions

### Post-conditions:

Todo: Add post-conditions

"""

__version__ = '0.1.1'
__author__ = "Seyyed Ali Ayati"

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

from codart.symbol_table import parse_and_walk
import sbse.config
from sbse.config import logger


class CutFieldListener(JavaParserLabeledListener):
    """

    Removes the field declaration from the parent class.

    """

    def __init__(self, source_class:str, field_name:str, rewriter: TokenStreamRewriter):
        """

        Args:

            source_class: (str) Parent's class name.

            field_name: (str) Field's name.

            rewriter (TokenStreamRewriter): ANTLR's token stream rewriter.

        Returns:

            field_content (CutFieldListener): The full string of field declaration

        """
        self.source_class = source_class
        self.field_name = field_name
        self.rewriter = rewriter
        self.field_content = ""
        self.import_statements = ""

        self.detected_field = False
        self.is_source_class = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_name = ctx.IDENTIFIER().getText()
        if class_name == self.source_class:
            self.is_source_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_name = ctx.IDENTIFIER().getText()
        if self.is_source_class and class_name == self.source_class:
            self.is_source_class = False

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        statement = self.rewriter.getText(
            program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
            start=ctx.start.tokenIndex,
            stop=ctx.stop.tokenIndex
        )
        self.import_statements += statement + "\n"

    def exitVariableDeclaratorId(self, ctx: JavaParserLabeled.VariableDeclaratorIdContext):
        variable_name = ctx.IDENTIFIER().getText()
        if self.is_source_class:
            if variable_name == self.field_name:
                self.detected_field = True

    def exitClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        if self.detected_field and self.is_source_class:
            self.field_content = self.rewriter.getText(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.start.tokenIndex,
                stop=ctx.stop.tokenIndex
            )
            self.rewriter.delete(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex
            )
            self.detected_field = False


class PasteFieldListener(JavaParserLabeledListener):
    """

    Inserts field declaration to children classes.

    """

    def __init__(self, source_class, field_content, import_statements, rewriter: TokenStreamRewriter):
        """

        Args:

            source_class: Child class name.

            field_content: Full string of the field declaration.

            rewriter: Antlr's token stream rewriter.

        Returns:

            object (PasteFieldListener): An instance of PasteFieldListener class

        """
        self.source_class = source_class
        self.rewriter = rewriter
        self.field_content = field_content
        self.import_statements = import_statements
        self.is_source_class = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_name = ctx.IDENTIFIER().getText()
        if class_name == self.source_class:
            self.is_source_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_name = ctx.IDENTIFIER().getText()
        if self.is_source_class and class_name == self.source_class:
            self.is_source_class = False

    def exitPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.rewriter.insertAfter(
            program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
            index=ctx.stop.tokenIndex,
            text="\n" + self.import_statements
        )

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        if self.is_source_class:
            self.rewriter.insertAfter(
                index=ctx.start.tokenIndex,
                text="\n\t" + self.field_content
            )


def main(udb_path=None, source_package=None, source_class=None, field_name=None, target_classes: list = None, *args,
         **kwargs):
    """

    The main API for push-down field refactoring

    """

    if udb_path is None:
        db = und.open(sbse.config.UDB_PATH)
    else:
        db = und.open(udb_path)

    source_class_ent = None
    source_class_ents = db.lookup(f"{source_package}.{source_class}", "Class")
    if len(source_class_ents) == 0:
        logger.error(f"Cannot find source class: {source_class}")
        db.close()
        return False
    else:
        for ent in source_class_ents:
            if ent.simplename() == source_class:
                source_class_ent = ent
                break

    if source_class_ent is None:
        logger.error(f"Cannot find source class: {source_class}")
        db.close()
        return False

    fields = db.lookup(f"{source_package}.{source_class}.{field_name}", "Variable")
    if fields is None or len(fields) == 0:
        logger.error(f"Cannot find field to pushdown: {field_name}")
        db.close()
        return False
    else:
        field_ent = fields[0]

    target_class_ents_files = []
    target_class_ents_simplenames = []
    for ref in source_class_ent.refs("Extendby"):
        if ref.ent().simplename() not in target_classes:
            logger.error("Target classes are not children classes")
            db.close()
            return False
        target_class_ents_files.append(ref.ent().parent().longname())
        target_class_ents_simplenames.append(ref.ent().simplename())

    for ref in field_ent.refs("Useby, Setby"):
        if ref.file().simplename().split(".")[0] in target_classes:
            continue
        else:
            logger.error("Field has dependencies.")
            db.close()
            return False

    source_class_file = source_class_ent.parent().longname()
    db.close()

    # Remove field from source class
    listener = parse_and_walk(
        file_path=source_class_file,
        listener_class=CutFieldListener,
        has_write=True,
        source_class=source_class,
        field_name=field_name,
        debug=False
    )

    # Insert field in children classes
    for i, target_class_file in enumerate(target_class_ents_files):
        parse_and_walk(
            file_path=target_class_file,
            listener_class=PasteFieldListener,
            has_write=True,
            source_class=target_class_ents_simplenames[i],
            field_content=listener.field_content,
            import_statements=listener.import_statements,
            debug=False
        )
    # db.close()
    return True


# Tests
if __name__ == '__main__':
    main(
        udb_path="D:\Dev\JavaSample\JavaSample\JavaSample.und",
        source_class="Person",
        source_package="target_package",
        field_name="testField",
        target_classes=["PersonChild"]
    )
