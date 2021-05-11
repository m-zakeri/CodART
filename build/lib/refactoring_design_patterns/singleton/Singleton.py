from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class SingletonRefactoringListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream = None,
                 class_identifier: str = None):
        """
        :param common_token_stream:
        """
        self.enter_class = False
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        self.ObjectIndex = []
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.class_identifier:
            self.enter_class = True
            new_code = "\n\tprivate static " + self.class_identifier + " Instance = null;\n\t"
            self.token_stream_rewriter.insertAfter(ctx.classBody().start.tokenIndex + 1, new_code)
            self.addInstance = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.enter_class == True:
            self.enter_class = False
            new_code = "\n\tpublic static " + self.class_identifier + " getInstance()\n\t{\n\t\tif (Instance == null)" \
                                                                      "\n\t\t\tInstance = new " + self.class_identifier + "();" \
                                                                                                                          "\n\t\treturn Instance;\n\t}\n"
            self.token_stream_rewriter.insertAfter(ctx.stop.tokenIndex - 1, new_code)

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        if self.enter_class == True:
            constructorModifier = ctx.parentCtx.parentCtx
            if constructorModifier.start.text == 'public':
                self.token_stream_rewriter.replaceRange(
                    from_idx=constructorModifier.start.tokenIndex,
                    to_idx=constructorModifier.start.tokenIndex,
                    text='private')

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if self.enter_class == False:
            A = ctx.parentCtx.parentCtx
            B = ctx.variableDeclarators()
            if ctx.start.text == self.class_identifier:
                start = ctx.variableDeclarators().variableDeclarator(0).ASSIGN().symbol.tokenIndex + 1
                end = ctx.stop.tokenIndex
                self.ObjectIndex.append([start, end])

    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        if self.enter_class == False:
            if ctx.start.text == self.class_identifier:
                start = ctx.variableDeclarators().variableDeclarator(0).ASSIGN().symbol.tokenIndex + 1
                end = ctx.stop.tokenIndex
                self.ObjectIndex.append([start, end])

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        for item in self.ObjectIndex:
            self.token_stream_rewriter.replaceRange(from_idx=item[0],
                                                    to_idx=item[1],
                                                    text=" " + self.class_identifier + ".getInstance()")
