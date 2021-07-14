import os
import time
import argparse

from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from antlr4.TokenStreamRewriter import TokenStreamRewriter as TSR

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class RemoveFieldRefactoringListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream = None, class_identifier: str = None,
                 fieldname: str = None, filename: str = None):
        """
        :param common_token_stream:
        """
        self.enter_class = False
        self.enter_field = False
        self.is_found_field = False
        self.is_static = False
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        self.class_number = 0
        self.type_field=None
        self.modifier_field=''
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TSR(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

        self.class_fields = []
        self.class_methods = []

        if class_identifier is not None:
            self.class_identifier = class_identifier
        else:
            raise ValueError("class_identifier is None")

        if filename is not None:
            self.filename = filename
        else:
            raise ValueError("filename is None")

        if fieldname is not None:
            self.fieldname = fieldname
        else:
            raise ValueError("fieldname is None")

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.class_number += 1
        if ctx.IDENTIFIER().getText() != self.class_identifier:
            return
        self.enter_class = True


    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.enter_class = False
        if ctx.IDENTIFIER().getText() != self.class_identifier:
            return

        old_file = open(self.filename, 'w')
        old_file.write(self.token_stream_rewriter.getDefaultText().replace("\r", ""))



    def enterFieldDeclaration(self, ctx:JavaParserLabeled.FieldDeclarationContext):
        if not self.enter_class:
            return
        self.enter_field = True
        self.is_found_field = False



    def exitClassBodyDeclaration2(self, ctx:JavaParserLabeled.ClassBodyDeclaration2Context):
        if not self.enter_class:
            return
        start=ctx.modifier(0).start.tokenIndex
        stop=ctx.modifier(0).stop.tokenIndex
        identifier=ctx.memberDeclaration().fieldDeclaration().variableDeclarators().variableDeclarator(0
                                    ).variableDeclaratorId().IDENTIFIER().getText()

        returnedV='this'
        if ctx.modifier(1) != None:
            self.modifier_field=' '+ctx.modifier(1).getText()
        self.type_field=ctx.memberDeclaration().fieldDeclaration().typeType().primitiveType().getText()
        if identifier==self.fieldname:
            self.is_found_field=True
            if ctx.modifier(1)!=None:
                self.is_static=True
                returnedV=self.class_identifier
            new_code=''
            new_code += '\n\tpublic' + self.modifier_field +" "+ self.type_field+ ' get' + str.capitalize(self.fieldname)
            new_code += '() { \n\t\t return ' + self.fieldname + ';' + '\n\t}'
            new_code += '\n\t'
            new_code += 'public'+self.modifier_field +' void set' + str.capitalize(self.fieldname)
            new_code += '(' + self.type_field + ' ' + self.fieldname + ') { \n\t\t'
            new_code += returnedV+'.' + self.fieldname + ' = ' + self.fieldname + ';' + '\n\t}\n'
            print(new_code)

            if not ctx.getText().__contains__('publicvoidset'+str.capitalize(self.fieldname)):
                self.token_stream_rewriter.insertAfter(ctx.stop.tokenIndex, new_code)

            self.token_stream_rewriter.replace(program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                               from_idx=start,
                                               to_idx=stop,
                                               text='private')



    def exitVariableDeclarators(self, ctx:JavaParserLabeled.VariableDeclaratorsContext):
        if not (self.enter_class and self.enter_field):
            return



    def exitCompilationUnit(self, ctx:JavaParserLabeled.CompilationUnitContext):
        if not self.is_found_field:
            print(f'Field "{self.fieldname}" NOT FOUND...')




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

    print("=====Enter Create ParseTree=====")
    # Step 5: Create parse tree
    parse_tree = parser.compilationUnit()
    print("=====Create ParseTree Finished=====")

    # Step 6: Create an instance of AssignmentStListener
    my_listener = RemoveFieldRefactoringListener(common_token_stream=token_stream, class_identifier='GodClass',
                                                 fieldname='number3', filename=args.file)

    # return
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(args.file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())


def process_file(file):
    argparser = argparse.ArgumentParser()
    # argparser.add_argument(
    #     '-n', '--file',
    #     help='Input source', default=r'refactorings/test/test1.java')
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
                process_file("{}/{}".format(dirname, file))