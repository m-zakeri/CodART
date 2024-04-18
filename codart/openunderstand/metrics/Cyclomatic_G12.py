from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from openunderstand.analysis_passes import class_properties


def countParents(ctx):
    scope_parents = class_properties.ClassPropertiesListener.findParents(ctx)
    if len(scope_parents) == 1:
        scope_longname = scope_parents[0]
    else:
        scope_longname = ".".join(scope_parents)
    return scope_longname


class CyclomaticListener(JavaParserLabeledListener):
    def __init__(self, class_):
        self.method_count_Cyclomatic = 1
        self.file = ""
        self.enter_method = False
        self.enter_block = False
        self.enter_class = False
        self.method_long_names = {}
        self.packagename = ""
        self.class_name = class_
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

    # parent and long name by parentclasses
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
        # print('method' , longname , self.method_count_Cyclomatic)
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

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        longname = (
            self.packagename + "." + countParents(ctx) + ctx.IDENTIFIER().getText()
        )
        self.classes[longname] = self.max_value
        self.max_value = 0


def get_parse_tree(file_path):
    file = FileStream(file_path)
    lexer = JavaLexer(file)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return parser.compilationUnit()
