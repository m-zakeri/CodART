import logging

from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from refactorings.move_field import CheckCycleListener
from refactorings.utils.utils2 import parse_and_walk

try:
    import understand as und
except ImportError as e:
    print(e)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__file__)
STATIC = "Static Method"

__author__ = "Seyyed Ali Ayati"
logger.info("You can find developer at: https://www.linkedin.com/in/seyyedaliayati/")


class CutMethodListener(JavaParserLabeledListener):
    def __init__(self, class_name: str, instance_name: str, method_name: str, is_static: bool, import_statement: str, rewriter: TokenStreamRewriter):
        self.class_name = class_name
        self.method_name = method_name
        self.is_static = is_static
        self.rewriter = rewriter
        self.import_statement = import_statement

        self.instance_name = instance_name
        self.is_member = False
        self.do_delete = False
        self.method_text = ""

    def exitPackageDeclaration(self, ctx:JavaParserLabeled.PackageDeclarationContext):
        if self.import_statement:
            self.rewriter.insertAfterToken(
                token=ctx.stop,
                text=self.import_statement,
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME
            )
            self.import_statement = None

    def enterMemberDeclaration0(self, ctx: JavaParserLabeled.MemberDeclaration0Context):
        self.is_member = True

    def exitMemberDeclaration0(self, ctx: JavaParserLabeled.MemberDeclaration0Context):
        self.is_member = False

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_member and ctx.IDENTIFIER().getText() == self.method_name:
            self.do_delete = True

    def exitClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        if self.do_delete:
            self.method_text = self.rewriter.getText(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.start.tokenIndex,
                stop=ctx.stop.tokenIndex
            )
            if self.is_static:
                replace_text = f"public static {self.class_name} {self.instance_name} = new {self.class_name}();"
            else:
                replace_text = f"public {self.class_name} {self.instance_name} = new {self.class_name}();"
            self.rewriter.replace(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex,
                text=replace_text
            )

            self.do_delete = False


class PasteMethodListener(JavaParserLabeledListener):
    def __init__(self, method_text: str, rewriter: TokenStreamRewriter):
        self.method_text = method_text
        self.rewriter = rewriter

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        self.rewriter.insertAfterToken(
            token=ctx.start,
            text="\n" + self.method_text + "\n",
            program_name=self.rewriter.DEFAULT_PROGRAM_NAME
        )


class PropagateListener(JavaParserLabeledListener):
    def __init__(self, method_name: str, new_name: str, lines: list, rewriter: TokenStreamRewriter):
        self.method_name = method_name
        self.new_name = new_name
        self.lines = lines
        self.rewriter = rewriter

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        identifier = ctx.IDENTIFIER()
        if identifier and ctx.start.line in self.lines and identifier.getText() == self.method_name:
            self.rewriter.replaceSingleToken(
                token=ctx.start,
                text=self.new_name
            )


def main(source_class: str, source_package: str, target_class: str, target_package: str, method_name: str,
         udb_path: str):
    import_statement = None
    if source_package != target_package:
        import_statement = f"\nimport {target_package}.{target_class};"
    instance_name = target_class.lower() + "ByCodArt"
    db = und.open(udb_path)

    # Check if method is static
    method_ent = db.lookup(f"{source_package}.{source_class}.{method_name}")
    if len(method_ent) != 1:
        logger.error("Can not move method duo to duplicated entities.")
        return None

    method_ent = method_ent[0]
    is_static = STATIC in method_ent.kindname()
    # Find usages
    usages = {}

    for ref in method_ent.refs("callby"):
        file = ref.file().longname()
        if file in usages:
            usages[file].append(ref.line())
        else:
            usages[file] = [ref.line(), ]

    src_class_file = db.lookup(f"{source_package}.{source_class}.java")[0].longname()
    target_class_file = db.lookup(f"{target_package}.{target_class}.java")[0].longname()

    # Check if there is an cycle
    listener = parse_and_walk(
        file_path=target_class_file,
        listener_class=CheckCycleListener,
        class_name=source_class
    )

    if not listener.is_valid:
        logger.error(f"Can not move method because there is a cycle between {source_class}, {target_class}")
        return None
    # Propagate Changes
    for file in usages.keys():
        parse_and_walk(
            file_path=file,
            listener_class=PropagateListener,
            has_write=True,
            method_name=method_name,
            new_name=f"{instance_name}.{method_name}",
            lines=usages[file],
        )
    # Do the cut and paste!
    # Cut
    listener = parse_and_walk(
        file_path=src_class_file,
        listener_class=CutMethodListener,
        has_write=True,
        class_name=target_class,
        instance_name=instance_name,
        method_name=method_name,
        is_static=is_static,
        import_statement=import_statement
    )

    method_text = listener.method_text

    # Paste
    parse_and_walk(
        file_path=target_class_file,
        listener_class=PasteMethodListener,
        has_write=True,
        method_text=method_text
    )
    db.close()


if __name__ == '__main__':
    main(
        source_class="Source",
        source_package="my_package",
        target_class="TargetNew",
        target_package="your_package",
        method_name="printTest",
        udb_path="D:\Dev\JavaSample\JavaSample1.udb"
    )
