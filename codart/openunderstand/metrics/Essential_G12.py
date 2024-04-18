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


class EssentialMetricListener(JavaParserLabeledListener):
    def __init__(self, method_entity=None):
        self.method = method_entity
        self.method_entered = False
        self.index = 0
        self.layers = []
        self.counts = []
        self.count_essential_metric = 1
        self.entered_switch = False
        self.methods = {}
        self.classes = {}
        self.packagename = ""

    @property
    def essential_metric(self):
        return self.count_essential_metric

    @property
    def get_packagename(self):
        return self.packagename

    @property
    def get_methods(self):
        return self.methods

    @property
    def get_classes(self):
        return self.classes

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.packagename = ctx.qualifiedName().getText()

    # enter if clause
    def enterStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        if self.method is not None:
            if self.method_entered:
                self.index += 1
                if ctx.ELSE() is not None:
                    self.layers.append(1)
                else:
                    self.layers.append(0)
                self.counts.append(0)
        else:
            self.index += 1
            if ctx.ELSE() is not None:
                self.layers.append(1)
            else:
                self.layers.append(0)
            self.counts.append(0)

    def exitStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        self.index -= 1
        if self.index == 0:
            while len(self.layers) != 0:
                last = self.layers.pop(0)
                if last > 0:
                    self.count_essential_metric += self.counts.pop(0) + last
                else:
                    break
            self.layers = []
            self.counts = []

    # enter while loop
    def enterStatement4(self, ctx: JavaParserLabeled.Statement4Context):
        if self.method is not None:
            if self.method_entered:
                if len(self.layers) == 0:
                    self.count_essential_metric += 1
                else:
                    self.counts[-1] += 1
        else:
            if len(self.layers) == 0:
                self.count_essential_metric += 1
            else:
                self.counts[-1] += 1

    # enter for loop
    def enterStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        if self.method is not None:
            if self.method_entered:
                if len(self.layers) == 0:
                    self.count_essential_metric += 1
                else:
                    self.counts[-1] += 1
        else:
            if len(self.layers) == 0:
                self.count_essential_metric += 1
            else:
                self.counts[-1] += 1

    # enter do-while class
    def enterStatement5(self, ctx: JavaParserLabeled.Statement5Context):
        if self.method is not None:
            if self.method_entered:
                if len(self.layers) == 0:
                    self.count_essential_metric += 1
                else:
                    self.counts[-1] += 1
        else:
            if len(self.layers) == 0:
                self.count_essential_metric += 1
            else:
                self.counts[-1] += 1

    # enter switch clause
    def enterStatement8(self, ctx: JavaParserLabeled.Statement8Context):
        self.entered_switch = True

    def exitStatement8(self, ctx: JavaParserLabeled.Statement8Context):
        self.entered_switch = False

    def enterStatement12(self, ctx: JavaParserLabeled.Statement12Context):
        if not self.entered_switch:
            if self.layers[-1] < 2:
                self.layers[-1] += 1

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.method is not None:
            if self.method == " ":
                self.method_entered = True

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        longname = (
            self.packagename
            + "."
            + countParents(ctx)
            + "."
            + ctx.IDENTIFIER().getText()
        )
        self.methods[longname] = self.count_essential_metric
        self.method_entered = False
        self.count_essential_metric = 1
        self.index = 0
        self.layers = []
        self.counts = []

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.methods = {}

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        longname = (
            self.packagename + "." + countParents(ctx) + ctx.IDENTIFIER().getText()
        )
        val = self.methods.values()
        list_of_val = list(val)
        max_val = 1
        if len(list_of_val) != 0:
            max_val = max(list_of_val)
        self.classes[longname] = max_val


def essential(ent_model=None):
    p = Project()
    listener = EssentialMetricListener()
    lexer = JavaLexer(InputStream(ent_model.contents()))
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return_tree = parser.compilationUnit()
    p.Walk(reference_listener=listener, parse_tree=return_tree)
    return listener.count_essential_metric
