from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class UseAndUseByListener(JavaParserLabeledListener):
    def __init__(self, file_name):
        self.file_name = file_name
        self.package_name = ""
        self.useBy = []
        self.class_members = []
        self.method_count = 0
        self.constructor_name = ""

    # find members
    def enterMemberDeclaration2(self, ctx: JavaParserLabeled.MemberDeclaration2Context):
        self.class_members.append(
            ctx.getChild(0).getChild(1).getChild(0).getChild(0).getChild(0).getText()
        )

    # find constructors
    def enterConstructorDeclaration(
        self, ctx: JavaParserLabeled.ConstructorDeclarationContext
    ):
        self.constructor_name = ctx.getText().split("(")[0]

    @property
    def get_use(self):
        d = {}
        d["useBy"] = self.useBy
        return d

    # find methods
    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.method_count += 1

    # find packages
    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_name = ctx.getText().replace("package", "").replace(";", "")

    # find variables(use or useby)
    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        # ==========used/usedby=============
        is_None = False
        VI = ctx

        while (
            type(ctx) != JavaParserLabeled.ClassDeclarationContext
            and type(ctx) != JavaParserLabeled.MethodDeclarationContext
        ):
            if ctx.parentCtx:
                ctx = ctx.parentCtx
            else:
                is_None = True
                break

        if not is_None:
            for classmember in self.class_members:
                if classmember == VI.getText():
                    line1 = VI.IDENTIFIER().symbol.line
                    column1 = VI.IDENTIFIER().symbol.column
                    line2 = ctx.IDENTIFIER().symbol.line
                    column2 = ctx.IDENTIFIER().symbol.column
                    self.useBy.append(
                        (
                            VI.getText(),
                            ctx.IDENTIFIER().getText(),
                            line1,
                            column1,
                            line2,
                            column2,
                            self.package_name,
                        )
                    )


def get_percent_lack_of_cohesion(ent_model=None) -> int:
    # stream files
    stream = InputStream(ent_model.contents())
    # lex and tokenize
    lexer = JavaLexer(stream)
    token_string = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_string)
    pars_tree = parser.compilationUnit()
    my_listener = UseAndUseByListener(file)
    walker = ParseTreeWalker()
    walker.walk(t=pars_tree, listener=my_listener)

    # this table stores items
    table = dict()

    # store items in the table
    for member in my_listener.class_members:
        table[member] = []
    for item in my_listener.useBy:
        if item[1] != my_listener.constructor_name:
            if item[1] not in table[item[0]]:
                table[item[0]].append(item[1])
    all_use = []
    if my_listener.method_count == 0:
        return 100
    for t in table:
        all_use.append(len(table[t]) / my_listener.method_count)
    try:
        avg = sum(all_use) / len(all_use)
    except:
        avg = 0
    return (1 - avg) * 100
