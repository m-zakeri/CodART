"""
Seyyed Ali Ayati
"""

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

from . import move_static_field

try:
    import understand as und
except ImportError as e:
    print(e)


class CutFieldListener(JavaParserLabeledListener):
    def __init__(self, class_name: str, field_name: str, rewriter: TokenStreamRewriter):
        self.class_name = class_name
        self.field_name = field_name
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
            self.rewriter.replace(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex,
                text=f"public {self.class_name} {self.instance_name} = new {self.class_name}();"
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


def main():
    STATIC = "Public Static Variable"
    src_class = "Source"
    src_package = "my_package"
    target_class = "Target"
    target_package = "my_package"
    field_name = "number3"
    project_dir = "/data/Dev/JavaSample/"
    udb_path = "/data/Dev/JavaSample/JavaSample.udb"
    db = und.open(udb_path)

    # Check if field is static
    field_ent = db.lookup(f"{src_package}.{src_class}.{field_name}")
    assert len(field_ent) == 1
    field_ent = field_ent[0]
    is_static = field_ent.kindname() == STATIC

    if is_static:
        print("Field is static")
        move_static_field.main(
            project_dir,
            src_package,
            src_class,
            field_name,
            target_class,
            target_package
        )
    else:
        print("Finding usages...")
        # Find usages
        usages = {}

        for ref in field_ent.refs("setby,useby"):
            file = ref.file().longname()
            if file in usages:
                usages[file].append(ref.line())
            else:
                usages[file] = [ref.line(), ]

        src_class_file = db.lookup(f"{src_package}/{src_class}.java")[0].longname()
        target_class_file = db.lookup(f"{src_package}/{target_class}.java")[0].longname()

        # Check if there is an cycle
        # TODO: Can we check cycle with understand ?
        stream = FileStream(target_class_file)
        lexer = JavaLexer(stream)
        tokens = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokens)
        tree = parser.compilationUnit()
        listener = CheckCycleListener(
            class_name=src_class,
        )
        ParseTreeWalker().walk(
            listener,
            tree
        )

        assert listener.is_valid, f"Can not move field because there is a cycle between {src_class}, {target_class}"

        # Do the cut and paste!
        # Cut
        stream = FileStream(src_class_file)
        lexer = JavaLexer(stream)
        tokens = CommonTokenStream(lexer)
        rewriter = TokenStreamRewriter(tokens)
        parser = JavaParserLabeled(tokens)
        tree = parser.compilationUnit()
        listener = CutFieldListener(
            class_name=target_class,
            field_name=field_name,
            rewriter=rewriter
        )
        ParseTreeWalker().walk(
            listener,
            tree
        )
        instance_name = listener.instance_name
        field_text = listener.field_text
        assert len(field_text) > 1
        with open(src_class_file, 'w') as f:
            f.write(listener.rewriter.getDefaultText())
        # print("=" * 30)
        # print(listener.rewriter.getDefaultText())
        # print("=" * 30)
        # Paste
        stream = FileStream(target_class_file)
        lexer = JavaLexer(stream)
        tokens = CommonTokenStream(lexer)
        rewriter = TokenStreamRewriter(tokens)
        parser = JavaParserLabeled(tokens)
        tree = parser.compilationUnit()
        listener = PasteFieldListener(
            field_text=field_text,
            rewriter=rewriter
        )
        ParseTreeWalker().walk(
            listener,
            tree
        )
        with open(target_class_file, 'w') as f:
            f.write(listener.rewriter.getDefaultText())
        # print(listener.rewriter.getDefaultText())
        # print("=" * 30)

        # Propagate Changes
        for file in usages.keys():
            stream = FileStream(file)
            lexer = JavaLexer(stream)
            tokens = CommonTokenStream(lexer)
            rewriter = TokenStreamRewriter(tokens)
            parser = JavaParserLabeled(tokens)
            tree = parser.compilationUnit()
            listener = PropagateListener(
                field_name=field_name,
                new_name=f"{instance_name}.{field_name}",
                lines=usages[file],
                rewriter=rewriter
            )
            ParseTreeWalker().walk(
                listener,
                tree
            )

            with open(file, 'w') as f:
                f.write(listener.rewriter.getDefaultText())

            # print(listener.rewriter.getDefaultText())
            # print("=" * 30)


if __name__ == '__main__':
    main()
