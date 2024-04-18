"""This module is for managing project files and walking on parse tree"""

__author__ = "Navid Mousavizadeh, Amir Mohammad Sohrabi, Sara Younesi, Deniz Ahmadi"
__copyright__ = "Copyright 2022, The OpenUnderstand Project, Iran University of Science and technology"
__credits__ = [
    "Dr.Parsa",
    "Dr.Zakeri",
    "Mehdi Razavi",
    "Navid Mousavizadeh",
    "Amir Mohammad Sohrabi",
    "Sara Younesi",
    "Deniz Ahmadi",
]
__license__ = "GPL"
__version__ = "1.0.0"

from antlr4 import *

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from analysis_passes.entity_manager_G11 import (
    get_created_entity_longname,
    get_all_files,
    get_created_entity_id,
)
from oudb.api import open as db_open, create_db


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


class CyclomaticModifiedMetric:
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
            listener = CyclomaticModifiedMetricListener(method_entity=self.method)
        else:
            self.files = get_all_files()
            listener = CyclomaticModifiedMetricListener()
        for file_content in self.files:
            parse_tree = AntlrHandler.Parse(file_content)
            AntlrHandler.Walk(listener, parse_tree)
        print(listener.cyclomatic_modified_metric)


class CyclomaticModifiedMetricListener(JavaParserLabeledListener):
    def __init__(self, method_entity=None):
        self.count_cyclomatic_modified_metric = 0
        self.method = method_entity
        self.method_entered = False

    @property
    def cyclomatic_modified_metric(self):
        return self.count_cyclomatic_modified_metric

    # enter if clause
    def enterStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:

            self.count_cyclomatic_modified_metric += 1

    # enter while loop
    def enterStatement4(self, ctx: JavaParserLabeled.Statement4Context):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:

            self.count_cyclomatic_modified_metric += 1

    # enter for loop
    def enterStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:

            self.count_cyclomatic_modified_metric += 1

    def enterExpression9(self, ctx: JavaParserLabeled.Expression9Context):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:
            self.count_cyclomatic_modified_metric += 1

    def enterExpression10(self, ctx: JavaParserLabeled.Expression10Context):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:
            self.count_cyclomatic_modified_metric += 1

    # enter switch clause
    def enterStatement8(self, ctx: JavaParserLabeled.Statement8Context):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:
            self.count_cyclomatic_modified_metric += 1

    # enter do-while class
    def enterStatement5(self, ctx: JavaParserLabeled.Statement5Context):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:
            self.count_cyclomatic_modified_metric += 1

    # enter catch clause
    def enterStatement6(self, ctx: JavaParserLabeled.Statement6Context):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:
            self.count_cyclomatic_modified_metric += 1

    def enterGenericMethodDeclaration(
        self, ctx: JavaParserLabeled.GenericMethodDeclarationContext
    ):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:
            self.count_cyclomatic_modified_metric += 1

    def enterGenericConstructorDeclaration(
        self, ctx: JavaParserLabeled.GenericConstructorDeclarationContext
    ):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:
            self.count_cyclomatic_modified_metric += 1

    def enterConstructorDeclaration(
        self, ctx: JavaParserLabeled.ConstructorDeclarationContext
    ):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:
            self.count_cyclomatic_modified_metric += 1

    def enterEnumDeclaration(self, ctx: JavaParserLabeled.EnumDeclarationContext):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:
            self.count_cyclomatic_modified_metric += 1

    def enterLambdaExpression(self, ctx: JavaParserLabeled.LambdaExpressionContext):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:
            self.count_cyclomatic_modified_metric += 1

    # enter ? clause
    def enterExpression20(self, ctx: JavaParserLabeled.Expression20Context):
        if self.method is not None:
            if self.method_entered:
                self.count_cyclomatic_modified_metric += 1
        else:
            self.count_cyclomatic_modified_metric += 1

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.method is not None:
            if ctx.IDENTIFIER().getText() == self.method._name:
                self.method_entered = True

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.method is not None:
            if ctx.IDENTIFIER().getText() == self.method._name:
                self.method_entered = False


if __name__ == "__main__":
    create_db("../../benchmark2_database.oudb", project_dir="..\..\benchmark")
    db = db_open("../../benchmark2_database.oudb")
    try:
        cyclomatic_modified_manager = CyclomaticModifiedMetric()
    except Exception as e:
        print("Error:", e)
