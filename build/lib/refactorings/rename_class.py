from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled

class RenameClassRefactoringListener(JavaParserLabeledListener):
    """
    To implement the encapsulate filed refactored
    Encapsulate field: Make a public field private and provide accessors
    """

    def __init__(self,
                 common_token_stream: CommonTokenStream = None,
                 class_new_name: str = None,
                 class_identifier: str = None,
                 package_identifier: str = None):
        """
        :param common_token_stream:
        """
        self.token_stream = common_token_stream
        self.class_new_name = class_new_name
        self.class_identifier = class_identifier
        self.package_identifier = package_identifier
        self.declared_objects_names = []

        self.is_package_imported = False
        self.in_selected_package = False
        self.in_selected_class = False
        self.in_some_package = False

        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterPackageDeclaration(self, ctx:JavaParserLabeled.PackageDeclarationContext):
        self.in_some_package = True
        if self.package_identifier is not None:
            if self.package_identifier == ctx.qualifiedName().getText():
                self.in_selected_package = True
                print("Package Found")

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        if self.package_identifier is None \
                and not self.in_some_package \
                or self.package_identifier is not None \
                and self.in_selected_package:
            if ctx.IDENTIFIER().getText() == self.class_identifier:
                print("Class Found")
                self.in_selected_class = True
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex + 2,
                    text=self.class_new_name)

    def enterImportDeclaration(self, ctx:JavaParserLabeled.ImportDeclarationContext):
        if self.package_identifier is not None:
            if ctx.getText() == "import" + self.package_identifier + "." + self.class_identifier + ";"\
                    or ctx.getText() == "import" + self.package_identifier + ".*" + ";"\
                    or ctx.getText() == "import" +  self.package_identifier + ";":
                self.is_package_imported = True
            if ctx.getText() == "import" + self.package_identifier + "." + self.class_identifier + ";":
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.qualifiedName().start.tokenIndex + 2*len(ctx.qualifiedName().IDENTIFIER()) - 2,
                    text=self.class_new_name)

    def enterConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):
        if self.in_selected_package and ctx.IDENTIFIER().getText() == self.class_identifier:
            self.token_stream_rewriter.replaceIndex(
                index=ctx.start.tokenIndex,
                text=self.class_new_name)

    def exitFieldDeclaration(self, ctx:JavaParserLabeled.FieldDeclarationContext):
        if self.package_identifier is None \
                or self.package_identifier is not None \
                and self.is_package_imported:
            if ctx.typeType().getText() == self.class_identifier:
                # change the name class; (we find right class then change the name class)
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.typeType().start.tokenIndex,
                    text=self.class_new_name)
                print("class name has change to new_class_name")


    # def enterExpressionName2(self, ctx:Java9_v2Parser.ExpressionName1Context):
    #     if self.is_package_imported \
    #             or self.package_identifier is None \
    #             or self.in_selected_package:
    #         if ctx.getText() == self.class_identifier:
    #             self.token_stream_rewriter.replaceIndex(
    #                 index=ctx.start.tokenIndex,
    #                 text=self.class_identifier)
    #
    def exitPrimary4(self, ctx:JavaParserLabeled.Primary4Context):
        if self.is_package_imported \
                or self.package_identifier is None \
                or self.in_selected_package:
            if ctx.getText() == self.class_identifier:
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex,
                    text=self.class_new_name)

    def enterCreatedName0(self, ctx:JavaParserLabeled.CreatedName0Context):
        if self.is_package_imported \
                or self.package_identifier is None \
                or self.in_selected_package:
            if ctx.getText() == self.class_identifier:
                print("ClassInstanceCreationExpression_lfno_primary1")
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex,
                    text=self.class_new_name)




    # def enterTypeName1(self, ctx:Java9_v2Parser.TypeName1Context):
    #     if self.is_package_imported \
    #             or self.package_identifier is None \
    #             or self.in_selected_package:
    #         if ctx.identifier().getText() == self.class_identifier:
    #             print(" type name 1")
    #             self.token_stream_rewriter.replaceIndex(
    #                 index=ctx.identifier().start.tokenIndex,
    #                 text=self.class_new_name)
    #
    #
    # def enterCompilationUnit1(self, ctx: Java9_v2Parser.CompilationUnit1Context):
    #     hidden = self.token_stream.getHiddenTokensToLeft(ctx.start.tokenIndex)
    #     self.token_stream_rewriter.replaceRange(from_idx=hidden[0].tokenIndex,
    #                                             to_idx=hidden[-1].tokenIndex,
    #                                             text='/*After refactoring (Refactored version)*/\n')



