"""


"""

__version__ = '0.1.0'
__author__ = 'IUST-Students'

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from refactorings.remove_class import RemoveClassRefactoringListener

# from utilization.setup_understand import *


class CollapseHierarchyRefactoringGetFieldTextListener(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, child_class=None):

        if child_class is None:
            self.moved_fields = []
        else:
            self.child_class = child_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_children_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.fieldcode = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):

        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.child_class:
            self.is_source_class = True
            self.fieldcode += self.NEW_LINE * 2
            self.fieldcode += f"// child class({self.child_class}) fields: " + self.NEW_LINE
        else:
            self.is_source_class = False

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_source_class:
            self.is_source_class = False

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        self.token_stream_rewriter.insertAfter(
            index=ctx.stop.tokenIndex,
            text=self.fieldcode
        )

    # def enterVariableDeclaratorId(self, ctx:JavaParserLabeled.VariableDeclaratorIdContext):
    #     if not self.is_source_class:
    #         return None
    #     self.detected_field = ctx.IDENTIFIER().getText()

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if not self.is_source_class:
            return None
        self.detected_field = ctx.variableDeclarators().getText().split(',')
        print("Here it is a field")
        grand_parent_ctx = ctx.parentCtx.parentCtx
        modifier = ""
        for i in range(0, len(grand_parent_ctx.modifier())):
            modifier += grand_parent_ctx.modifier(i).getText()
            modifier += " "
        field_type = ctx.typeType().getText()
        self.fieldcode += f"{self.TAB}{modifier} {field_type} {self.detected_field[0]};{self.NEW_LINE}"


class CollapseHierarchyRefactoringGetMethodTextListener(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, child_class=None):

        if child_class is None:
            self.moved_methods = []
        else:
            self.child_class = child_class
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        self.is_children_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.methodcode = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):

        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.child_class:
            self.is_source_class = True
            self.methodcode += self.NEW_LINE * 2
            self.methodcode += f"// child class({self.child_class}) methods: " + self.NEW_LINE
        else:
            self.is_source_class = False

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_source_class:
            self.is_source_class = False

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        self.token_stream_rewriter.insertAfter(
            index=ctx.stop.tokenIndex,
            text=self.methodcode
        )

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.is_source_class:
            return None
        self.detected_method = ctx.IDENTIFIER().getText()

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.is_source_class:
            return None
        method_identifier = ctx.IDENTIFIER().getText()
        print("Here it is a method")

        grand_parent_ctx = ctx.parentCtx.parentCtx
        modifier = ""
        for i in range(0, len(grand_parent_ctx.modifier())):
            modifier += grand_parent_ctx.modifier(i).getText()
            modifier += " "

        if self.detected_method == method_identifier:
            start_index = ctx.start.tokenIndex
            stop_index = ctx.stop.tokenIndex
            method_text = self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=start_index,
                stop=stop_index
            )
            self.methodcode += (self.NEW_LINE + self.TAB + modifier + method_text + self.NEW_LINE)


class CollapseHierarchyRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, parent_class=None, child_class=None,
                 field_text: str = None, method_text: str = None):

        if method_text is None:
            self.mothod_text = []
        else:
            self.method_text = method_text

        if field_text is None:
            self.field_text = []
        else:
            self.field_text = field_text
        if parent_class is None:
            self.parent_class = []
        else:
            self.parent_class = parent_class

        if child_class is None:
            self.child_class = []
        else:
            self.child_class = child_class

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if parent_class is None:
            raise ValueError("destination_class is None")
        else:
            self.parent_class = parent_class

        self.is_parent_class = False
        self.is_child_class = False
        self.detected_field = None
        self.detected_method = None

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier in self.parent_class:
            self.is_parent_class = True

        elif class_identifier in self.child_class:
            self.is_child_class = True

        else:
            print("enter other class")
            self.is_parent_class = False

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        classDecctx = ctx.parentCtx
        class_identifier = classDecctx.IDENTIFIER().getText()
        if class_identifier in self.parent_class:
            self.token_stream_rewriter.replaceRange(
                from_idx=ctx.start.tokenIndex + 1,
                to_idx=ctx.start.tokenIndex + 1,
                text="\n" + self.field_text + "\n" + self.method_text + "\n"
            )

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_parent_class:
            self.is_parent_class = False

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.is_child_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        # delete method from source class
        self.token_stream_rewriter.delete(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            from_idx=grand_parent_ctx.start.tokenIndex,
            to_idx=grand_parent_ctx.stop.tokenIndex
        )
        self.detected_method = None

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if not self.is_child_class:
            return None
        grand_parent_ctx = ctx.parentCtx.parentCtx
        # delete field from source class
        self.token_stream_rewriter.delete(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            from_idx=grand_parent_ctx.start.tokenIndex,
            to_idx=grand_parent_ctx.stop.tokenIndex
        )
        self.detected_field = None

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        pass


class PropagationCollapseHierarchyListener(JavaParserLabeledListener):

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


def main(udb, child, parent):
    # initialize with understand
    udb_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    child_path_file = ""
    father_path_file = ""
    file_list_to_be_propagate = set()
    propagate_classes = set()
    # db = und.open(udb)
    # for cls in db.ents("class"):
    #     if cls.simplename() == child:
    #         child_path_file = cls.parent().longname()
    #         for ref in cls.refs("Coupleby"):
    #             propagate_classes.add(ref.ent().longname())
    #             file_list_to_be_propagate.add(ref.ent().parent().longname())
    #     if cls.simplename() == parent:
    #         father_path_file = cls.parent().longname()

    file_list_to_be_propagate = list(file_list_to_be_propagate)
    propagate_classes = list(propagate_classes)

    stream = FileStream(child_path_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener_field_text = CollapseHierarchyRefactoringGetFieldTextListener(common_token_stream=token_stream,
                                                                              child_class=child)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener_field_text)
    field_code = my_listener_field_text.fieldcode

    my_listener_method_text = CollapseHierarchyRefactoringGetMethodTextListener(common_token_stream=token_stream,
                                                                                child_class=child)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener_method_text)
    methods_code = my_listener_method_text.methodcode

    # Remove child class
    my_listener_remove_child_class = RemoveClassRefactoringListener(common_token_stream=token_stream,
                                                                    class_name=child)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener_remove_child_class)
    with open(child_path_file, mode='w', newline='') as f:
        f.write(my_listener_remove_child_class.token_stream_rewriter.getDefaultText())
    # Refactor
    stream = FileStream(father_path_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener_refactor_action = CollapseHierarchyRefactoringListener(common_token_stream=token_stream,
                                                                       parent_class=parent,
                                                                       child_class=child,
                                                                       field_text=field_code,
                                                                       method_text=methods_code)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener_refactor_action)

    with open(father_path_file, mode='w', newline='') as f:
        f.write(my_listener_refactor_action.token_stream_rewriter.getDefaultText())
    # Propagate
    for file in file_list_to_be_propagate:
        stream = FileStream(file, encoding='utf8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        my_listener_propagate = PropagationCollapseHierarchyListener(token_stream_rewriter=token_stream,
                                                                     old_class_name=child,
                                                                     new_class_name=parent,
                                                                     propagated_class_name=propagate_classes)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener_propagate)

        with open(file, mode='w', newline='') as f:
            f.write(my_listener_propagate.token_stream_rewriter.getDefaultText())
