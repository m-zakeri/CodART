"""
The module implements encapsulate field refactoring in
response to `Deficient Encapsulation` design smell.

## References
[1] G. Suryanarayana, G. Samarthyam, and T. Sharma, Refactoring for software design smells: managing technical debt,
1st ed. San Francisco, CA, USA: Morgan Kaufmann Publishers Inc., 2014.


"""
import os

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaLexer import JavaLexer


class EncapsulateFiledRefactoringListener(JavaParserLabeledListener):
    """
    To implement the encapsulate filed refactored
    Encapsulate field: Make a public field private and provide accessors
    """

    #
    def __init__(self, common_token_stream: CommonTokenStream = None,
                 package_name: str = None,
                 source_class_name: str = None,
                 field_identifier: str = None):
        """
        :param common_token_stream:
        """
        self.token_stream = common_token_stream
        if package_name is None:
            self.package_name = ''
        else:
            self.package_name = package_name
        self.source_class_name = source_class_name
        self.field_identifier = field_identifier
        self.getter_exist = False
        self.setter_exist = False
        self.in_source_class = False
        self.in_selected_package = True if self.package_name == '' else False
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = \
                TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        if self.package_name == ctx.qualifiedName().getText():
            self.in_selected_package = True
        else:
            self.in_selected_package = False

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.source_class_name:
            self.in_source_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.in_source_class = False

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if self.in_source_class and self.in_selected_package:
            if ctx.variableDeclarators().variableDeclarator(
                    0).variableDeclaratorId().getText() == self.field_identifier:
                if not ctx.parentCtx.parentCtx.modifier(0):
                    self.token_stream_rewriter.insertBeforeIndex(
                        index=ctx.typeType().stop.tokenIndex,
                        text='private ')

                elif ctx.parentCtx.parentCtx.modifier(0).getText() == 'public':
                    self.token_stream_rewriter.replaceRange(
                        from_idx=ctx.parentCtx.parentCtx.modifier(0).start.tokenIndex,
                        to_idx=ctx.parentCtx.parentCtx.modifier(0).stop.tokenIndex,
                        text='private')
                else:
                    return

                for c in ctx.parentCtx.parentCtx.parentCtx.classBodyDeclaration():
                    try:
                        print('method name: ' + c.memberDeclaration()
                              .methodDeclaration().IDENTIFIER().getText())

                        if c.memberDeclaration().methodDeclaration().IDENTIFIER() \
                                .getText() == 'get' + str.capitalize(
                            self.field_identifier):
                            self.getter_exist = True

                        if c.memberDeclaration().methodDeclaration().IDENTIFIER() \
                                .getText() == 'set' + str.capitalize(
                            self.field_identifier):
                            self.setter_exist = True

                    except:
                        print("not method !!!")

                print("setter find: " + str(self.setter_exist))
                print("getter find: " + str(self.getter_exist))

                # generate accessor and mutator methods
                # Accessor body
                new_code = ''
                if not self.getter_exist:
                    new_code = '\n\t// new getter method\n\t'
                    new_code += 'public ' + ctx.typeType().getText() + \
                                ' get' + str.capitalize(self.field_identifier)
                    new_code += '() { \n\t\treturn this.' + self.field_identifier \
                                + ';' + '\n\t}\n'

                # Mutator body
                if not self.setter_exist:
                    new_code += '\n\t// new setter method\n\t'
                    new_code += 'public void set' + str.capitalize(self.field_identifier)
                    new_code += '(' + ctx.typeType().getText() + ' ' \
                                + self.field_identifier + ') { \n\t\t'
                    new_code += 'this.' + self.field_identifier + ' = ' \
                                + self.field_identifier + ';' + '\n\t}\n'
                self.token_stream_rewriter.insertAfter(ctx.stop.tokenIndex, new_code)

                hidden = self.token_stream.getHiddenTokensToRight(ctx.stop.tokenIndex)
                # self.token_stream_rewriter.replaceRange(from_idx=hidden[0].tokenIndex,
                #                                         to_idx=hidden[-1].tokenIndex,
                #                                         text='\n\t/*End of accessor and mutator methods!*/\n\n')

    def exitExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        if self.in_source_class and self.in_selected_package:
            if ctx.expression(0).getText() == self.field_identifier or \
                    ctx.expression(0).getText() == 'this.' + self.field_identifier:
                expr_code = self.token_stream_rewriter.getText(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    start=ctx.expression(1).start.tokenIndex,
                    stop=ctx.expression(1).stop.tokenIndex)
                new_code = 'this.set' + str.capitalize(self.field_identifier) + '(' + expr_code + ')'
                self.token_stream_rewriter.replaceRange(ctx.start.tokenIndex, ctx.stop.tokenIndex, new_code)

    def exitExpression0(self, ctx: JavaParserLabeled.Expression0Context):
        if self.in_source_class and self.in_selected_package:
            try:
                if ctx.parentCtx.getChild(1).getText() in ('=', '+=', '-=',
                                                           '*=', '/=', '&=',
                                                           '|=', '^=', '>>=',
                                                           '>>>=', '<<=', '%=') and \
                        ctx.parentCtx.getChild(0) == ctx:
                    return
            except:
                pass
            if ctx.getText() == self.field_identifier:
                new_code = 'this.get' + str.capitalize(self.field_identifier) + '()'
                self.token_stream_rewriter.replaceRange(ctx.start.tokenIndex,
                                                        ctx.stop.tokenIndex,
                                                        new_code)

    def exitExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        if self.in_source_class and self.in_selected_package:
            try:
                if ctx.parentCtx.getChild(1).getText() in ('=', '+=', '-=',
                                                           '*=', '/=', '&=',
                                                           '|=', '^=', '>>=',
                                                           '>>>=', '<<=', '%=') and \
                        ctx.parentCtx.getChild(0) == ctx:
                    return
            except:
                pass
            if ctx.getText() == 'this.' + self.field_identifier:
                new_code = 'this.get' + str.capitalize(self.field_identifier) + '()'
                self.token_stream_rewriter.replaceRange(ctx.start.tokenIndex,
                                                        ctx.stop.tokenIndex,
                                                        new_code)

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        try:
            hidden = self.token_stream.getHiddenTokensToLeft(ctx.start.tokenIndex)
            self.token_stream_rewriter.replaceRange(from_idx=hidden[0].tokenIndex,
                                                    to_idx=hidden[-1].tokenIndex,
                                                    text='/*After refactoring (Refactored version)*/\n')
        except:
            pass


class InstancePropagationEncapsulateFieldListener(JavaParserLabeledListener):
    def __init__(self, token_stream_rewriter: TokenStreamRewriter = None,
                 package_name: str = None,
                 source_class_name: str = None,
                 field_identifier: str = None):
        if package_name is None:
            self.package_name = ''
        else:
            self.package_name = package_name
        self.source_class_name = source_class_name
        self.field_identifier = field_identifier
        self.has_access_to_class = False
        self.instances = list()
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if token_stream_rewriter is not None:
            self.token_stream_rewriter = \
                token_stream_rewriter
        else:
            raise TypeError('common_token_stream is None')

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        if self.package_name == ctx.qualifiedName().getText():
            self.has_access_to_class = True

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        if ctx.qualifiedName().getText() == self.package_name + '.' + self.source_class_name \
                or ctx.qualifiedName().getText() == self.package_name:
            self.has_access_to_class = True

    def exitLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        try:
            instance_class_name = ctx.variableDeclarators().variableDeclarator(0) \
                .variableInitializer().expression().creator() \
                .createdName().getText()

            if (self.has_access_to_class and instance_class_name == self.source_class_name) \
                    or instance_class_name == self.package_name + '.' + self.source_class_name:
                self.instances.append(ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().getText())
        except:
            pass

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.instances = []

    def exitExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        try:
            if ctx.parentCtx.getChild(1).getText() in ('=', '+=', '-=',
                                                       '*=', '/=', '&=',
                                                       '|=', '^=', '>>=',
                                                       '>>>=', '<<=', '%=') and \
                    ctx.parentCtx.getChild(0) == ctx:
                return
        except:
            pass

        for instance in self.instances:
            if ctx.getText() == instance + '.' + self.field_identifier:
                new_code = instance + '.get' + str.capitalize(self.field_identifier) + '()'
                self.token_stream_rewriter.replaceRange(ctx.start.tokenIndex,
                                                        ctx.stop.tokenIndex,
                                                        new_code)

    def exitExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        for instance in self.instances:
            if ctx.expression(0).getText() == instance + '.' + self.field_identifier:
                expr_code = self.token_stream_rewriter.getText(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    start=ctx.expression(1).start.tokenIndex,
                    stop=ctx.expression(1).stop.tokenIndex)
                new_code = instance + '.set' + str.capitalize(self.field_identifier) + '(' + expr_code + ')'
                self.token_stream_rewriter.replaceRange(ctx.start.tokenIndex, ctx.stop.tokenIndex, new_code)


def main(directory_path, package_name, source_class, field_name):
    print('Encapsulate Field')

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.java'):
                stream = FileStream(os.path.join(root, file), encoding='utf8', errors='ignore')
                lexer = JavaLexer(stream)
                token_stream = CommonTokenStream(lexer)
                parser = JavaParserLabeled(token_stream)
                ef_listener = EncapsulateFiledRefactoringListener(token_stream,
                                                                  package_name,
                                                                  source_class,
                                                                  field_name)
                tree = parser.compilationUnit()
                walker = ParseTreeWalker()
                walker.walk(t=tree, listener=ef_listener)

                ip_listener = InstancePropagationEncapsulateFieldListener(ef_listener.token_stream_rewriter,
                                                                          package_name,
                                                                          source_class,
                                                                          field_name)
                walker.walk(t=tree, listener=ip_listener)

                refactored = open(os.path.join(root, file), 'w', newline='')
                refactored.write(ip_listener.token_stream_rewriter.getDefaultText())
                refactored.close()

    print('Finished!')


if __name__ == "__main__":
    directory_path = "../tests/encapsulate_field_tests/NewTests"
    package_name = 'learnjava'
    source_class = 'First'
    field_name = 'score'
    main(directory_path, package_name, source_class, field_name)
