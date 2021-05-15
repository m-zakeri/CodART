from gen.javaLabeled.JavaLexer import JavaLexer

try:
    import understand as und
except ImportError as e:
    print(e)

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener




class PushDownGetTextFieldListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream, father: str = None, field=None):
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        if father is None:
            raise ValueError("source_class is None")
        else:
            self.father = father

        if field is None:
            raise ValueError("field is None")
        else:
            self.field = field

        self.field_text = ""

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        ctx1 = ctx.parentCtx.parentCtx.parentCtx.parentCtx
        class_identifier = ctx1.IDENTIFIER().getText()
        if class_identifier in self.father:
            # field_identifier = ctx.variableDeclarators().getText().split(",")
            field_identifier = ctx.variableDeclarators().variableDeclarator(
                0).variableDeclaratorId().IDENTIFIER().getText()
            if self.field in field_identifier:
                ctx1 = ctx.parentCtx.parentCtx
                start_index = ctx1.start.tokenIndex
                stop_index = ctx1.stop.tokenIndex
                self.field_text = self.token_stream_rewriter.getText(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    start=start_index,
                    stop=stop_index)


class PushDownFieldRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, source_class: str = None, children_class=None,
                 moved_fields=None, fieldtext=None):

        if moved_fields is None:
            self.moved_fields = []
        else:
            self.moved_fields = moved_fields
        if children_class is None:
            self.moved_fields = []
        else:
            self.children_class = children_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if source_class is None:
            raise ValueError("source_class is None")
        else:
            self.source_class = source_class
        #
        if fieldtext is None:
            raise ValueError("fieldtext is None")
        else:
            self.fieldtext = fieldtext
        #
        # if destination_class is None:
        #     raise ValueError("new_class is None")
        # else:
        #     self.destibation_class = destination_class

        self.is_source_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""
        self.tempdeclarationcode = ""
        self.field_text = ""

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):

        if self.is_source_class:

            # field_identifier = ctx.variableDeclarators().getText().split(",")
            field_identifier = ctx.variableDeclarators().variableDeclarator(
                0).variableDeclaratorId().IDENTIFIER().getText()
            print(field_identifier)
            if self.moved_fields[0] in field_identifier:
                ctx1 = ctx.parentCtx.parentCtx
                start_index = ctx1.start.tokenIndex
                stop_index = ctx1.stop.tokenIndex
                self.field_text = self.token_stream_rewriter.getText(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    start=start_index,
                    stop=stop_index)
                self.token_stream_rewriter.delete(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=ctx1.start.tokenIndex,
                    to_idx=ctx1.stop.tokenIndex
                )

            print(self.field_text)

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = True

        elif class_identifier == "B":
            print("enter B class")

            self.is_source_class = False

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        ctx1 = ctx.parentCtx
        class_identifier = ctx1.IDENTIFIER().getText()
        if class_identifier in self.children_class:
            self.token_stream_rewriter.replaceRange(
                from_idx=ctx.start.tokenIndex + 1,
                to_idx=ctx.start.tokenIndex + 1,
                text="\n" + self.fieldtext + "\n"
            )

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_source_class:
            # self.code += "}"
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

    # def exitFieldDeclaration(self, ctx:JavaParserLabeled.FieldDeclarationContext):
    #     if not self.is_source_class:
    #         return None
    #     field_names = ctx.variableDeclarators().getText().split(",")
    #     print("Here")
    #     grand_parent_ctx = ctx.parentCtx.parentCtx
    #     if self.detected_field in field_names:
    #         modifier = grand_parent_ctx.modifier(0).getText()
    #         field_type = ctx.typeType().getText()
    #         self.code += f"{self.TAB}{modifier} {field_type} {self.detected_field};{self.NEW_LINE}"
    #         # delete field from source class
    #         field_names.remove(self.detected_field)
    #         if field_names:
    #             self.token_stream_rewriter.replaceRange(
    #                 from_idx=grand_parent_ctx.start.tokenIndex,
    #                 to_idx=grand_parent_ctx.stop.tokenIndex,
    #                 text=f"{modifier} {field_type} {','.join(field_names)};"
    #             )
    #         else:
    #             self.token_stream_rewriter.delete(
    #                 program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
    #                 from_idx=grand_parent_ctx.start.tokenIndex,
    #                 to_idx=grand_parent_ctx.stop.tokenIndex
    #             )
    #         self.detected_field = None

    # def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
    #     if not self.is_source_class:
    #         return None
    #     method_identifier = ctx.IDENTIFIER().getText()
    #     if method_identifier in self.moved_methods:
    #         self.detected_method = method_identifier

    # def exitMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
    #     if not self.is_source_class:
    #         return None
    #     method_identifier = ctx.IDENTIFIER().getText()
    #     if self.detected_method == method_identifier:
    #         start_index = ctx.start.tokenIndex
    #         stop_index = ctx.stop.tokenIndex
    #         method_text = self.token_stream_rewriter.getText(
    #             program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
    #             start=start_index,
    #             stop=stop_index
    #         )
    #         self.code += (self.NEW_LINE + self.TAB + method_text + self.NEW_LINE)
    #         # delete method from source class
    #         self.token_stream_rewriter.delete(
    #             program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
    #             from_idx=start_index,
    #             to_idx=stop_index
    #         )
    #         self.detected_method = None


class PropagationPushDownFieldRefactoringListener(JavaParserLabeledListener):

    def __init__(self, token_stream_rewriter: CommonTokenStream = None, old_class_name: list = None,
                 new_class_name: str = None, propagated_class_name: list = None):

        if propagated_class_name is None:
            self.propagated_class_name = []
        else:
            self.propagated_class_name = propagated_class_name

        if new_class_name is None:
            self.new_class_name = []
        else:
            self.new_class_name = new_class_name

        if old_class_name is None:
            self.old_class_name = []
        else:
            self.old_class_name = old_class_name

        if token_stream_rewriter is None:
            raise ValueError('token_stream_rewriter is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(token_stream_rewriter)

        self.is_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""
        self.tempdeclarationcode = ""
        self.method_text = ""

    def enterVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        print("Propagation started, please wait...")
        if not self.is_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        class_identifier = grand_parent_ctx.typeType().getText()
        if class_identifier in self.old_class_name:
            self.token_stream_rewriter.replaceRange(
                from_idx=grand_parent_ctx.typeType().start.tokenIndex,
                to_idx=grand_parent_ctx.typeType().stop.tokenIndex,
                text=self.new_class_name
            )
            grand_child_ctx = ctx.variableInitializer().expression().creator().createdName()
            self.token_stream_rewriter.replaceRange(
                from_idx=grand_child_ctx.start.tokenIndex,
                to_idx=grand_child_ctx.stop.tokenIndex,
                text=self.new_class_name
            )

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier in self.propagated_class_name:
            self.is_class = True

        else:
            print("enter other class")
            self.is_class = False


if __name__ == '__main__':
    udb_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    source_class = "App"
    moved_fields = ["push_down_field", ]
    # initialize with understand
    fileslist_to_be_propagate = set()
    propagation_classes = set()
    children_class = set()
    fileslist_to_be_rafeactored = set()
    main_file = ""
    db = und.open(udb_path)

    for field in db.ents("Java Variable"):
        if field.longname().endswith(source_class + "." + moved_fields[0]):
            main_file = field.parent().parent().longname()
            for ref in field.refs("Java Setby , Useby"):
                # Get File
                if ref.ent().parent().parent():
                    fileslist_to_be_propagate.add(ref.ent().parent().parent().longname())
                # Get Class
                if ref.ent().parent():
                    propagation_classes.add(ref.ent().parent().longname())
    for classname in db.ents("class"):
        if classname.simplename() == source_class:
            for childcls in classname.refs("Extendby"):
                children_class.add(childcls.ent().longname())
                fileslist_to_be_rafeactored.add(childcls.ent().parent().longname())

    fileslist_to_be_propagate = list(fileslist_to_be_propagate)
    propagation_classes = list(propagation_classes)
    children_class = list(children_class)
    fileslist_to_be_rafeactored = list(fileslist_to_be_rafeactored)
    print("Main File :", main_file)
    print("fileslist_to_be_propagate :", fileslist_to_be_propagate)
    print("propagation_classes : ", propagation_classes)
    print("children_class :", children_class)
    print("fileslist_to_be_rafeactored :", fileslist_to_be_rafeactored)
    print("==============================================================================")
    # get text
    stream = FileStream(main_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    get_text = PushDownGetTextFieldListener(common_token_stream=token_stream, father=source_class,
                                            field=moved_fields[0])
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=get_text)

    field_text = get_text.field_text
    print(field_text)
    # begin refactoring
    for file in fileslist_to_be_rafeactored:
        stream = FileStream(file, encoding='utf8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        my_listener = PushDownFieldRefactoringListener(common_token_stream=token_stream, source_class=source_class,
                                                       children_class=children_class, moved_fields=moved_fields,
                                                       fieldtext=field_text)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        with open(file, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())
    # end of refactored

    # beginning of propagate
    for file in fileslist_to_be_propagate:
        stream = FileStream(file, encoding='utf8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        my_listener = PropagationPushDownFieldRefactoringListener(token_stream_rewriter=token_stream,
                                                                  old_class_name=source_class,
                                                                  new_class_name=children_class[0],
                                                                  propagated_class_name=propagation_classes)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        with open(file, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())
