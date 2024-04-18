"""This module is for managing project files and walking on parse tree"""

__author__ = "Navid Mousavizadeh, Amir Mohammad Sohrabi, Sara Younesi, Deniz Ahmadi"
__copyright__ = "Copyright 2022, The OpenUnderstand Project, Iran University of Science and technology"
__credits__ = [
    "AminHZ" "Dr.Parsa",
    "Dr.Zakeri",
    "Mehdi Razavi",
    "Navid Mousavizadeh",
    "Amir Mohammad Sohrabi",
    "Sara Younesi",
    "Deniz Ahmadi",
]
__license__ = "GPL"
__version__ = "1.0.0"

from openunderstand.ounderstand.project import Project
from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from openunderstand.analysis_passes.entity_manager_g11 import (
    get_created_entity_longname,
    get_all_files,
    get_created_entity_id,
)


class AntlrHandler:
    @staticmethod
    def Parse(entity_content):
        file_stream = InputStream(entity_content)
        lexer = JavaLexer(file_stream)
        tokens = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokens)
        return_tree = parser.compilationUnit()
        return return_tree

    @staticmethod
    def Walk(reference_listener, parse_tree):
        walker = ParseTreeWalker()
        walker.walk(listener=reference_listener, t=parse_tree)


class EssentialMetric:
    def __init__(self, entity_longname="Project"):
        """get project or method entity and will calculate Cyclomatic Modified Metric of it."""
        self.files = []
        self.method = None
        if entity_longname != "Project":
            entity = get_created_entity_longname(entity_longname)
            if entity is None:
                raise Exception("Couldn't find entity.")
            if not 3 <= int(entity._kind._id) <= 66:
                raise Exception("Entity is not a method.")
            current = entity
            parent = get_created_entity_id(current._parent_id)
            while current._parent_id is not None and not (70 <= parent._kind._id <= 73):
                current = get_created_entity_id(current._parent_id)
                parent = get_created_entity_id(current._parent_id)
            self.files.append(current._contents)
            self.method = entity
            listener = KnotsMetricListener(method_entity=self.method)
        else:
            self.files = get_all_files()
            listener = KnotsMetricListener()
        for file_content in self.files:
            parse_tree = AntlrHandler.Parse(file_content)
            AntlrHandler.Walk(listener, parse_tree)
        print(listener.knots_metric)


class KnotsMetricListener(JavaParserLabeledListener):
    def __init__(self, method_entity=None):
        self.count_knots_metric = 0
        self.if_else_count = 0
        self.if_count = 0
        self.loop_count = 0
        self.case_count = 0
        self.catch_count = 0
        self.break_count = 0
        self.guide = []
        self.method = method_entity
        self.entered_switch = False
        self.method_entered = False

    @property
    def knots_metric(self):
        return self.count_knots_metric

    # enter if clause
    def enterStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        if self.method is not None:
            if self.method_entered:
                if ctx.ELSE() is not None:
                    self.count_knots_metric += 1
                    self.if_else_count += 1
                    self.guide.append(1)
                else:
                    self.if_count += 1
                    self.guide.append(0)
        else:
            if ctx.ELSE() is not None:
                self.count_knots_metric += 1
                self.if_else_count += 1
                self.guide.append(1)
            else:
                self.if_count += 1
                self.guide.append(0)

    def exitStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        last = self.guide.pop()
        if last == 0:
            self.if_count -= 1
        else:
            self.if_else_count -= 1

    # enter while loop
    def enterStatement4(self, ctx: JavaParserLabeled.Statement4Context):
        if self.method is not None:
            if self.method_entered:
                self.loop_count += 1
        else:
            self.loop_count += 1

    def exitStatement4(self, ctx: JavaParserLabeled.Statement4Context):
        if self.loop_count > 0:
            self.loop_count -= 1

    # enter for loop
    def enterStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        if self.method is not None:
            if self.method_entered:
                self.loop_count += 1
        else:
            self.loop_count += 1

    def exitStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        if self.loop_count > 0:
            self.loop_count -= 1

    # enter case clause
    def enterSwitchLabel(self, ctx: JavaParserLabeled.SwitchLabelContext):
        if "case" in ctx.getText():
            if self.method is not None:
                if self.method_entered:
                    self.case_count += 1
                    self.count_knots_metric += 1
            else:
                self.case_count += 1
                self.count_knots_metric += 1

    def exitSwitchLabel(self, ctx: JavaParserLabeled.SwitchLabelContext):
        if self.case_count > 0:
            self.case_count -= 1

    # enter do-while class
    def enterStatement5(self, ctx: JavaParserLabeled.Statement5Context):
        if self.method is not None:
            if self.method_entered:
                self.loop_count += 1
        else:
            self.loop_count += 1

    def exitStatement5(self, ctx: JavaParserLabeled.Statement5Context):
        if self.loop_count > 0:
            self.loop_count -= 1

    # enter catch clause
    def enterStatement6(self, ctx: JavaParserLabeled.Statement6Context):
        if self.method is not None:
            if self.method_entered:
                self.catch_count += 1
                self.count_knots_metric += 1
        else:
            self.catch_count += 1
            self.count_knots_metric += 1

    def exitStatement6(self, ctx: JavaParserLabeled.Statement6Context):
        if self.catch_count > 0:
            self.catch_count -= 1

    # enter switch clause
    def enterStatement8(self, ctx: JavaParserLabeled.Statement8Context):
        self.entered_switch = True

    def exitStatement8(self, ctx: JavaParserLabeled.Statement8Context):
        self.entered_switch = False

    def enterStatement12(self, ctx: JavaParserLabeled.Statement12Context):
        if not self.entered_switch:
            self.count_knots_metric += (
                self.if_else_count
                + self.case_count
                + self.if_count
                + self.loop_count
                + self.catch_count
                + self.break_count
            )
            self.break_count += 1

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.method is not None:
            if ctx.IDENTIFIER().getText() == self.method._name:
                self.method_entered = True

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.method is not None:
            if ctx.IDENTIFIER().getText() == self.method._name:
                self.method_entered = False


def knot(ent_model=None):
    p = Project()
    listener = KnotsMetricListener()
    lexer = JavaLexer(InputStream(ent_model.contents()))
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return_tree = parser.compilationUnit()
    p.Walk(reference_listener=listener, parse_tree=return_tree)
    return listener.count_essential_metric
