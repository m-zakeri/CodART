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
        self.exc=False
        self.NFE=False #throwwrongValueFormatException
        self.AE=False #throwArthimeticalException
        self.SIOB=False #throwStringIndextOutOfBound
        self.NP=False #throwNullPointer
        self.denominator="num2"
        self.string=''
        self.upbound=0
        self.parser=''
        self.stringnull=''
        with open(filename, 'r') as file:
            self.lines = file.readlines()
            file.close()
        self.linesCatch=[]
        self.linesTry=[]
        self.linesT=[]


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
        new_code = '' \
                   '\tBoolean flag = false;\n'
        new_code+=f"\t\tif ({inp}.matches("+"\"[-+]?[0-9]*\""+")) {\n"
        new_code+="\t\t\tflag = true;\n"
        new_code+="\t\t}"
        return new_code

    def isFloat(self,inp: str):
        new_code = '' \
                   '\tBoolean flag = false;\n'
        new_code+=f"\t\tif ({inp}.matches("+"\"[-+]?[0-9]*\\.?[0-9]+\""+")) {\n"
        new_code+="\t\t\tflag = true;\n"
        new_code+="\t\t}"
        return new_code



    def isDouble(self,inp: str):
        new_code = '' \
                   '\tBoolean flag = false;\n'
        new_code+=f"\t\tif ({inp}.matches("+"\"[-+]?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?[fF]\""+")) {\n"
        new_code+="\t\t\tflag = true;\n"
        new_code+="\t\t}"
        return new_code






    def exitStatement6(self, ctx: JavaParserLabeled.Statement6Context):
        if not self.exc:
            return
        # for i in range(0, ctx.block().blockStatement().__len__() - 1):
        #     startclasOrInterfaceType = ctx.block().blockStatement(i).children[0].children[0].children[0].start.tokenIndex
        #     classOrInterfaceType = ctx.block().blockStatement(i).children[0].children[0].children[0].getText()
        #     if classOrInterfaceType.__contains__('.'):
        #         continue
        #     else:
        #         start=startclasOrInterfaceType
        #         stop=startclasOrInterfaceType-classOrInterfaceType.__len__()
        #         text=ctx.getText()[4:10]
        #         # self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
        #         #                                    from_idx=ctx.start.tokenIndex,
        #         #                                    to_idx=ctx.stop.tokenIndex,
        #         #                                    text=ctx.getText() + ' ')
        #         print(text,startclasOrInterfaceType,classOrInterfaceType)


        # TODO ctx.finally...
        if (self.IOOBE and len(ctx.catchClause()) == 1 and ctx.finallyBlock() is None):
            self.name = ctx.children[1].children[1].children[0].children[1].children[0].children[2].getText()
            self.index = ctx.children[1].children[1].children[0].children[1].children[2].children[2].getText()
            tryExp=ctx.block().getText()
            self.returnedValue0=tryExp
            new_code = ''
            new_code += f' if ({self.index} >= {self.name}.length)'+self.returnedValue
            new_code+=f'else' + self.returnedValue0
            new_code = new_code.replace('{int', ';int ')
            new_code = new_code.replace(';String', ';String ')
            new_code = new_code.replace('{String', ';String ')
            new_code = new_code.replace(';char', ';char ')
            new_code = new_code.replace(';return', ';return ')
            new_code = new_code.replace('{return', ';return ')
            new_code = new_code.replace('e)', ' e) ')
            new_code = new_code.replace(';', ';\n')
            print(new_code)
            self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                               from_idx=ctx.start.tokenIndex,
                                               to_idx=ctx.stop.tokenIndex,
                                               text=new_code)
        elif (self.NFE and len(ctx.catchClause()) == 1 and ctx.finallyBlock() is None):
            flag=True
            new_code=''
            tryExp=ctx.block().getText()
            self.returnedValue0=tryExp
            self.parser=ctx.block().blockStatement(0).localVariableDeclaration().variableDeclarators().variableDeclarator(0
                ).variableInitializer().expression().methodCall().IDENTIFIER().getText()
            self.index=(ctx.block().blockStatement(0).localVariableDeclaration().variableDeclarators().variableDeclarator(0
                ).variableInitializer().expression().methodCall().expressionList().expression(0).primary().literal().getText())
            print(self.parser)
            start = tryExp.find('(')+1
            stop = tryExp.find(';')-1
            self.index = tryExp[start:stop]
            if(self.parser=='parseInt'):
                new_code+=self.isInt(self.index)
            elif(self.parser=='parseFloat'):
                new_code+=self.isFloat(self.index)
            elif(self.parser=='parseDouble'):
                new_code+=self.isDouble(self.index)
            else:
                flag=False
            if flag==True:
                new_code += f' if (flag==false)' + self.returnedValue
                new_code += f'else' + self.returnedValue0
                new_code = new_code.replace('{int', ';int ')
                new_code = new_code.replace(';String', ';String ')
                new_code = new_code.replace('{String', ';String ')
                new_code = new_code.replace(';char', ';char ')
                new_code = new_code.replace(';return', ';return ')
                new_code = new_code.replace('{return', ';return ')
                new_code = new_code.replace('e)', ' e) ')
                new_code = new_code.replace(';', ';\n')
                self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                                   from_idx=ctx.start.tokenIndex,
                                                   to_idx=ctx.stop.tokenIndex,
                                                   text=new_code)
            else:
                print(new_code)
        elif (self.AE and len(ctx.catchClause()) == 1 and ctx.finallyBlock() is None):

            new_code=''
            tryExp=ctx.block().getText()
            self.returnedValue0=tryExp
            new_code = ''
            new_code += f' if ({self.denominator}==0)' + self.returnedValue
            new_code += f'else' + self.returnedValue0
            new_code = new_code.replace('{int', ';int ')
            new_code = new_code.replace(';String', ';String ')
            new_code = new_code.replace('{String', ';String ')
            new_code = new_code.replace(';char', ';char ')
            new_code = new_code.replace(';return', ';return ')
            new_code = new_code.replace('{return', ';return ')
            new_code = new_code.replace('e)', ' e) ')
            new_code = new_code.replace(';', ';\n')
            self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                               from_idx=ctx.start.tokenIndex,
                                               to_idx=ctx.stop.tokenIndex,
                                               text=new_code)
        elif (self.SIOB and len(ctx.catchClause()) == 1 and ctx.finallyBlock() is None):

            catchline=ctx.catchClause(0).CATCH().symbol.line-1
            tryline = ctx.TRY().symbol.line-1
            lbraceline = ctx.block().children[0].symbol.line-1
            rbraceline = ctx.block().children[-1].symbol.line+1
            if(tryline==lbraceline):
                self.lines[lbraceline] = self.lines[rbraceline].replace('{', '{\n')
            if(self.lines[rbraceline].__contains__('catch')):
                self.lines[rbraceline]=self.lines[rbraceline].replace('}','}\n')

            definingString1=''
            definingString=''

            for i in range(0,ctx.block().blockStatement().__len__()-1):
                if(ctx.block().blockStatement(i).getText().__contains__(f'charAt({self.upbound})')):
                    continue
                else:
                    definingString1+= ctx.block().blockStatement(i).getText()


            new_code=''
            tryExp=ctx.block().getText()
            self.returnedValue0=tryExp.replace(definingString,'')
            new_code = ''
            new_code += definingString
            new_code += f' if ({self.string}.length()<={self.upbound})' + self.returnedValue
            new_code += f'else' + self.returnedValue0
            new_code = new_code.replace('{int', ';int ')
            new_code = new_code.replace(';String', ';String ')
            new_code = new_code.replace('{String', ';String ')
            new_code = new_code.replace(';char', ';char ')
            new_code = new_code.replace(';return', ';return ')
            new_code = new_code.replace('{return', ';return ')
            new_code = new_code.replace('e)', ' e) ')
            new_code = new_code.replace(';', ';\n')
            self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                               from_idx=ctx.start.tokenIndex,
                                               to_idx=ctx.stop.tokenIndex,
                                               text=new_code)
        elif (self.NP and len(ctx.catchClause()) == 1 and ctx.finallyBlock() is None):
            definingString=''
            for i in range(0,ctx.block().blockStatement().__len__()-1):
                if(ctx.block().blockStatement(i).getText().__contains__(f'{self.stringnull}.')):
                    continue
                else:
                    definingString+= ctx.block().blockStatement(i).getText()

            new_code=''
            tryExp=ctx.block().getText()
            self.returnedValue0=tryExp.replace(definingString,'')
            print(self.returnedValue0)
            new_code = ''
            new_code += definingString
            new_code += f' if ({self.stringnull}==null)' + self.returnedValue
            new_code += f'else' + self.returnedValue0
            new_code = new_code.replace('{int', ';int ')
            new_code = new_code.replace(';String', ';String ')
            new_code = new_code.replace('{String', 'String  ')

            new_code = new_code.replace(';char', ';char ')
            new_code = new_code.replace(';return', ';return ')
            new_code = new_code.replace('{return', ';return ')
            new_code = new_code.replace('e)', ' e) ')
            new_code = new_code.replace(';', ';\n')
            print(new_code)
            self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                               from_idx=ctx.start.tokenIndex,
                                               to_idx=ctx.stop.tokenIndex,
                                               text=new_code)


        file = open(self.filename, 'w')
        file.writelines(self.lines)
        file.close()

    # def enterPrimitiveType(self, ctx:JavaParserLabeled.PrimitiveTypeContext):
    #     self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
    #                                        from_idx=ctx.start.tokenIndex,
    #                                        to_idx=ctx.stop.tokenIndex,
    #                                        text=ctx.getText()+' ')

    # def enterClassOrInterfaceType(self, ctx:JavaParserLabeled.ClassOrInterfaceTypeContext):
        # self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
        #                                    from_idx=ctx.start.tokenIndex,
        #                                    to_idx=ctx.stop.tokenIndex,
        #                                    text=ctx.getText()+' ')

    def exitExpression2(self, ctx: JavaParserLabeled.Expression2Context):
        self.name = ctx.expression(0).primary().IDENTIFIER().getText()
        self.index = ctx.expression(1).primary().IDENTIFIER().getText()
        print("self.name")


    def enterCatchClause(self, ctx:JavaParserLabeled.CatchClauseContext):
        print(ctx.catchType().getText())
        if ctx.catchType().getText()=='ArrayIndexOutOfBoundsException':
            self.exc=True
            self.NP=False
            self.IOOBE=True
            self.NFE=False
            self.SIOB=False
            self.AE=False
            self.returnedValue = ctx.block().getText()

        elif ctx.getText().__contains__('NumberFormatException'):
            self.exc=True
            self.NP=False
            self.IOOBE=False
            self.NFE=True
            self.SIOB=False
            self.AE=False
            self.returnedValue = ctx.block().getText()

        elif ctx.getText().__contains__('ArithmeticException'):
            self.exc=True
            self.NP=False
            self.IOOBE=False
            self.NFE=False
            self.SIOB=False
            self.AE=True
            self.returnedValue=ctx.block().getText()

        elif ctx.getText().__contains__('StringIndexOutOfBound'):
            self.exc=True
            self.SIOB=True
            self.NP=False
            self.IOOBE=False
            self.NFE=False
            self.AE=False
            self.returnedValue=ctx.block().getText()
            # # print(ctx.block().children[1].getText())
            # definingString=''
            # # for j in range(0,ctx.block().blockStatement().__len__()):
            # #     for i in range(0, ctx.block().blockStatement(j).children.__len__()):
            # #         defe+=ctx.block().blockStatement(j).children[i].getText()
            # #         defe+=' '
            # #     defe+='\n'
            # # print(defe)
            #
            # for i in range(0,ctx.block().blockStatement().__len__()):
            #     counter=0
            #     clasOrInterfaceType = ctx.block().blockStatement(i).children[0].children[0].children[0].getText()
            #     part = ctx.block().blockStatement(i).children[0].children[1].getText()
            #     if clasOrInterfaceType.__contains__('.'):
            #         definingString += '\t\t' + ctx.block().blockStatement(i).getText()
            #         # definingString += '\n'
            #     else:
            #         clasOrInterfaceType += ' '
            #         definingString += '\t\t' + clasOrInterfaceType + part
            #         # definingString += '\n'
            #         counter+1
            #     print(counter)
            #     # self.returnedValue+=definingString
            # # print(self.returnedValue)





        elif ctx.getText().__contains__('NullPointer'):
            self.exc=True
            self.NP=True
            self.IOOBE=False
            self.NFE=False
            self.SIOB=False
            self.AE=False
            self.returnedValue=ctx.block().getText()

    def enterExpression9(self, ctx:JavaParserLabeled.Expression9Context):
        if not self.exc:
            return
        if ctx.getText().__contains__('/'):
            dv=ctx.getText().split('/')
            self.denominator=dv[1]

    def enterBlockStatement0(self, ctx:JavaParserLabeled.BlockStatement0Context):
        if not self.exc:
            return
        if ctx.getText().__contains__('.parse'):
            self.parser= ctx.localVariableDeclaration().variableDeclarators().variableDeclarator(0
                ).variableInitializer().expression().methodCall().IDENTIFIER().getText()
        if ctx.getText().__contains__('.charAt'):
            self.string= ctx.localVariableDeclaration().variableDeclarators().variableDeclarator(
                0).variableInitializer().expression().getText().split('.')[0]
        if ctx.getText().__contains__('null'):
            self.stringnull=ctx.localVariableDeclaration().variableDeclarators().variableDeclarator(0
            ).variableDeclaratorId().IDENTIFIER().getText()


    def enterExpression21(self, ctx:JavaParserLabeled.Expression21Context):
        if not self.exc or not self.SIOB:
            return
        else:
            self.upbound=ctx.expression(1).methodCall().expressionList().expression(0).primary().literal().integerLiteral().getText()


    def exitCompilationUnit(self, ctx:JavaParserLabeled.CompilationUnitContext):
        if not self.exc:
            print("doesn't have any exceptions")
            return





directory = "C:\\Users\\asus\\Desktop\\TestProject"


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