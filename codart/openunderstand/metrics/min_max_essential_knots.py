from antlr4 import *
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from openunderstand.ounderstand.project import Project


class MinEssentialKnots(JavaParserLabeledListener):
    def __init__(self):
        self.stack = []
        self.counter = 0
        self.maxEssentialKnots = 0
        self.method_counter = 0
        self.method_maxEssentialKnots = 0

    # return
    def enterStatement10(self, ctx: JavaParserLabeled.Statement10Context):
        new_num = 0
        new_method_num = 0
        new_max = 0
        new_method_max = 0
        p = ctx

        while not type(p) == JavaParserLabeled.compilationUnit:

            p = p.parentCtx
            # if statement
            if type(p) == JavaParserLabeled.Statement2Context:
                new_num += 1
                new_method_num += 1

            # While Statement
            if type(p) == JavaParserLabeled.Statement4Context:
                new_num += 1
                new_max += 2
                new_method_num += 1
                new_method_max += 2

            # Do while statement
            if type(p) == JavaParserLabeled.Statement5Context:
                new_num += 1
                new_max += 2
                new_method_num += 1
                new_method_max += 2

            # For Statement
            if type(p) == JavaParserLabeled.Statement3Context:
                new_num += 1
                new_max += 2
                new_method_num += 1
                new_method_max += 2

            # Stop On Method
            if type(p) == JavaParserLabeled.MethodDeclarationContext:
                break

        if self.counter < new_num:
            self.counter = new_num

        if self.maxEssentialKnots < new_max + new_num:
            self.maxEssentialKnots = new_max + new_num

        if self.method_counter < new_method_num:
            self.method_counter = new_method_num

        if self.method_maxEssentialKnots < new_method_max + new_method_num:
            self.method_maxEssentialKnots = new_method_max + new_method_num

    # continue
    def enterStatement13(self, ctx: JavaParserLabeled.Statement13Context):
        new_num = 0
        new_method_num = 0
        new_max = 0
        new_method_max = 0
        p = ctx

        while not type(p) == JavaParserLabeled.compilationUnit:

            p = p.parentCtx
            # if statement
            if type(p) == JavaParserLabeled.Statement2Context:
                new_num += 1
                new_method_num += 1

            # While Statement
            if type(p) == JavaParserLabeled.Statement4Context:
                new_max += 2
                new_method_max += 2
                break

            # Do while statement
            if type(p) == JavaParserLabeled.Statement5Context:
                new_max += 2
                new_method_max += 2
                break

            # For Statement
            if type(p) == JavaParserLabeled.Statement3Context:
                new_max += 2
                new_method_max += 2
                break

        if self.counter < new_num:
            self.counter = new_num

        if self.maxEssentialKnots < new_max + new_num:
            self.maxEssentialKnots = new_max + new_num

        if self.method_counter < new_method_num:
            self.method_counter = new_method_num

        if self.method_maxEssentialKnots < new_method_max + new_method_num:
            self.method_maxEssentialKnots = new_method_max + new_method_num

    # break
    def enterStatement12(self, ctx: JavaParserLabeled.Statement12Context):
        new_num = 0
        new_method_num = 0
        new_max = 0
        new_method_max = 0
        p = ctx

        while not type(p) == JavaParserLabeled.compilationUnit:

            p = p.parentCtx
            # if statement
            if type(p) == JavaParserLabeled.Statement2Context:
                new_num += 1
                new_method_num += 1

            # While Statement
            if type(p) == JavaParserLabeled.Statement4Context:
                new_num += 1
                new_max += 2
                new_method_num += 1
                new_method_max += 2
                break
            # Do while statement
            if type(p) == JavaParserLabeled.Statement5Context:
                new_num += 1
                new_max += 2
                new_method_num += 1
                new_method_max += 2
                break

            # For Statement
            if type(p) == JavaParserLabeled.Statement3Context:
                new_num += 1
                new_max += 2
                break

            # Ignore Switch Case
            if type(p) == JavaParserLabeled.Statement8Context:
                print("Enter Switch Case")
                new_num = 0
                new_max = 0
                new_method_num += 1
                new_method_max += 2
                break

        if self.counter < new_num:
            self.counter = new_num

        if self.maxEssentialKnots < new_max + new_num:
            self.maxEssentialKnots = new_max + new_num

        if self.method_counter < new_method_num:
            self.method_counter = new_method_num

        if self.method_maxEssentialKnots < new_method_max + new_method_num:
            self.method_maxEssentialKnots = new_method_max + new_method_num

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.method_counter = 0
        self.method_maxEssentialKnots = 0

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        print(
            "Min and Max Knots of ",
            ctx.IDENTIFIER().getText(),
            "is : ",
            self.method_counter,
            ", ",
            self.method_maxEssentialKnots,
        )


def min_max_essential_knots(ent_model=None, enable: bool = True):
    p = Project()
    listener = MinEssentialKnots()
    lexer = JavaLexer(InputStream(ent_model.contents()))
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return_tree = parser.compilationUnit()
    p.Walk(reference_listener=listener, parse_tree=return_tree)
    if enable:
        return listener.method_counter
    else:
        return listener.method_maxEssentialKnots
