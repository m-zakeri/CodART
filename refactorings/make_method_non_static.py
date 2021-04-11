"""
The scripts implements different refactoring operations


"""
__version__ = '0.1.0'
__author__ = 'Morteza'

import networkx as nx

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

import visualization.graph_visualization

try:
    import understand as understand
except ImportError as e:
    print(e)


class Parameter:
    def __init__(self, parameterType, name):
        self.parameterType = parameterType
        self.name = name


class ConstructorOrMethod:
    def __init__(self, text: str = None, name: str = None, parameters: Parameter = None):
        self.text = text
        self.name = name
        self.parameters = parameters


class MakeMethodNonStaticRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(
            self, common_token_stream: CommonTokenStream = None,
            target_class: str = None, target_methods: list = None):

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if target_class is None:
            raise ValueError("source_class is None")
        else:
            self.target_class = target_class
        if target_methods is None or len(target_methods) == 0:
            raise ValueError("target method must have one method name")
        else:
            self.target_methods = target_methods

        self.target_class_data = None
        self.is_target_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.target_class:
            self.is_target_class = True
            self.target_class_data = {'constructors': []}
        else:
            self.is_target_class = False

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_target_class:
            have_default_constructor = False
            for constructor in self.target_class_data['constructor']:
                if len(constructor.parameters) == 0:
                    have_default_constructor = True
                    break
            if not have_default_constructor:
                self.token_stream_rewriter.insertBeforeIndex(
                    index=ctx.stop.tokenIndex - 1,
                    text=f'\n\t public {self.target_class_data["constructors"][0]} ()\n\t{{}}\n'
                )
            self.is_target_class = False

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_target_class:
            if ctx.IDENTIFIER().getText() in self.target_methods:
                grand_parent_ctx = ctx.parentCtx.parentCtx
                if grand_parent_ctx.modifier():
                    if len(grand_parent_ctx.modifier()) == 2:
                        self.token_stream_rewriter.delete(
                            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                            from_idx=grand_parent_ctx.modifier(1).start.tokenIndex - 1,
                            to_idx=grand_parent_ctx.modifier(1).stop.tokenIndex
                        )
                    else:
                        if grand_parent_ctx.modifier(0).getText() == 'static':
                            self.token_stream_rewriter.delete(
                                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                                from_idx=grand_parent_ctx.modifier(0).start.tokenIndex - 1,
                                to_idx=grand_parent_ctx.modifier(0).stop.tokenIndex
                            )
                else:
                    return None

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        if self.is_target_class:
            if ctx.formalParameters().formalParameterList():
                constructor_parameters = [ctx.formalParameters().formalParameterList().children[i] for i in
                                          range(len(ctx.formalParameters().formalParameterList().children)) if
                                          i % 2 == 0]
            else:
                constructor_parameters = []
            constructor_text = ''
            for modifier in ctx.parentCtx.parentCtx.modifier():
                constructor_text += modifier.getText() + ' '
                constructor_text += ctx.IDENTIFIER().getText()
            constructor_text += ' ( '
            for parameter in constructor_parameters:
                constructor_text += parameter.typeType().getText() + ' '
                constructor_text += parameter.variableDeclaratorId().getText() + ', '
            if constructor_parameters:
                constructor_text = constructor_text[:len(constructor_text) - 2]
            constructor_text += ')\n\t{'
            constructor_text += self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.block().start.tokenIndex + 1,
                stop=ctx.block().stop.tokenIndex - 1
            )
            constructor_text += '}\n'
            self.target_class_data['constructors'].append(ConstructorOrMethod(
                name=self.target_class,
                parameters=[Parameter(parameterType=p.typeType().getText(),
                                      name=p.variableDeclaratorId().IDENTIFIER().getText()) for p in
                            constructor_parameters],
                text=constructor_text))


def main(udb_path, target_class, target_methods):
    main_file = ""
    db = understand.open(udb_path)
    for cls in db.ents("class"):
        if cls.simplename() == target_class:
            main_file = cls.parent().longname()

    stream = FileStream(main_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = MakeMethodNonStaticRefactoringListener(common_token_stream=token_stream, target_class=target_class,
                                                         target_methods=target_methods)
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(main_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_rewriter.getDefaultText())


if __name__ == '__main__':
    udb_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    target_class = "Website"
    target_methods = "HELLO_FROM_STUDENT_WEBSITE"
    # initialize with understand
    main(udb_path, target_class, target_methods)
