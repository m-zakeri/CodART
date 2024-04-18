from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from antlr4 import *
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaLexer import JavaLexer
from openunderstand.ounderstand.project import Project

from openunderstand.metrics.utils_g10 import get_keys


class StatementListener(JavaParserLabeledListener):
    def __init__(self):
        self.repository = {}
        self.counter = 0

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.counter += 1

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        self.counter += 1

    def enterInterfaceMethodDeclaration(
        self, ctx: JavaParserLabeled.InterfaceMethodDeclarationContext
    ):
        self.update_repository(ctx, 1)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.update_repository(ctx, 1)

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        self.update_repository(ctx, 1)

    def enterLocalVariableDeclaration(
        self, ctx: JavaParserLabeled.LocalVariableDeclarationContext
    ):
        self.update_repository(ctx, 1)

    # for
    def enterStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        self.update_repository(ctx, 1)

    # semi-colon
    def enterStatement14(self, ctx: JavaParserLabeled.Statement14Context):
        self.update_repository(ctx, 1)

    # call
    def enterStatement15(self, ctx: JavaParserLabeled.Statement15Context):
        self.update_repository(ctx, 1)

    def enterAnnotationMethodOrConstantRest0(
        self, ctx: JavaParserLabeled.AnnotationMethodOrConstantRest0Context
    ):
        self.update_repository(ctx, 1)

    def update_repository(self, ctx, increment):
        self.counter += increment
        keys = get_keys(ctx)
        for key in keys:
            if key in self.repository:
                self.repository[key] += increment
            else:
                new_dict = {key: 0}
                new_dict[key] += increment
                self.repository.update(new_dict)


def statement_counter_delc(ent_model=None):
    p = Project()
    listener = StatementListener()
    lexer = JavaLexer(InputStream(ent_model.contents()))
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return_tree = parser.compilationUnit()
    p.Walk(reference_listener=listener, parse_tree=return_tree)
    return listener.counter
