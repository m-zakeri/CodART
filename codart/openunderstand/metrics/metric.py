from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from halstead import main_


class DSCmetric(JavaParserLabeledListener):
    def __init__(self):
        self.arr = []
        self.tmp = []
        self.name = []
        self.null = []
        self.mmd = []

    @property
    def get_arr(self):
        return self.arr

    @property
    def get_tmp(self):
        return self.tmp

    @property
    def get_name(self):
        return self.name

    @property
    def get_mmd(self):
        return self.mmd

    def enterBlockStatement1(self, ctx: JavaParserLabeled.BlockStatement1Context):
        try:
            self.arr.append(ctx.statement().RETURN().getText())
        except:
            pass

    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        parent = ctx.parentCtx
        parent = parent.parentCtx

        try:
            self.null.append(parent.RETURN().getText())
            self.tmp.append(ctx.getText())

        except:
            pass

    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        if ctx.ASSIGN().getText() == "=":
            parent = ctx.parentCtx
            parent = parent.parentCtx
            parent = parent.parentCtx
            parent = parent.parentCtx
            parent = parent.parentCtx
            parent = parent.parentCtx

            # remove constructor
            try:
                parent.memberDeclaration().constructorDeclaration()

            except:
                self.mmd.append(ctx.getChild(2).getText())

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.name.append(ctx.IDENTIFIER().getText())


class DSCmetric2(JavaParserLabeledListener):
    def __init__(self, file_path):
        self.assign = 0
        self.add = 0
        self.sub = 0
        self.mul = 0
        self.div = 0
        self.add_assign = 0
        self.mul_assign = 0
        self.sub_assign = 0
        self.div_assign = 0
        self.path = file_path

    @property
    def get_res(self):
        main_(self.path)

    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        if ctx.getChild(2).getText() == "=":
            self.assign += 1
        elif ctx.getChild(2).getText() == "+=":
            self.add_assign += 1
        elif ctx.getChild(2).getText() == "-=":
            self.sub_assign += 1
        elif ctx.getChild(2).getText() == "*=":
            self.mul_assign += 1
        elif ctx.getChild(2).getText() == "/=":
            self.div_assign += 1

    def enterExpression9(self, ctx: JavaParserLabeled.Expression9Context):
        if ctx.getChild(2).getText() == "*":
            self.mul += 1
        elif ctx.getChild(2).getText() == "/":
            self.div += 1

    def enterExpression10(self, ctx: JavaParserLabeled.Expression10Context):
        if ctx.getChild(2).getText() == "+":
            self.add += 1
        elif ctx.getChild(2).getText() == "-":
            self.sub += 1
