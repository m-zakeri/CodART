import os
from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaLexer import JavaLexer
from refactorings.utils.utils2 import get_filenames_in_dir


class ReplaceConstructorWithFactoryFunctionRefactoringListener(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None,
                 target_class: str = None):

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.codeRewrite = TokenStreamRewriter(common_token_stream)

        if target_class is None:
            raise ValueError("source_class is None")
        else:
            self.target_class = target_class

        self.is_target_class = False
        self.have_constructor = False
        self.new_factory_function = False
        self.new_parameters = []
        self.new_parameters_names = []

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        # self.target_class = ctx.IDENTIFIER().getText()
        # have_constructor = False
        # if ctx.IDENTIFIER().getText() ==
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.target_class:
            self.is_target_class = True
            # print("class name " + ctx.IDENTIFIER().getText())
        else:
            self.is_target_class = False

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_target_class:
            self.is_target_class = False

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        if self.is_target_class:
            # print("constructor name " + ctx.IDENTIFIER().getText())
            # parameters = ctx.formalParameters().getText()
            # print(len(ctx.formalParameters().formalParameterList().formalParameter()))
            grandParentCtx = ctx.parentCtx.parentCtx
            if ctx.IDENTIFIER().getText() == self.target_class:
                self.have_constructor = True
                # do refactor
                """
                Declare the constructor private.
                """
                if grandParentCtx.modifier():
                    if 'public' == grandParentCtx.modifier(0).getText():
                        self.codeRewrite.replaceRange(
                            from_idx=grandParentCtx.modifier(0).start.tokenIndex,
                            to_idx=grandParentCtx.modifier(0).stop.tokenIndex,
                            text='private')
                else:
                    self.codeRewrite.insertBeforeIndex(
                        index=ctx.start.tokenIndex,
                        text="private "
                    )

    def exitConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        """
        Create a factory method. Make its body a call to the current constructor.
        """
        if self.is_target_class:
            grandParentCtx = ctx.parentCtx.parentCtx
            self.codeRewrite.insertAfter(
                index=grandParentCtx.stop.tokenIndex,
                text="\n    public static " + ctx.IDENTIFIER().getText() + " Create( " + ", ".join(
                    self.new_parameters) +
                     "){\n       return new " + ctx.IDENTIFIER().getText() + "(" + ", ".join(
                    self.new_parameters_names) + ");\n}"
            )
        self.new_parameters = []
        self.new_parameters_names = []

    def enterFormalParameterList0(self, ctx: JavaParserLabeled.FormalParameterList0Context):
        # print(len(ctx.formalParameter()))
        pass

    def exitFormalParameterList0(self, ctx: JavaParserLabeled.FormalParameterList0Context):
        pass

    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        # print(ctx.typeType().getText())
        # print(ctx.variableDeclaratorId().getText())
        constructorName = ctx.parentCtx.parentCtx.parentCtx.IDENTIFIER().getText()
        if self.target_class == constructorName:
            text = ctx.typeType().getText() + " " + ctx.variableDeclaratorId().getText()
            self.new_parameters.append(text)
            self.new_parameters_names.append(ctx.variableDeclaratorId().getText())

    def exitFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        pass

    def enterExpression4(self, ctx: JavaParserLabeled.Expression4Context):
        """
            Replace all constructor calls with calls to the factory method.
        """
        # currentMethodOrClassCtx=ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx
        # print(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.getText())
        if ctx.creator().createdName().getText() == self.target_class:
            self.codeRewrite.replaceRange(
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex,
                text=self.target_class + "." + "Create" + ctx.creator().classCreatorRest().getText())


def main():
    # folder_path = "..\\benchmark_projects\\JSON\\src\\main\\java\\org\\json"
    folder_path = "/data/Dev/JavaSample/"
    path = get_filenames_in_dir(folder_path)
    print(path)
    # target_class = "CDL"
    target_class = "ReplaceConstructorWithFactoryMethod"

    for file in path:
        if file.endswith('.java') and not file.endswith('_refactored.java'):
            stream = FileStream(file)
            lexer = JavaLexer(stream)
            tokens = CommonTokenStream(lexer)
            parser = JavaParserLabeled(tokens)
            tree = parser.compilationUnit()
            new_file = open(file, mode='w', newline='')
            listener = ReplaceConstructorWithFactoryFunctionRefactoringListener(common_token_stream=tokens,
                                                                                target_class=target_class)
            walker = ParseTreeWalker()
            walker.walk(
                listener=listener,
                t=tree
            )
            new_code = str(listener.codeRewrite.getDefaultText())
            new_file.write(new_code)


if __name__ == "__main__":
    main()
