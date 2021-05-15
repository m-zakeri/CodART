import os

from gen.javaLabeled.JavaLexer import JavaLexer

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class ExtractSubClassRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(
            self, common_token_stream: CommonTokenStream = None,
            source_class: str = None, new_class: str = None,
            moved_fields=None, moved_methods=None):

        if moved_methods is None:
            self.moved_methods = []
        else:
            self.moved_methods = moved_methods
        if moved_fields is None:
            self.moved_fields = []
        else:
            self.moved_fields = moved_fields

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if source_class is None:
            raise ValueError("source_class is None")
        else:
            self.source_class = source_class
        if new_class is None:
            raise ValueError("new_class is None")
        else:
            self.new_class = new_class

        self.is_source_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):

        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = True
            self.code += self.NEW_LINE * 2
            self.code += f"// New class({self.new_class}) generated by CodART" + self.NEW_LINE
            self.code += f"class {self.new_class} extends {self.source_class}{self.NEW_LINE}" + "{" + self.NEW_LINE
        else:
            self.is_source_class = False

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_source_class:
            self.code += "}"
            self.is_source_class = False

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):

        self.token_stream_rewriter.insertAfter(
            index=ctx.stop.tokenIndex,
            text=self.code
        )

    def enterVariableDeclaratorId(self, ctx: JavaParserLabeled.VariableDeclaratorIdContext):
        if not self.is_source_class:
            return None
        field_identifier = ctx.IDENTIFIER().getText()
        if field_identifier in self.moved_fields:
            self.detected_field = field_identifier

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if not self.is_source_class:
            return None
        # field_names = ctx.variableDeclarators().getText().split(",")
        field_identifier = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText()
        field_names = list()
        field_names.append(field_identifier)
        print("field_names=", field_names)
        print("Here")
        grand_parent_ctx = ctx.parentCtx.parentCtx
        if self.detected_field in field_names:
            if (not grand_parent_ctx.modifier()):
                # print("******************************************")
                modifier = ""
            else:
                modifier = grand_parent_ctx.modifier(0).getText()
            field_type = ctx.typeType().getText()
            self.code += f"{self.TAB}{modifier} {field_type} {self.detected_field};{self.NEW_LINE}"
            # delete field from source class
            # field_names.remove(self.detected_field)
            # if field_names:
            #     self.token_stream_rewriter.replaceRange(
            #         from_idx=grand_parent_ctx.start.tokenIndex,
            #         to_idx=grand_parent_ctx.stop.tokenIndex,
            #         text=f"{modifier} {field_type} {','.join(field_names)};"
            #     )
            # else:
            # self.token_stream_rewriter.delete(
            #     program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            #     from_idx=grand_parent_ctx.start.tokenIndex,
            #     to_idx=grand_parent_ctx.stop.tokenIndex
            # )
            self.detected_field = None

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.is_source_class:
            return None
        method_identifier = ctx.IDENTIFIER().getText()
        if method_identifier in self.moved_methods:
            self.detected_method = method_identifier

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.is_source_class:
            return None
        method_identifier = ctx.IDENTIFIER().getText()
        if self.detected_method == method_identifier:
            start_index = ctx.start.tokenIndex
            stop_index = ctx.stop.tokenIndex
            method_text = self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=start_index,
                stop=stop_index
            )
            self.code += (self.NEW_LINE + self.TAB + method_text + self.NEW_LINE)
            # delete method from source class
            # self.token_stream_rewriter.delete(
            #     program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            #     from_idx=start_index,
            #     to_idx=stop_index
            # )
            self.detected_method = None


def main():
    udb_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    source_class = "GodClass"
    moved_methods = ['method1', 'method3', ]
    moved_fields = ['field1', 'field2', ]

    # initialize with understand
    father_path_file = ""
    file_list_to_be_propagate = set()
    propagate_classes = set()

    db = und.open(udb_path)

    for cls in db.ents("class"):
        if (cls.simplename() == source_class):
            father_path_file = cls.parent().longname()
            for ref in cls.refs("Coupleby"):
                # print(ref.ent().longname())
                propagate_classes.add(ref.ent().longname())
                # print(ref.ent().parent().relname())
                # file_list_to_be_propagate.add(ref.ent().parent().relname())
        # if(cls.longname()==fatherclass):
        #     print(cls.parent().relname())
        #     father_path_file=cls.parent().relname()

    stream = FileStream(father_path_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = ExtractSubClassRefactoringListener(common_token_stream=token_stream,
                                                     source_class=source_class,
                                                     new_class=source_class + "extracted",
                                                     moved_fields=moved_fields, moved_methods=moved_methods)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(father_path_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())