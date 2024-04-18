from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from openunderstand.analysis_passes import class_properties



class CoupleAndCoupleBy(JavaParserLabeledListener):
    """
    #Todo: Implementing the ANTLR listener pass for Java Couple and Java Coupleby reference kind
    """

    def __init__(self):
        self.Couple = []
        self.packageName = ""
        self.Imports = {}
        self.Modifiers = []
        self.dic = {}
        self.file = None
        self.classes = {}
        self.classlongname = ""
        self.couplebyrefrences = []
        self.news = []
        self.extend = False
        self.classx = False

    def set_file(self, filex):
        self.file = filex

    def set_classesx(self, classesx):
        self.classes = classesx

    def set_couples(self, couples):
        self.Couple = couples

    @property
    def get_couples(self):
        return self.Couple

    @property
    def get_classes(self):
        return self.classes

    def extract_original_text(self, ctx):
        token_source = ctx.start.getTokenSource()
        input_stream = token_source.inputStream
        start, stop = ctx.start.start, ctx.stop.stop
        return input_stream.getText(start, stop)

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if True:
            scope_parents = class_properties.ClassPropertiesListener.findParents(ctx)
            if len(scope_parents) == 1:
                scope_longname = scope_parents[0]
            else:
                scope_longname = ".".join(scope_parents)
            [line, col] = str(ctx.start).split(",")[3].split(":")
            self.classlongname = self.packageName + "." + scope_longname
            self.dic = {
                "scope_kind": "Class",
                "scope_name": ctx.IDENTIFIER().__str__(),
                "scope_longname": self.packageName + "." + scope_longname,
                "scope_parent": scope_parents[-2] if len(scope_parents) >= 2 else None,
                "scope_contents": self.extract_original_text(ctx),
                "scope_modifiers": self.Modifiers,
                "File": self.file,
                "line": line,
                "col": col[:-1],
            }
            if ctx.EXTENDS() != None:
                self.extend = True
                self.classx = True

            self.Modifiers = []

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.packageName = ctx.qualifiedName().getText()

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        imported_class_longname = ctx.qualifiedName().getText()
        imported_class_name = imported_class_longname.split(".")[-1]
        self.Imports[imported_class_name] = imported_class_longname

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):

        self.dic["type_ent_longname"] = self.couplebyrefrences
        self.Couple.append(self.dic)

        self.classes[self.classlongname] = self.dic

        self.classlongname = ""
        self.couplebyrefrences = []
        self.news = []

    def enterClassOrInterfaceModifier(
        self, ctx: JavaParserLabeled.ClassOrInterfaceModifierContext
    ):
        parent = ctx.parentCtx
        if type(parent).__name__ == "TypeDeclarationContext":
            self.Modifiers.append(ctx.getText())

    def enterClassOrInterfaceType(
        self, ctx: JavaParserLabeled.ClassOrInterfaceTypeContext
    ):
        prnt1 = ctx.parentCtx
        keyname = None

        if type(prnt1).__name__ == "TypeTypeContext":
            if type(prnt1.parentCtx).__name__ != "ClassDeclarationContext":
                typereferenced = ctx.getText()
                if typereferenced in self.Imports:
                    keyname = self.Imports[typereferenced]
                else:
                    keyname = self.packageName + "." + typereferenced
        if keyname != None and keyname not in self.couplebyrefrences:
            self.couplebyrefrences.append(keyname)

        if self.extend and self.classx:
            extendx = ctx.IDENTIFIER()[0].getText()
            key2 = ""
            if extendx in self.Imports:
                key2 = self.Imports[extendx]
            else:
                key2 = self.packageName + "." + extendx

            if key2 != None and key2 not in self.couplebyrefrences:
                self.couplebyrefrences.append(key2)
            self.extend = False
            self.classx = False

    def enterExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        expression = ctx.getText()

        exp = expression.split(".")
        classnamemain = exp[0]
        typex = type(ctx.children[0]).__name__

        if ctx.DOT() != None:
            if classnamemain in self.Imports:
                reference = self.Imports[classnamemain]
                if reference not in self.couplebyrefrences:
                    self.couplebyrefrences.append(reference)

            if typex == "Expression0Context":
                if (
                    classnamemain not in self.Imports
                    and classnamemain not in self.couplebyrefrences
                    and classnamemain != "this"
                    and classnamemain not in self.news
                ):
                    self.couplebyrefrences.append(classnamemain)

    def enterExpression4(self, ctx: JavaParserLabeled.Expression4Context):
        name = ctx.children[1]
        parent = ctx.parentCtx

        createdname = name.children[0].getText()

        if type(parent).__name__ == "VariableInitializer1Context":
            parent2 = parent.parentCtx
            if type(parent2).__name__ == "VariableDeclaratorContext":
                parent3 = parent.parentCtx
                if parent3.ASSIGN() != None:
                    if parent3.ASSIGN().getText() == "=":
                        self.news.append(parent3.children[0].getText())

        if createdname in self.Imports:
            reference = self.Imports[createdname]
            if reference not in self.couplebyrefrences:
                self.couplebyrefrences.append(reference)
        if "." in createdname:
            if createdname not in self.couplebyrefrences:
                self.couplebyrefrences.append(createdname)

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.news = []

    # def enterFormalParameter(self, ctx:JavaParserLabeled.FormalParameterContext):
    #     self.couplebyrefrences.pop()
    #     #fieldparametersarenotclasses
