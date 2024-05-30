from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaLexer import JavaLexer
from antlr4 import *
import pandas as pd


def stringify(dict):
    res_dict = {}
    for i in dict:
        res_dict[i] = str(dict[i])
    return res_dict


class LineOfCode(JavaParserLabeledListener):
    def __init__(self, ent_model=None):
        self.tokens = JavaLexer(InputStream(ent_model.contents())).getAllTokens()
        self.method_countLineExec = []
        self.method_countLineCode = []
        self.method_countLineComment = []
        self.method_countLineDecl = []
        self.class_countLineDecl = {}
        self.class_countLineExec = {}
        self.class_countLineCode = {}
        self.class_countLineComment = {}
        self.interface_countLineDecl = {}
        self.interface_countLineComment = {}
        self.interface_countLineCode = {}
        self.import_package = 0

    @property
    def get_countLineDecl(self):
        return {**self.class_countLineDecl, **self.interface_countLineDecl}

    @property
    def get_countLineCode(self):
        return {**self.class_countLineCode, **self.interface_countLineCode}

    @property
    def get_countLineComment(self):
        return {**self.class_countLineComment, **self.interface_countLineComment}

    @property
    def get_countLineExec(self):
        return self.class_countLineExec

    def enterCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        tokens = self.find(ctx.start, ctx.stop)
        self.class_countLineCode["file"] = len(tokens[0])
        self.class_countLineComment["file"] = self.countLineCodeComment(tokens[1])

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        file_counter = 0
        for i in self.class_countLineExec:
            if isinstance(self.class_countLineExec[i], int):
                file_counter += self.class_countLineExec[i]
        self.class_countLineExec["file"] = file_counter
        file_counter = 0
        for i in self.class_countLineDecl:
            if isinstance(self.class_countLineDecl[i], int):
                file_counter += self.class_countLineDecl[i]
        for i in self.interface_countLineDecl:
            if isinstance(self.interface_countLineDecl[i], int):
                file_counter += self.interface_countLineDecl[i]
        self.class_countLineDecl["file"] = file_counter + self.import_package

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        tokens = self.find(ctx.start, ctx.stop)
        self.import_package += len(tokens[0])

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        tokens = self.find(ctx.start, ctx.stop)
        self.import_package += len(tokens[0])

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        tokens = self.find(ctx.start, ctx.stop)
        decl = self.countLineCodeDecl(tokens[0])
        self.class_countLineDecl[ctx.IDENTIFIER().getText() + "num"] = decl
        self.method_countLineDecl.append(("class " + ctx.IDENTIFIER().getText(), decl))
        self.method_countLineComment.append(
            (
                "class " + ctx.IDENTIFIER().getText(),
                self.countLineCodeComment(tokens[1]),
            )
        )
        self.method_countLineCode.append(
            ("class " + ctx.IDENTIFIER().getText(), len(tokens[0]))
        )

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        tokens = self.find(ctx.start, ctx.stop)
        self.method_countLineDecl.append(
            ("method " + ctx.IDENTIFIER().getText(), self.countLineCodeDecl(tokens[0]))
        )
        self.method_countLineComment.append(
            (
                "method " + ctx.IDENTIFIER().getText(),
                self.countLineCodeComment(tokens[1]),
            )
        )
        self.method_countLineCode.append(
            ("method " + ctx.IDENTIFIER().getText(), len(tokens[0]))
        )

    def enterMethodBody(self, ctx: JavaParserLabeled.MethodBodyContext):
        tokens = self.find(ctx.start, ctx.stop)
        self.method_countLineExec.append(
            (
                "method " + ctx.parentCtx.IDENTIFIER().getText(),
                self.countLineCodeExec(tokens[0]),
            )
        )

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.class_countLineExec[ctx.IDENTIFIER().getText() + "num"] = 0
        for i in self.method_countLineExec:
            self.class_countLineExec[ctx.IDENTIFIER().getText() + "num"] += i[1]
        self.class_countLineExec[ctx.IDENTIFIER().getText()] = self.method_countLineExec
        self.method_countLineExec = []
        self.class_countLineDecl[ctx.IDENTIFIER().getText()] = self.method_countLineDecl
        self.method_countLineDecl = []
        self.class_countLineComment[ctx.IDENTIFIER().getText()] = (
            self.method_countLineComment
        )
        self.method_countLineComment = []
        self.class_countLineCode[ctx.IDENTIFIER().getText()] = self.method_countLineCode
        self.method_countLineCode = []
        # print(self.class_countLineDecl)

    def enterInterfaceDeclaration(
        self, ctx: JavaParserLabeled.InterfaceDeclarationContext
    ):
        tokens = self.find(ctx.start, ctx.stop)
        self.interface_countLineDecl["interface " + ctx.IDENTIFIER().getText()] = (
            self.countLineCodeDecl(tokens[0])
        )
        self.interface_countLineComment["interface " + ctx.IDENTIFIER().getText()] = (
            self.countLineCodeComment(tokens[1])
        )
        self.interface_countLineCode["interface " + ctx.IDENTIFIER().getText()] = len(
            tokens[0]
        )
        # print((self.interface_countLineDecl))

    def find(self, start, stop):
        all_lines = []
        singl_line = []
        all_tokens = []
        flag = False
        line = start.line
        for i in self.tokens:
            if i.line == start.line and i.column == start.column:
                flag = True
            if flag:
                all_tokens.append(i)
                if i.line == line and i.channel == 0:
                    singl_line.append(i)
                    # print((i))
                elif i.line > line and i.channel == 0:
                    line += i.line - line
                    # print(i)
                    all_lines.append(singl_line)
                    singl_line = []
                    singl_line.append(i)
            if i.line == stop.line and i.column == stop.column:
                all_lines.append(singl_line)
                flag = False
        return all_lines, all_tokens

    def countLineCodeComment(self, tokens):
        counter = 0
        for i in tokens:
            if i.type == 110 and i.channel == 1:
                counter += 1
            elif i.type == 109 and i.channel == 1:
                str = i.text.split()
                counter += len(str)
        return counter

    def countLineCodeDecl(self, tokens):
        counter = 0
        for j in tokens:
            for i in j:
                if (
                    i.type in [31, 9, 48, 27, 14, 8, 5, 28, 29, 20, 3, 37]
                ) and i.channel == 0:
                    # print(i.type)
                    counter += 1
                    break

        return counter

    def countLineCodeExec(self, tokens):
        counter = 0
        for j in tokens:
            for i in j:
                if i.channel == 0:
                    if i.type in [64, 67, 63, 62, 61, 68]:
                        pass
                    else:
                        counter += 1
                        break
        return counter


def get_line_of_codes(ent_model=None):
    return LineOfCode(ent_model)
