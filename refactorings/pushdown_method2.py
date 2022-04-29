"""

## Introduction

The module implements a light-weight version of the push-down method refactoring described in `pushdown_method.py`


### Pre-conditions:

Todo: Add pre-conditions

### Post-conditions:

Todo: Add post-conditions

"""

__version__ = '0.1.1'
__author__ = 'Seyyed Ali Ayati'

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

from codart.symbol_table import parse_and_walk
from sbse import config


class CutMethodListener(JavaParserLabeledListener):
    """

    Removes the method declaration from the parent class.

    """
    def __init__(self, source_class, method_name, rewriter: TokenStreamRewriter):
        """

        Args:

            source_class: (str) Parent's class name.

            method_name: (str) Method's name.

            rewriter (TokenStreamRewriter): ANTLR's token stream rewriter.

        Returns:

            field_content (CutMethodListener): The full string of method declaration

        """

        self.source_class = source_class
        self.method_name = method_name
        self.rewriter = rewriter
        self.method_content = ""
        self.import_statements = ""

        self.detected_method = False
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

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_source_class and ctx.IDENTIFIER().getText() == self.method_name:
            self.detected_method = True

    def exitClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        if self.detected_method:
            self.method_content = self.rewriter.getText(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.start.tokenIndex,
                stop=ctx.stop.tokenIndex
            )
            self.rewriter.delete(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex
            )
            self.detected_method = False


class PasteMethodListener(JavaParserLabeledListener):
    """

    Inserts method declaration to children classes.

    """
    def __init__(self, source_class, method_content, import_statements, rewriter: TokenStreamRewriter):
        """

        Args:

            source_class (str): Child class name.

            method_content (str): Full string of the method declaration.

            rewriter (TokenStreamRewriter): ANTLR's token stream rewriter.

        Returns:

            object (PasteMethodListener): An instance of PasteMethodListener class.

        """

        self.source_class = source_class
        self.rewriter = rewriter
        self.method_content = method_content
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
            self.rewriter.insertBefore(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                index=ctx.stop.tokenIndex,
                text="\n\t" + self.method_content + "\n"
            )


def main(udb_path, source_package, source_class, method_name, target_classes: list, *args, **kwargs):
    """

    The main API for the push-down method refactoring (version 2)

    """

    db = und.open(udb_path)
    source_class_ents = db.lookup(f"{source_package}.{source_class}", "Class")
    target_class_ents = []
    source_class_ent = None

    if len(source_class_ents) == 0:
        config.logger.error(f"Cannot find source class: {source_class}")
        db.close()
        return False
    else:
        for ent in source_class_ents:
            if ent.simplename() == source_class:
                source_class_ent = ent
                break
    if source_class_ent is None:
        config.logger.error(f"Cannot find source class: {source_class}")
        db.close()
        return False

    method_ent = db.lookup(f"{source_package}.{source_class}.{method_name}", "Method")
    if len(method_ent) == 0:
        config.logger.error(f"Cannot find method to pushdown: {method_name}")
        db.close()
        return False
    else:
        method_ent = method_ent[0]

    for ref in source_class_ent.refs("extendBy"):
        if ref.ent().simplename() not in target_classes:
            config.logger.error("Target classes are not children classes")
            db.close()
            return False
        target_class_ents.append(ref.ent())

    for ref in method_ent.refs("callBy"):
        if ref.file().simplename().split(".")[0] in target_classes:
            continue
        else:
            config.logger.error("Method has dependencies.")
            db.close()
            return False

    # Remove field from source class
    listener = parse_and_walk(
        file_path=source_class_ent.parent().longname(),
        listener_class=CutMethodListener,
        has_write=True,
        source_class=source_class,
        method_name=method_name,
        debug=False
    )

    # Insert field in children classes
    for target_class in target_class_ents:
        parse_and_walk(
            file_path=target_class.parent().longname(),
            listener_class=PasteMethodListener,
            has_write=True,
            source_class=target_class.simplename(),
            method_content=listener.method_content,
            import_statements=listener.import_statements,
            debug=False
        )
    db.close()


# Tests
if __name__ == '__main__':
    main(
        udb_path="D:\Dev\JavaSample\JavaSample\JavaSample.und",
        source_class="Person",
        source_package="target_package",
        method_name="runTest",
        target_classes=["PersonChild"]
    )
