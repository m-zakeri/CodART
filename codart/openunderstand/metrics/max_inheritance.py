from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class FindAllClasses(JavaParserLabeledListener):
    def __init__(self):
        self.classes = {}
        self.class_names = []

    def get_classes(self):
        return self.classes

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.class_names.append(ctx.IDENTIFIER().getText())


class FindAllInheritances(JavaParserLabeledListener):
    def __init__(self, c):
        self.__dsc = 0
        self.name = ""
        self.classes = c
        self.is_interface = False
        self.intered_class = False
        self.enterd_class_body = False
        self.current_class = JavaParserLabeled.ClassDeclarationContext

    @property
    def get_design_size(self):
        return self.__dsc

    @property
    def get_classes(self):
        return self.classes

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.name = ctx.IDENTIFIER().getText()
        self.intered_class = True
        self.is_interface = False

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        self.enterd_class_body = True

    def exitClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        self.enterd_class_body = False

    def enterTypeList(self, ctx: JavaParserLabeled.TypeListContext):
        self.is_interface = True

    def exitTypeList(self, ctx: JavaParserLabeled.TypeListContext):
        self.is_interface = False

    def enterClassOrInterfaceType(
        self, ctx: JavaParserLabeled.ClassOrInterfaceTypeContext
    ):
        if not self.is_interface:
            if not self.enterd_class_body:
                try:
                    self.classes[self.name].append(ctx.children[0].getText())
                except:
                    x = 2

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.name = ""
        self.intered_class = False
        after_extends = False
