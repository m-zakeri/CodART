from antlr4.TokenStreamRewriter import TokenStreamRewriter as TSR

from gen.javaLabeled.JavaParserLabeled import *
from gen.javaLabeled.JavaParserLabeledListener import *


class ReplaceExceptionWithTestClassRefactoringListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream = None,
                 class_identifier: str = None, filename: str = None):
        self.IOOBE = False  # IndexOutOfBoundException
        # self.ASE = False # ArrayStoreException
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        self.dictionary = {}
        with open(filename, 'r') as file:
            self.lines = file.readlines()
            file.close()

        if common_token_stream is not None:
            self.token_stream_rewriter = TSR(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

        if class_identifier is not None:
            self.class_identifier = class_identifier
        else:
            raise ValueError("class_identifier is None")

        if filename is not None:
            self.filename = filename
        else:
            raise ValueError("filename is None")

    def enterStatement6(self, ctx: JavaParserLabeled.Statement6Context):
        print("'enterStatement6'")

    # def enterTryStatement1(self, ctx:Java9_v2Parser.TryStatement1Context):
    #     print("'enterTryStatement1'")
    #     pass

    def exitStatement6(self, ctx: JavaParserLabeled.Statement6Context):
        # TODO ctx.finally...
        if (self.IOOBE and len(ctx.catchClause()) == 1 and ctx.finallyBlock() is None):
            ctx.TRY().getText()
            tryline = ctx.TRY().symbol.line - 1
            self.lines[tryline] = self.lines[tryline].replace('try', '')

            lbraceline = ctx.block().children[0].symbol.line - 1
            self.lines[lbraceline] = self.lines[lbraceline].replace('{', '')

            rbraceline = ctx.block().children[-1].symbol.line - 1
            head, _sep, tail = self.lines[rbraceline].rpartition('}')
            self.lines[rbraceline] = self.lines[rbraceline] = head + '' + tail

        file = open(self.filename, 'w')
        file.writelines(self.lines)
        file.close()
        print("'exitTryStatement1'")

    # def exitTryStatement1(self, ctx:Java9_v2Parser.TryStatement1Context):
    #     # TODO Replace Exceptions With Test(ReWrite file with self.lines)
    #     if self.IOOBE and len(ctx.catches().children) == 1:
    #         ctx.TRY().getText()
    #         tryline = ctx.TRY().symbol.line - 1
    #         self.lines[tryline] = self.lines[tryline].replace('try', '')
    #
    #         lbraceline = ctx.block().children[0].symbol.line - 1
    #         self.lines[lbraceline] = self.lines[lbraceline].replace('{', '')
    #
    #         rbraceline = ctx.block().children[2].symbol.line - 1
    #         head, _sep, tail = self.lines[rbraceline].rpartition('}')
    #         self.lines[rbraceline] = self.lines[rbraceline] = head + '' + tail
    #
    #     file = open('refactorings/test/test3.java', 'w')
    #     file.writelines(self.lines)
    #     file.close()
    #     print("'exitTryStatement1'")

    # def enterTryStatement2(self, ctx:Java9_v2Parser.TryStatement2Context):
    #     print("'enterTryStatement2'")
    #     pass

    # def exitTryStatement2(self, ctx:Java9_v2Parser.TryStatement2Context):
    #     # TODO Replace Exceptions With Test(ReWrite file with self.lines)
    #     file = open('refactorings/test/test3.java', 'w')
    #     file.writelines(self.lines)
    #     file.close()
    #
    #     print("'exitTryStatement2'")

    # def enterTryStatement3(self, ctx:Java9_v2Parser.TryStatement3Context):
    #     print("'enterTryStatement3'")
    #     pass
    #
    # def exitTryStatement3(self, ctx:Java9_v2Parser.TryStatement3Context):
    #     print("'exitTryStatement3'")
    #     pass

    # ====================================================================================================

    def enterExpression2(self, ctx: JavaParserLabeled.Expression2Context):
        print("'enterExpression2'")

    # def enterArrayAccess(self, ctx:Java9_v2Parser.ArrayAccessContext):
    #     print("'enterArrayAccess'")

    def exitExpression2(self, ctx: JavaParserLabeled.Expression2Context):
        start = ctx.start.tokenIndex
        stop = ctx.stop.tokenIndex

        print(f"ArrayName: {ctx.expression(0).getText()}; ArrayIndex: {ctx.expression(1).getText()};")
        name = ctx.expression(0).getText()
        index = ctx.expression(1).getText()
        # TODO Find Prev. & Next ';' Of Current Line
        currentline = ctx.start.line - 1

        array = self.token_stream.getText(start, stop)
        idx = self.lines[currentline].find(f'{array}')
        before = self.lines[currentline][:idx]
        after = self.lines[currentline][idx + len(f'{array}'):]

        prevsc = before.rfind(';')  # Previous ';' Index
        if prevsc != -1:
            before = f"{before[:prevsc + 1]}\nif ({index} < {name}.length) {{\n\t {before[prevsc + 1:]}"

        nextsc = after.find(';')  # Next ';' Index
        if nextsc != -1:
            after = f"{after[:nextsc + 1]} }}\n{after[nextsc + 1:]}"
            self.dictionary[currentline] = len(before) + len(array) + nextsc + 4  # '; }\n' = 4 Characters

        self.lines[currentline] = f"{before}{array}{after}"

        offset = 1
        while nextsc == -1:
            nextsc = self.lines[currentline + offset].find(';')
            if nextsc == -1:
                self.lines[currentline + offset] = "\t" + self.lines[currentline + offset]
            else:
                self.lines[currentline + offset] = f"\t{self.lines[currentline + offset][:nextsc + 1]} }}\n" \
                                                   f"{self.lines[currentline + offset][nextsc + 1:]}"
                self.dictionary[currentline + offset] = nextsc + 4  # '; }\n' = 4 Characters
            offset += 1

        offset = 1
        while prevsc == -1:
            prevsc = self.lines[currentline - offset].rfind(';')
            if prevsc == -1:
                self.lines[currentline - offset] = "\t" + self.lines[currentline - offset]
            else:
                self.lines[currentline - offset] = f"{self.lines[currentline - offset][:prevsc + 1]}\n" \
                                                   f"if ({index} < {name}.length) {{\n" \
                                                   f"\t{self.lines[currentline - offset][prevsc + 1:]}"

            offset += 1

        print("'exitArrayAccess'")

    # def exitArrayAccess(self, ctx:Java9_v2Parser.ArrayAccessContext):
    #     # if not self.IOOBE:
    #     #     return
    #     start = ctx.start.tokenIndex
    #     stop = ctx.stop.tokenIndex
    #
    #     print(f"ArrayName: {ctx.expressionName().identifier().getText()}; ArrayIndex: {ctx.expression(0).getText()};")
    #     name = ctx.expressionName().identifier().getText()
    #     index = ctx.expression(0).getText()
    #     # TODO Find Prev. & Next ';' Of Current Line
    #     currentline = ctx.start.line - 1
    #
    #     array = self.token_stream.getText(start, stop)
    #     idx = self.lines[currentline].find(f'{array}')
    #     before = self.lines[currentline][:idx]
    #     after = self.lines[currentline][idx + len(f'{array}'):]
    #
    #     prevsc = before.rfind(';')  # Previous ';' Index
    #     if prevsc != -1:
    #         before = f"{before[:prevsc + 1]}\nif ({index} < {name}.length) {{\n\t {before[prevsc + 1:]}"
    #
    #     nextsc = after.find(';')  # Next ';' Index
    #     if nextsc != -1:
    #         after = f"{after[:nextsc + 1]} }}\n{after[nextsc + 1:]}"
    #         self.dictionary[currentline] = len(before) + len(array) + nextsc + 4  # '; }\n' = 4 Characters
    #
    #     self.lines[currentline] = f"{before}{array}{after}"
    #
    #     offset = 1
    #     while nextsc == -1:
    #         nextsc = self.lines[currentline + offset].find(';')
    #         if nextsc == -1:
    #             self.lines[currentline + offset] = "\t" + self.lines[currentline + offset]
    #         else:
    #             self.lines[currentline + offset] = f"\t{self.lines[currentline + offset][:nextsc + 1]} }}\n" \
    #                                                f"{self.lines[currentline + offset][nextsc + 1:]}"
    #             self.dictionary[currentline + offset] = nextsc + 4  # '; }\n' = 4 Characters
    #         offset += 1
    #
    #     offset = 1
    #     while prevsc == -1:
    #         prevsc = self.lines[currentline - offset].rfind(';')
    #         if prevsc == -1:
    #             self.lines[currentline - offset] = "\t" + self.lines[currentline - offset]
    #         else:
    #             self.lines[currentline - offset] = f"{self.lines[currentline - offset][:prevsc + 1]}\n" \
    #                                                f"if ({index} < {name}.length) {{\n" \
    #                                                f"\t{self.lines[currentline - offset][prevsc + 1:]}"
    #
    #         offset += 1
    #
    #     print("'exitArrayAccess'")

    # def enterArrayAccess_lfno_primary(self, ctx:Java9_v2Parser.ArrayAccess_lfno_primaryContext):
    #     print("'enterArrayAccess_lfno_primary'")
    #
    # def exitArrayAccess_lfno_primary(self, ctx:Java9_v2Parser.ArrayAccess_lfno_primaryContext):
    #     start = ctx.start.tokenIndex
    #     stop = ctx.stop.tokenIndex
    #
    #     print(f"ArrayName: {ctx.expressionName().identifier().getText()}; ArrayIndex: {ctx.expression(0).getText()};")
    #     name = ctx.expressionName().identifier().getText()
    #     index = ctx.expression(0).getText()
    #     # TODO Find Prev. & Next ';' Of Current Line
    #     currentline = ctx.start.line - 1
    #
    #     array = self.token_stream.getText(start, stop)
    #     idx = self.lines[currentline].find(f'{array}')
    #     before = self.lines[currentline][:idx]
    #     after = self.lines[currentline][idx + len(f'{array}'):]
    #
    #     prevsc = before.rfind(';') # Previous ';' Index
    #     if prevsc != -1:
    #         before = f"{before[:prevsc + 1]}\nif ({index} < {name}.length) {{\n\t {before[prevsc + 1:]}"
    #
    #     nextsc = after.find(';') # Next ';' Index
    #     if nextsc != -1:
    #         after = f"{after[:nextsc + 1]} }}\n{after[nextsc + 1:]}"
    #         self.dictionary[currentline] = len(before) + len(array) + nextsc + 4  # '; }\n' = 4 Characters
    #
    #     self.lines[currentline] = f"{before}{array}{after}"
    #
    #     offset = 1
    #     while nextsc == -1:
    #         nextsc = self.lines[currentline + offset].find(';')
    #         if nextsc == -1:
    #             self.lines[currentline + offset] = "\t" + self.lines[currentline + offset]
    #         else:
    #             self.lines[currentline + offset] = f"\t{self.lines[currentline + offset][:nextsc + 1]} }}\n" \
    #                                                f"{self.lines[currentline + offset][nextsc + 1:]}"
    #             self.dictionary[currentline + offset] = nextsc + 4 # '; }\n' = 4 Characters
    #         offset += 1
    #
    #     offset = 1
    #     while prevsc == -1:
    #         prevsc = self.lines[currentline - offset].rfind(';')
    #         if prevsc == -1:
    #             self.lines[currentline - offset] = "\t" + self.lines[currentline - offset]
    #         else:
    #             self.lines[currentline - offset] = f"{self.lines[currentline - offset][:prevsc + 1]}\n" \
    #                                                f"if ({index} < {name}.length) {{\n" \
    #                                                f"\t{self.lines[currentline - offset][prevsc + 1:]}"
    #
    #         offset += 1
    #
    #     print("'exitArrayAccess_lfno_primary'")

    def exitCatchClause(self, ctx: JavaParserLabeled.CatchClauseContext):
        exception = ctx.catchType().getText()
        if (exception == "IndexOutOfBoundsException"):
            self.IOOBE = True
            start = ctx.block().start.tokenIndex
            stop = ctx.block().stop.tokenIndex
            # self.token_stream_rewriter.delete(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            #                                   from_idx=start, to_idx=stop)
            print(f'Start: {ctx.start.line}, Stop: {ctx.stop.line}')
            catch_block = self.token_stream.getText(start=start, stop=stop)
            for key in self.dictionary:
                self.lines[key] = f"{self.lines[key][:self.dictionary[key]]} else {catch_block}\n" \
                                  f"{self.lines[key][self.dictionary[key]:]}"
            print('=' * 50)
            for line in range(ctx.start.line - 1, ctx.stop.line):
                del self.lines[ctx.start.line - 1]
            print('=' * 50)

            # # TODO Replace Exceptions With Test(ReWrite file with self.lines)
            # file = open('refactorings/test/test3.java', 'w')
            # file.writelines(self.lines)
            # file.close()

            # print("Dictionary: \n", self.dictionary)
            # print("Catch Clause: \n", self.token_stream.getText(start=start, stop=stop))

    # def exitCatchClause(self, ctx:Java9_v2Parser.CatchClauseContext):
    #     exception = ctx.catchFormalParameter().catchType().unannClassType().getText()
    #     if (exception == "IndexOutOfBoundsException"):
    #         self.IOOBE = True
    #         start = ctx.block().start.tokenIndex
    #         stop = ctx.block().stop.tokenIndex
    #         # self.token_stream_rewriter.delete(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
    #         #                                   from_idx=start, to_idx=stop)
    #         print(f'Start: {ctx.start.line}, Stop: {ctx.stop.line}')
    #         catch_block = self.token_stream.getText(start=start, stop=stop)
    #         for key in self.dictionary:
    #             self.lines[key] = f"{self.lines[key][:self.dictionary[key]]} else {catch_block}\n" \
    #                               f"{self.lines[key][self.dictionary[key]:]}"
    #         print('=' * 50)
    #         for line in range(ctx.start.line - 1, ctx.stop.line):
    #             del self.lines[ctx.start.line - 1]
    #         print('='*50)
    #
    #         # # TODO Replace Exceptions With Test(ReWrite file with self.lines)
    #         # file = open('refactorings/test/test3.java', 'w')
    #         # file.writelines(self.lines)
    #         # file.close()
    #
    #         print("Dictionary: \n", self.dictionary)
    #         print("Catch Clause: \n", self.token_stream.getText(start=start, stop=stop))

# ====================================================================================================
