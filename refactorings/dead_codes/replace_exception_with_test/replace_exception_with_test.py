import os
import time
import argparse

from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from antlr4.TokenStreamRewriter import TokenStreamRewriter as TSR

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class ReplaceExceptionWithPrecheckListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream = None,
                 class_identifier: str = None, filename: str = None):
        self.IOOBE = False  # IndexOutOfBoundException
        # self.ASE = False # ArrayStoreException
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        self.dictionary = {}
        self.returnedValue=''
        self.currentLine=1
        self.lastLine=0
        self.returnedValue0=''
        self.name=''
        self.index=''
        self.NFE=False #throwwrongValueFormatException
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

    def isInt(self,inp: str):
        new_code='\rBoolean flag = true\n'
        new_code+=f"\tfor (int a=0 ;a < {inp}.length() ;a++)"
        new_code+="\t{"
        new_code+=f"\t\tif (a == 0 & & {inp}.charAt(a) == '-')\n"
        new_code+="\t\t\tcontinue;"
        new_code+=f"\t\tif (!Character.isDigit({inp}.charAt(a)))\n" \
                                                    "\t\t\tflag = false;" \
                                                    "}"
        return new_code

    def isFloat(self,inp: str):
        new_code = '' \
                   '\tBoolean flag = true\n'
        new_code+=f"\t\tif ({inp}.matches("+"\"[-+]?[0-9]*\\.?[0-9]+\""+")) {\n"
        new_code+="\t\t\tflag = true\n;"
        new_code+="\t\t}"
        return new_code



    def isDouble(self,inp: str):
        new_code = '' \
                   '\tBoolean flag = true\n'
        new_code+=f"\t\tif ({inp}.matches("+"\"[-+]?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?[fF]\""+")) {\n"
        new_code+="\t\t\tflag = true\n;"
        new_code+="\t\t}"
        return new_code






    def exitStatement6(self, ctx: JavaParserLabeled.Statement6Context):
        # TODO ctx.finally...
        if (self.IOOBE and len(ctx.catchClause()) == 1 and ctx.finallyBlock() is None):
            tryExp=ctx.block().getText()
            self.returnedValue0=tryExp
            if (tryExp.__contains__('this.')):
                start = tryExp.find('this.') +5
                stop  = tryExp.find('.get')
                self.name=tryExp[start:stop]
                start = tryExp.find('.get(') +5
                stop  = tryExp.find(')')
                self.index=tryExp[start:stop]

            ctx.TRY().getText()
            tryline = ctx.TRY().symbol.line-1
            self.lines[tryline] = self.lines[tryline].replace('try', '')

            lbraceline = ctx.block().children[0].symbol.line - 1
            self.lines[lbraceline] = self.lines[lbraceline].replace('{', '')

            rbraceline = ctx.block().children[-1].symbol.line - 1
            head, _sep, tail = self.lines[rbraceline].rpartition('}')
            self.lines[rbraceline] = self.lines[rbraceline] = head + '' + tail
            new_code = ''
            new_code += f' if ({self.index} >= {self.name}.length)'+self.returnedValue
            new_code+=f'else' + self.returnedValue0
            new_code = new_code.replace('{','{\n')
            new_code = new_code.replace('}','}\n')
            new_code = new_code.replace(';',';\n')
            new_code = new_code.replace('return','return ')
            self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                               from_idx=ctx.start.tokenIndex,
                                               to_idx=ctx.stop.tokenIndex,
                                               text=new_code)
        if (self.NFE and len(ctx.catchClause()) == 1 and ctx.finallyBlock() is None):
            new_code=''
            tryExp=ctx.block().getText()
            self.returnedValue0=tryExp
            start = tryExp.find('.parse') + 6
            stop = tryExp.find('(')
            self.name = tryExp[start:stop]
            start = tryExp.find('(')+1
            stop = tryExp.find(';')-1
            self.index = tryExp[start:stop]
            if(self.name=='Int'):
                new_code+=self.isInt(self.index)
            if(self.name=='Float'):
                new_code+=self.isFloat(self.index)
            if(self.name=='Double'):
                new_code+=self.isDouble(self.index)
            new_code += f' if (flag==false)' + self.returnedValue
            new_code += f'else' + self.returnedValue0
            new_code = new_code.replace('{', '{\n')
            new_code = new_code.replace('}', '}\n')
            # new_code = new_code.replace(';', ';\n')
            new_code = new_code.replace('return', 'return ')
            print(new_code)
            self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                               from_idx=ctx.start.tokenIndex,
                                               to_idx=ctx.stop.tokenIndex,
                                               text=new_code)


        file = open(self.filename, 'w')
        file.writelines(self.lines)
        file.close()

    def exitExpression2(self, ctx: JavaParserLabeled.Expression2Context):
        start = ctx.start.tokenIndex
        stop = ctx.stop.tokenIndex

        # self.returnedValue0=ctx.getText()+";"
        self.name = ctx.expression(0).getText()
        self.index = ctx.expression(1).getText()
        currentline = ctx.start.line-1
        array = self.token_stream.getText(start, stop)
        idx = self.lines[currentline].find(f'{array}')
        before = self.lines[currentline][:idx]
        after = self.lines[currentline][idx + len(f'{array}'):]
       # self.lines[currentline]=f"if ({self.index} >= {self.name}.length) {{\n "

    def enterCatchClause(self, ctx:JavaParserLabeled.CatchClauseContext):
        print(ctx.catchType().getText())
        if ctx.catchType().getText()=='ArrayIndexOutOfBoundsException':
            self.IOOBE = True
            self.returnedValue = ctx.block().getText()

        elif ctx.getText().__contains__('NumberFormatException'):
            self.NFE=True
            self.returnedValue = ctx.block().getText()



    def enterMethodBody(self, ctx:JavaParserLabeled.MethodBodyContext):
        if not self.IOOBE:
            return

    def exitMethodBody(self, ctx:JavaParserLabeled.MethodBodyContext):
        if not self.IOOBE:
            return






directory = "C:\\Users\\asus\\Desktop\\TestProject2"


def main(args):
    # Step 1: Load input source into stream
    stream = FileStream(args.file, encoding='utf8')
    # input_stream = StdinStream()

    # Step 2: Create an instance of AssignmentStLexer
    lexer = JavaLexer(stream)
    # Step 3: Convert the input source into a list of tokens
    token_stream = CommonTokenStream(lexer)
    # Step 4: Create an instance of the AssignmentStParser
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()

    # Step 5: Create parse tree
    parse_tree = parser.compilationUnit()


    # Step 6: Create an instance of AssignmentStListener
    my_listener = ReplaceExceptionWithPrecheckListener(common_token_stream=token_stream, class_identifier='GodClass',
                                                 filename=args.file)

    # return
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(args.file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())


def process_file(file):
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=file)
    args = argparser.parse_args()
    main(args)


if __name__ == '__main__':
    for dirname, dirs, files in os.walk(directory):
        for file in files:
            name, extension = os.path.splitext(file)
            if extension == '.java':
                print(dirname)
                print(name)
                process_file("{}/{}".format(dirname, file))