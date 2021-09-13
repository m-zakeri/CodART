import logging

from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from utils.utils2 import parse_and_walk

try:
    import understand as und
except ImportError as e:
    print(e)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__file__)
STATIC = "Public Static Variable"
__author__ = "Seyyed Ali Ayati"
logger.info("You can find me at: https://www.linkedin.com/in/seyyedaliayati/")


class CutFieldListener(JavaParserLabeledListener):
    def __init__(self, class_name: str, field_name: str, is_static: bool, rewriter: TokenStreamRewriter):
        self.class_name = class_name
        self.field_name = field_name
        self.is_static = is_static
        self.rewriter = rewriter
        self.instance_name = class_name.lower() + "ByCodArt"
        self.is_member = False
        self.do_delete = False
        self.field_text = ""

    def enterMemberDeclaration2(self, ctx: JavaParserLabeled.MemberDeclaration2Context):
        self.is_member = True

    def exitMemberDeclaration2(self, ctx: JavaParserLabeled.MemberDeclaration2Context):
        self.is_member = False

    def enterVariableDeclaratorId(self, ctx: JavaParserLabeled.VariableDeclaratorIdContext):
        if self.is_member and ctx.IDENTIFIER().getText() == self.field_name:
            self.do_delete = True

    def exitClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        if self.do_delete:
            self.field_text = self.rewriter.getText(
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


class PasteFieldListener(JavaParserLabeledListener):
    def __init__(self, field_text: str, rewriter: TokenStreamRewriter):
        self.field_text = field_text
        self.rewriter = rewriter

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        self.rewriter.insertAfterToken(
            token=ctx.start,
            text="\n" + self.field_text + "\n",
            program_name=self.rewriter.DEFAULT_PROGRAM_NAME
        )


class PropagateListener(JavaParserLabeledListener):
    def __init__(self, field_name: str, new_name: str, lines: list, rewriter: TokenStreamRewriter):
        self.field_name = field_name
        self.new_name = new_name
        self.lines = lines
        self.rewriter = rewriter

    def enterExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        identifier = ctx.IDENTIFIER()
        if identifier and ctx.start.line in self.lines and identifier.getText() == self.field_name:
            self.rewriter.replaceSingleToken(
                token=ctx.stop,
                text=self.new_name
            )

    def enterExpression0(self, ctx: JavaParserLabeled.Expression0Context):
        identifier = ctx.getText()
        if identifier and ctx.start.line in self.lines and identifier == self.field_name:
            self.rewriter.replaceSingleToken(
                token=ctx.stop,
                text=self.new_name
            )


class CheckCycleListener(JavaParserLabeledListener):
    def __init__(self, class_name: str):
        self.class_name = class_name
        self.is_valid = True
        self.in_constructor = False

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        self.in_constructor = True

    def exitConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        self.in_constructor = False

    def enterCreatedName0(self, ctx: JavaParserLabeled.CreatedName0Context):
        if ctx.IDENTIFIER() and self.in_constructor and self.is_valid:
            identifiers = [i.getText() for i in ctx.IDENTIFIER()]
            if self.class_name in identifiers:
                self.is_valid = False


def main(source_class: str, source_package: str, target_class: str, target_package: str, field_name: str,
         udb_path: str):
    db = und.open(udb_path)

    # Check if field is static
    field_ent = db.lookup(f"{source_package}.{source_class}.{field_name}")
    assert len(field_ent) == 1
    field_ent = field_ent[0]
    is_static = field_ent.kindname() == STATIC

    if is_static:
        logger.warning("Field is static!")

    # Find usages
    usages = {}

    for ref in field_ent.refs("setby,useby"):
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
        class_name=source_class,
    )

    if not listener.is_valid:
        logger.error(f"Can not move field because there is a cycle between {source_class}, {target_class}")
        return

    # Do the cut and paste!
    # Cut

    listener = parse_and_walk(
        file_path=src_class_file,
        listener_class=CutFieldListener,
        has_write=True,
        class_name=target_class,
        field_name=field_name,
        is_static=is_static
    )

    instance_name = listener.instance_name
    field_text = listener.field_text

    # Paste
    parse_and_walk(
        file_path=target_class_file,
        listener_class=PasteFieldListener,
        has_write=True,
        field_text=field_text,
    )

    # Propagate Changes
    print(usages)
    for file in usages.keys():
        parse_and_walk(
            file_path=file,
            listener_class=PropagateListener,
            has_write=True,
            field_name=field_name,
            new_name=f"{instance_name}.{field_name}",
            lines=usages[file],
        )


if __name__ == '__main__':
    main(
        source_class="Source",
        source_package="my_package",
        target_class="Target",
        target_package="my_package",
        field_name="number2",
        udb_path="D:\Dev\JavaSample\JavaSample1.udb"
    )
