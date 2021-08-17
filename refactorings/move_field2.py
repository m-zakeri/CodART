from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

try:
    import understand as und
except ImportError as e:
    print(e)


class CutFieldListener(JavaParserLabeledListener):
    def __init__(self, field_name: str, rewriter: TokenStreamRewriter):
        self.field_name = field_name
        self.rewriter = rewriter
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
            self.rewriter.delete(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start,
                to_idx=ctx.stop
            )
            self.do_delete = False


class PasteFieldListener(JavaParserLabeledListener):
    def __init__(self, field_text: str, rewriter: TokenStreamRewriter):
        self.field_text = field_text
        self.rewriter = rewriter

    def enterClassBody(self, ctx:JavaParserLabeled.ClassBodyContext):
        self.rewriter.insertAfterToken(
            token=ctx.start,
            text="\n" + self.field_text + "\n",
            program_name=self.rewriter.DEFAULT_PROGRAM_NAME
        )


def main():
    STATIC = "Public Static Variable"
    src_class = "Source"
    src_package = "my_package"
    target_class = "Target"
    target_package = "my_package"
    field_name = "number3"
    udb_path = "/data/Dev/JavaSample/JavaSample.udb"
    db = und.open(udb_path)

    # Check if field is static
    field_ent = db.lookup(f"{src_package}.{src_class}.{field_name}")
    assert len(field_ent) == 1
    field_ent = field_ent[0]
    is_static = field_ent.kindname() == STATIC

    if is_static:
        print("Field is static")
    else:
        print("Finding usages...")
        # Find usages
        usages = []

        for ref in field_ent.refs("setby,useby"):
            usages.append({
                "ent": ref.ent(),
                "file": ref.file().longname(),
                "line": ref.line(),
                "column": ref.column(),
                "kind": ref.kindname()
            })

        # Do the cut and paste!

        src_class_file = db.lookup(f"{src_package}/{src_class}.java")[0].longname()
        target_class_file = db.lookup(f"{src_package}.{target_class}")[0].longname()

        # Cut
        print(src_class_file)
        stream = FileStream(src_class_file)
        lexer = JavaLexer(stream)
        tokens = CommonTokenStream(lexer)
        rewriter = TokenStreamRewriter(tokens)
        parser = JavaParserLabeled(tokens)
        tree = parser.compilationUnit()
        listener = CutFieldListener(
            field_name=field_name,
            rewriter=rewriter
        )
        ParseTreeWalker().walk(
            listener,
            tree
        )

        field_text = listener.field_text
        assert len(field_text) > 1
        # with open(src_class_file, 'w') as f:
        #     f.write(listener.rewriter.getDefaultText())
        print("=" * 30)
        print(listener.rewriter.getDefaultText())
        print("=" * 30)

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

        print(listener.rewriter.getDefaultText())
        print("=" * 30)


if __name__ == '__main__':
    main()
