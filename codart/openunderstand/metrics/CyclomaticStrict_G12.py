from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaLexer import JavaLexer
from openunderstand.ounderstand.project import Project
from antlr4 import *
from openunderstand.analysis_passes import class_properties


def countParents(ctx):
    scope_parents = class_properties.ClassPropertiesListener.findParents(ctx)
    if len(scope_parents) == 1:
        scope_longname = scope_parents[0]
    else:
        scope_longname = ".".join(scope_parents)
    return scope_longname


class CyclomaticStrictListener(JavaParserLabeledListener):
    def __init__(self):
        self.method_count_Cyclomatic = 1
        self.method_long_name = ""
        self.file = ""
        self.enter_method = False
        self.enter_block = False
        self.enter_class = False
        self.method_long_names = {}
        self.packagename = ""
        self.class_name = None
        self.max_value = 0
        self.classes = {}

    @property
    def get_packagename(self):
        return self.packagename

    @property
    def get_max_value(self):
        return self.method_count_Cyclomatic

    @property
    def get_methods(self):
        return self.method_long_names

    @property
    def get_classes(self):
        return self.classes

    # parent and long name by parent classes
    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.packagename = ctx.qualifiedName().getText()

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):

        self.enter_method = True

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):

        if (
            self.class_name == ctx.IDENTIFIER().getText()
            or self.class_name == ""
            or self.class_name is None
        ):
            self.enter_class = True
        self.classes = {}
        self.max_value = 0

    # if-statement
    def enterStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        if ctx.IF() and self.enter_method and self.enter_class:
            self.method_count_Cyclomatic += 1

    # while statement

    def enterStatement4(self, ctx: JavaParserLabeled.Statement4Context):
        if ctx.WHILE() and self.enter_method and self.enter_class:
            self.method_count_Cyclomatic += 1

    # try-catch
    def enterStatement6(self, ctx: JavaParserLabeled.Statement6Context):
        if ctx.catchClause() and self.enter_method and self.enter_class:
            self.method_count_Cyclomatic += 1

    # for
    def enterStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        if ctx.FOR() and self.enter_method and self.enter_class:
            self.method_count_Cyclomatic += 1

    # do-while
    def enterStatement5(self, ctx: JavaParserLabeled.Statement5Context):
        if ctx.DO() and self.enter_method and self.enter_class:
            self.method_count_Cyclomatic += 1

    # enter-case

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        longname = (
            self.packagename
            + "."
            + countParents(ctx)
            + "."
            + ctx.IDENTIFIER().getText()
        )
        print("method", longname, self.method_count_Cyclomatic)
        self.method_long_names[longname] = self.method_count_Cyclomatic

        if self.max_value < self.method_count_Cyclomatic:
            self.max_value = self.method_count_Cyclomatic

        self.method_count_Cyclomatic = 1
        self.enter_method = False

    # count cases
    def enterSwitchLabel(self, ctx: JavaParserLabeled.SwitchLabelContext):
        if ctx.CASE() and self.enter_method and self.enter_class:
            self.method_count_Cyclomatic += 1

    def enterBlockStatement1(self, ctx: JavaParserLabeled.BlockStatement1Context):
        self.enter_block = True

    def exitBlockStatement1(self, ctx: JavaParserLabeled.BlockStatement1Context):
        self.enter_block = False

    # count ?
    def enterExpression20(self, ctx: JavaParserLabeled.Expression20Context):
        if ctx.QUESTION() and self.enter_method and self.enter_class:
            self.method_count_Cyclomatic += 1

    # count && &

    def enterExpression18(self, ctx: JavaParserLabeled.Expression18Context):
        if ctx.AND() and self.enter_method and self.enter_block and self.enter_class:
            self.method_count_Cyclomatic += 1

    def enterExpression15(self, ctx: JavaParserLabeled.Expression15Context):
        if ctx.BITAND() and self.enter_method and self.enter_block and self.enter_class:
            self.method_count_Cyclomatic += 1

    def enterExpression19(self, ctx: JavaParserLabeled.Expression19Context):
        if ctx.OR() and self.enter_method and self.enter_block and self.enter_class:
            self.method_count_Cyclomatic += 1

    def enterExpression17(self, ctx: JavaParserLabeled.Expression17Context):
        if ctx.BITOR() and self.enter_method and self.enter_block and self.enter_class:
            self.method_count_Cyclomatic += 1

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        longname = (
            self.packagename + "." + countParents(ctx) + ctx.IDENTIFIER().getText()
        )
        self.classes[longname] = self.max_value


# add and or counter
# interfaces
# complete essential
def cyclomatic_strict(ent_model=None):
    p = Project()
    listener = CyclomaticStrictListener()
    lexer = JavaLexer(InputStream(ent_model.contents()))
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return_tree = parser.compilationUnit()
    p.Walk(reference_listener=listener, parse_tree=return_tree)
    return listener.method_count_Cyclomatic
