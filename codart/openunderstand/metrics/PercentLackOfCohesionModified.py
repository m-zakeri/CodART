from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


def toLower(l):
    result = []
    for i in l:
        result.append(i.lower())
    return result


class UseAndUseByListener(JavaParserLabeledListener):
    def __init__(self, file_name):
        self.file_name = file_name
        self.package_name = ""
        self.useBy = []
        self.class_members = []
        self.method_count = 0
        self.constructor_name = ""
        self.inGetterOrSetter = False

    # find members
    def enterMemberDeclaration2(self, ctx: JavaParserLabeled.MemberDeclaration2Context):
        self.class_members.append(
            ctx.getChild(0).getChild(1).getChild(0).getChild(0).getChild(0).getText()
        )

    # find consteructors
    def enterConstructorDeclaration(
        self, ctx: JavaParserLabeled.ConstructorDeclarationContext
    ):
        self.constructor_name = ctx.getText().split("(")[0]

    @property
    def get_use(self):
        d = {}
        d["useBy"] = self.useBy
        return d

    # find Methods
    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not (
            (
                str(ctx.IDENTIFIER()).startswith("get")
                or str(ctx.IDENTIFIER()).startswith("set")
            )
            and str(ctx.IDENTIFIER())[3:].lower() in toLower(self.class_members)
        ):
            # not in setter or getter
            self.method_count += 1
        else:
            # in setter or getter
            self.inGetterOrSetter = True

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.inGetterOrSetter = False

    # find Packages
    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_name = ctx.getText().replace("package", "").replace(";", "")

    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        if self.inGetterOrSetter:
            return 0
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


def get_percent_lack_of_cohesion_modified(ent_model=None):
    stream = InputStream(ent_model.contents())
    lexer = JavaLexer(stream)
    token_string = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_string)
    pars_tree = parser.compilationUnit()
    my_listener = UseAndUseByListener(file)
    walker = ParseTreeWalker()
    walker.walk(t=pars_tree, listener=my_listener)
    # this table stores items
    table = dict()
    for member in my_listener.class_members:
        table[member] = []
    for item in my_listener.useBy:
        if item[1] != my_listener.constructor_name:
            if item[1] not in table[item[0]]:
                table[item[0]].append(item[1])
    alluse = []
    if my_listener.method_count == 0:
        return 100
    for t in table:
        alluse.append(len(table[t]) / my_listener.method_count)
    try:
        avg = sum(alluse) / len(alluse)
    except:
        avg = 0
    return (1 - avg) * 100
