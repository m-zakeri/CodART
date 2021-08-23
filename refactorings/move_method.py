"""
Seyyed Ali Ayati
"""

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from refactorings.move_field import CheckCycleListener

try:
    import understand as und
except ImportError as e:
    print(e)


class CutMethodListener(JavaParserLabeledListener):
    def __init__(self, class_name: str, method_name: str, rewriter: TokenStreamRewriter):
        self.class_name = class_name
        self.method_name = method_name
        self.rewriter = rewriter
        self.instance_name = class_name.lower() + "ByCodArt"
        self.is_member = False
        self.do_delete = False
        self.method_text = ""

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
            self.rewriter.replace(
                program_name=self.rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex,
                text=f"public {self.class_name} {self.instance_name} = new {self.class_name}();"
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


def main():
    STATIC = "Static Method"
    src_class = "Source"
    src_package = "my_package"
    target_class = "Target"
    target_package = "my_package"
    method_name = "printTest"
    udb_path = "/data/Dev/JavaSample/JavaSample.udb"
    db = und.open(udb_path)

    # Check if method is static
    method_ent = db.lookup(f"{src_package}.{src_class}.{method_name}")
    assert len(method_ent) == 1
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

    assert listener.is_valid, f"Can not move method because there is a cycle between {src_class}, {target_class}"

    # Do the cut and paste!
    # Cut
    stream = FileStream(src_class_file)
    lexer = JavaLexer(stream)
    tokens = CommonTokenStream(lexer)
    rewriter = TokenStreamRewriter(tokens)
    parser = JavaParserLabeled(tokens)
    tree = parser.compilationUnit()
    listener = CutMethodListener(
        class_name=target_class,
        method_name=method_name,
        rewriter=rewriter
    )
    ParseTreeWalker().walk(
        listener,
        tree
    )
    instance_name = listener.instance_name
    method_text = listener.method_text
    assert len(method_text) > 1
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
    listener = PasteMethodListener(
        method_text=method_text,
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
            method_name=method_name,
            new_name=f"{instance_name}.{method_name}",
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
