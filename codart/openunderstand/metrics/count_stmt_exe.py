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

    # return
    def enterStatement10(self, ctx: JavaParserLabeled.Statement10Context):
        self.update_repository(ctx, 1)

    # for
    def enterStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        self.update_repository(ctx, 2)

    # break
    def enterStatement12(self, ctx: JavaParserLabeled.Statement12Context):
        self.update_repository(ctx, 1)

    # throw
    def enterStatement11(self, ctx: JavaParserLabeled.Statement11Context):
        self.update_repository(ctx, 1)

    # continue
    def enterStatement13(self, ctx: JavaParserLabeled.Statement13Context):
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


def statement_counter_exe(ent_model=None):
    p = Project()
    listener = StatementListener()
    lexer = JavaLexer(InputStream(ent_model.contents()))
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return_tree = parser.compilationUnit()
    p.Walk(reference_listener=listener, parse_tree=return_tree)
    return listener.counter
