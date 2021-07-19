import os
import os
import errno
import argparse
from gen.javaLabeled.JavaLexer import JavaLexer

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class MakeFieldNonStaticRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class=None, field_name: str = None , have_Non_Parameter_cunstrutor_flag=None):

        if have_Non_Parameter_cunstrutor_flag is None:
            self.have_Non_Parameter_cunstrutor_flag=False
        else:
            self.have_Non_Parameter_cunstrutor_flag=have_Non_Parameter_cunstrutor_flag

        if field_name is None:
            self.field_name = ""
        else:
            self.field_name = field_name

        if source_class is None:
            self.source_class = ""
        else:
            self.source_class = source_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_source_class = False
        self.is_static = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):

        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = True



        else:
            self.is_source_class = False
    def enterClassBody(self, ctx:JavaParserLabeled.ClassBodyContext):
        if not self.is_source_class:
            return None
        temtext="\n\tpublic "+self.source_class+"() {}\n"
        if self.have_Non_Parameter_cunstrutor_flag is False:
            self.token_stream_rewriter.replaceRange(
                from_idx=ctx.start.tokenIndex + 1,
                to_idx=ctx.start.tokenIndex + 1,
                text=temtext
            )
    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if not self.is_source_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        # field_identifier = ctx.variableDeclarators().getText().split(",")
        field_identifier = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText()
        if self.field_name in field_identifier:
            if not (grand_parent_ctx.modifier() == []):
                for i in range(0, len(grand_parent_ctx.modifier())):
                    if grand_parent_ctx.modifier(i).getText() == "static":
                        self.is_static = True
                        break
                if self.is_static:
                    self.token_stream_rewriter.replaceRange(
                        from_idx=grand_parent_ctx.modifier(i).start.tokenIndex,
                        to_idx=grand_parent_ctx.modifier(i).stop.tokenIndex,
                        text=''
                    )
class PropagationMakeFieldNonStaticRefactoringListener(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, using_field_name= None,
                 propagated_class_name=None,mainclass=None):

        if using_field_name is None:
            self.using_field_name = []
        else:
            self.using_field_name = using_field_name
        #
        if mainclass is None:
            self.mainclass = []
        else:
            self.mainclass = mainclass

        if propagated_class_name is None:
            self.propagated_class_name = []
        else:
            self.propagated_class_name = propagated_class_name

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_class = False
    def enterClassBody(self, ctx:JavaParserLabeled.ClassBodyContext):
        if(self.is_class == True):
            text="\n"+self.mainclass+" "+self.mainclass+"obj = new "+self.mainclass+"();\n"
            self.token_stream_rewriter.replaceRange(
            from_idx=ctx.start.tokenIndex+1,
            to_idx=ctx.start.tokenIndex+1,
            text=text)
    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if (class_identifier in self.propagated_class_name):
            self.is_class = True
            print("Propagation started, please wait...")
        else:
            self.is_class = False
    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        if (self.is_class == True):
            self.is_class=False


    def enterExpression1(self, ctx:JavaParserLabeled.Expression1Context):

        if not self.is_class:
            return
        # print("ctx.expression()",ctx.expression())
        if ctx.expression()!=None:
            # print("ctx.expression().primary()",ctx.expression().primary())
            if ctx.expression().primary() != None:
                # print("ctx.expression().primary().IDENTIFIER().getText()",ctx.expression().primary().IDENTIFIER().getText())
                # print(ctx.DOT())
                # print(ctx.IDENTIFIER().getText())
                if ctx.expression().primary().IDENTIFIER().getText() == self.mainclass\
                        and ctx.DOT().getText()=="." and ctx.IDENTIFIER().getText()==self.using_field_name:
                    # print("111111111111111111111111111111111")
                    text = self.mainclass + "obj"
                    # print("enterClassBodyDeclaration2")
                    self.token_stream_rewriter.replaceRange(
                        from_idx=ctx.start.tokenIndex ,
                        to_idx=ctx.start.tokenIndex ,
                        text=text)


def main(udb_path, source_class, field_name):
    print("Make Field Non Static")
    main_file = None
    db = und.open(udb_path)
    have_Non_Parameter_cunstrutor_flag=False
    for cls in db.ents("class"):
        if cls.simplename() == source_class:
            main_file = cls.parent().longname(True)
            # print(main_file)
            #
            # print("counstructor {{{")
            for mth in cls.ents('Define', 'Java Method Constructor'):
                print("mth=",mth)
                print("parameters:", mth.parameters())
                if(str(mth.parameters()) ==""):
                    print("is nonnnnnnnnnnnnnnnnnnnnnnn")
                    have_Non_Parameter_cunstrutor_flag=True

            if (len(cls.ents('Define', 'Java Method Constructor')) == 0):
                have_Non_Parameter_cunstrutor_flag = True
            # print("counstructor }}}}")
            #
            if not os.path.isfile(main_file):
                continue



    if main_file is None:
        return

    stream = FileStream(main_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = MakeFieldNonStaticRefactoringListener(common_token_stream=token_stream, source_class=source_class,
                                                        field_name=field_name,
                                                        have_Non_Parameter_cunstrutor_flag=have_Non_Parameter_cunstrutor_flag)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    # print(my_listener.token_stream_rewriter.getDefaultText())

    with open(main_file, mode='w',encoding="utf-8", newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////
    # propagation
    file_list_to_be_propagate = set()
    propagate_classes = set()
    for fld in db.ents("variable"):
        if fld.simplename() == field_name:
            # print(fld.longname())
            # print("refs",fld.refs())

            for ref in fld.refs("Definein"):
                # print(ref.ent().simplename())
                if (ref.ent().simplename()==source_class):
                    # print(fld.refs())
                    for ref in fld.refs("Setby , Useby"):
                        if not (str(ref.ent()) == str(fld.parent())
                                or str(ref.ent().parent()) == str(fld.parent())):
                            propagate_classes.add(str(ref.ent().parent().simplename()))
                            # file_list_to_be_propagate.add( ref.file().relname())
                            file_list_to_be_propagate.add( ref.file().longname(True))
                            # print(propagate_classes)
                            # print(file_list_to_be_propagate)

    for file in file_list_to_be_propagate:
        # print(file)
        argparser = argparse.ArgumentParser()
        argparser.add_argument('-n', '--file', help='Input source', default= file)
        args = argparser.parse_args()
        stream = FileStream(main_file, encoding='utf8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        my_listener = PropagationMakeFieldNonStaticRefactoringListener(common_token_stream=token_stream,
                                                                            using_field_name=field_name,
                                                                            propagated_class_name=propagate_classes,mainclass=source_class)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)
        # print(my_listener.token_stream_rewriter.getDefaultText())

        with open(main_file, mode='w', encoding="utf-8", newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    # udb_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    udb_path = "D:\CodART\\benchmark_projects\\testerproject.udb"
    source_class = "mainclass"
    field_name = "staticfield"

    # initialize with understand
    main(udb_path, source_class, field_name)
