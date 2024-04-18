from antlr4 import *
import os
from fnmatch import fnmatch
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class Cyclomatics(JavaParserLabeledListener):
    def __init__(self):
        self.switches = 0
        self.cases = 0
        self.ands = 0
        self.ors = 0
        self.wtfs = 0
        self.catches = 0
        self.dos = 0
        self.whiles = 0
        self.fors = 0
        self.ifs = 0

    def get_sum_cyclomatics(self):
        return (
            self.switches
            + self.cases
            + self.ands
            + self.ors
            + self.wtfs
            + self.catches
            + self.dos
            + self.whiles
            + self.fors
            + self.ifs
        )

    # switch statement
    def enterStatement8(self, ctx: JavaParserLabeled.Statement8Context):
        self.switches += 1

    # case
    def enterSwitchBlockStatementGroup(
        self, ctx: JavaParserLabeled.SwitchBlockStatementGroupContext
    ):
        self.cases += 1

    # ?
    def enterExpression20(self, ctx: JavaParserLabeled.Expression20Context):
        self.wtfs += 1

    # and
    def enterExpression18(self, ctx: JavaParserLabeled.Expression18Context):
        self.ands += 1

    # or
    def enterExpression19(self, ctx: JavaParserLabeled.Expression19Context):
        self.ors += 1

    # catch
    def enterStatement6(self, ctx: JavaParserLabeled.Statement6Context):
        self.catches += 1

    # do
    def enterStatement5(self, ctx: JavaParserLabeled.Statement5Context):
        self.dos += 1

    # whiles
    def enterStatement4(self, ctx: JavaParserLabeled.Statement4Context):
        self.whiles += 1

    # for
    def enterStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        self.fors += 1

    # if
    def enterStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        self.ifs += 1


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        elif fnmatch(fullPath, "*.java"):
            allFiles.append(fullPath)

    return allFiles


def get_sum_of_cyclomatics(ent_model=None):
    # at first we should Stream text from input file
    inputfile = InputStream(ent_model.contents())
    # then we must use lexer
    lex = JavaLexer(inputfile)
    # then we should tokenize that
    toked = CommonTokenStream(lex)
    # at last we should parse tokenized
    parsed = JavaParserLabeled(toked)
    ptree = parsed.compilationUnit()

    listener = Cyclomatics()
    treewalker = ParseTreeWalker()
    treewalker.walk(t=ptree, listener=listener)
    return listener.get_sum_cyclomatics()
