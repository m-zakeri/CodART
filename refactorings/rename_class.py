from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class RenameClassRefactoringListener(JavaParserLabeledListener):
    """
    To implement the encapsulate filed refactored
    Encapsulate field: Make a public field private and provide accessors
    """

    def __init__(self,java_file_path,
                 common_token_stream: CommonTokenStream = None,
                 class_new_name: str = None,
                 class_identifier: str = None,
                 package_identifier: str = None):
        """
        :param common_token_stream:
        """
        self.file_path = java_file_path
        self.token_stream = common_token_stream
        self.class_new_name = class_new_name
        self.class_identifier = class_identifier
        self.package_identifier = package_identifier
        self.in_class = False
        self.changed = False
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
            print(ctx.qualifiedName())
            print(ctx.getText())
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
                self.changed = True

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
                self.changed = True

    def enterConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):
        if self.in_selected_package and ctx.IDENTIFIER().getText() == self.class_identifier:
            self.token_stream_rewriter.replaceIndex(
                index=ctx.start.tokenIndex,
                text=self.class_new_name)
            self.changed = True

    def exitFieldDeclaration(self, ctx:JavaParserLabeled.FieldDeclarationContext):
        if self.package_identifier is None \
                or self.package_identifier is not None \
                and self.is_package_imported:
            if ctx.typeType().getText() == self.class_identifier:
                # change the name class; (we find right class then change the name class)
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.typeType().start.tokenIndex,
                    text=self.class_new_name)
                self.changed = True
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
                self.changed = True

    def enterCreatedName0(self, ctx:JavaParserLabeled.CreatedName0Context):
        if self.is_package_imported \
                or self.package_identifier is None \
                or self.in_selected_package:
            if ctx.getText() == self.class_identifier:
                print("ClassInstanceCreationExpression_lfno_primary1")
                self.token_stream_rewriter.replaceIndex(
                    index=ctx.start.tokenIndex,
                    text=self.class_new_name)
                self.changed = True


        
def rename_class(java_file_path, package_identifier, class_identifier, class_new_name, reference=None):
    """Main Entry Point to the Listener and Tree Walker

    Args:
        java_file_path(str): Address path to the test/source file

        scope_class_name(str): Name of the class in which the refactoring has to be done

        target_method_name(str): Name of the method in which the refactoring has to be done

        new_name(str): The new name of the refactored method

        reference(str): Keeping track for all of the method references in the project scope

    Returns:
        No Returns
"""
    stream = FileStream(java_file_path)
    lexer = JavaLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    tree = parser.compilationUnit()
    listener = RenameClassRefactoringListener(
        java_file_path=java_file_path,
        common_token_stream=tokens,
        class_new_name=class_new_name,
        class_identifier=class_identifier,
        package_identifier=package_identifier
    )
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    if listener.changed:
        #print(java_file_path)
        new_file = open(file=java_file_path, mode='w')
        new_file.write(listener.token_stream_rewriter.getDefaultText().replace('\r', ''))



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




def main():
    # TODO: Create UDB File automatically
    # db_path = "/home/ali/Documents/compiler/Research/xerces2-j/xerces2-j.udb"
    file_path = "D:/RamezaniEftekharZadeh/java-med/java-med/test/Activiti__Activiti/activiti-bpmn-layout/src/main/java/org/activiti/bpmn/BpmnAutoLayout.java"
    class_name = "bpmn"
    method_name = "BpmnAutoLayout"
    new_method_name = "BpmnAutoLayoutCC"
    # references = get_method_calls(db_path, class_name, method_name)
    rename_class(file_path, class_name, method_name, new_method_name)

    # for ref in references:
        # rename_method(ref["file_path"], ref["scope"].split(".")[0], target_method_name=method_name,
        #               new_name=new_method_name, reference=ref)

if __name__ == '__main__':
    main()