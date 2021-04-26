import argparse
import os

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class MoveClassRefactoringListener(JavaParserLabeledListener):
    """
    To implement the move class refactoring
    a stream of tokens is sent to the listener, to build an object token_stream_rewriter
    and we move all class methods and fields from the source package to the target package
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, class_identifier: str = None,
                 source_package: str = None, target_package: str = None, filename: str = None, dirname: str = None):
        """
        :param common_token_stream:
        """
        self.enter_class = False
        self.token_stream = common_token_stream
        self.class_found = False
        self.class_fields = []
        self.class_methods = []

        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

        if class_identifier is not None:
            self.class_identifier = class_identifier
        else:
            raise ValueError("class_identifier is None")

        if filename is not None:
            self.filename = filename
        else:
            raise ValueError("filename is None")

        if dirname is not None:
            self.dirname = dirname
        else:
            raise ValueError("dirname is None")

        if source_package is not None:
            self.source_package = source_package
        else:
            raise ValueError("source_package is None")

        if target_package is not None:
            self.target_package = target_package
        else:
            raise ValueError("target_package is None")

        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = f"package {self.target_package};{self.NEW_LINE}{self.NEW_LINE}"

    # Exit a parse tree produced by JavaParserLabeled#importDeclaration.
    def exitImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        text_to_replace = "import " + ctx.qualifiedName().getText() + ';'
        if ctx.STATIC() is not None:
            text_to_replace = text_to_replace.replace("import", "import static")

        self.code += text_to_replace + self.NEW_LINE

    # Enter a parse tree produced by JavaParserLabeled#packageDeclaration.
    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        package_name = ctx.getText()[7:-1]
        print(package_name)
        if package_name != self.source_package:
            raise ValueError(f"The package {package_name} in the file isn't equal to the source package!")

    # Exit a parse tree produced by JavaParserLabeled#classBodyDeclaration2.
    def exitClassBodyDeclaration2(self, ctx: JavaParserLabeled.ClassBodyDeclaration2Context):
        self.enter_class = False
        try:
            if ctx.memberDeclaration().classDeclaration().IDENTIFIER().getText() != self.class_identifier:
                return
        except Exception:
            return

        self.class_found = True

        start_index = ctx.start.tokenIndex
        stop_index = ctx.stop.tokenIndex

        # get the class body from the token_stream_rewriter
        class_body = self.token_stream_rewriter.getText(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            start=start_index,
            stop=stop_index
        )

        self.code += f"import {self.source_package}.*;"
        self.code += self.NEW_LINE * 2
        self.code += f"// Class \"{self.class_identifier}\" moved here " \
                     f"from package {self.source_package} by CodART" + self.NEW_LINE + \
                     f"{class_body}"

        # delete class declaration from source class
        self.token_stream_rewriter.delete(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            from_idx=start_index,
            to_idx=stop_index
        )

        old_file = open(self.filename, 'w')
        old_file.write(self.token_stream_rewriter.getDefaultText().replace("\r", ""))

        print("----------------------------")
        print("Class attributes: ", str(self.class_fields))
        print("Class methods: ", str(self.class_methods))
        print("----------------------------")

    # Exit a parse tree produced by JavaParserLabeled#typeDeclaration.
    def exitTypeDeclaration(self, ctx: JavaParserLabeled.TypeDeclarationContext):
        if ctx.classDeclaration() is not None:
            self.enter_class = False
            if ctx.classDeclaration().IDENTIFIER().getText() != self.class_identifier:
                return



            self.enter_class = True
            self.class_found = True

            start_index = ctx.start.tokenIndex
            stop_index = ctx.stop.tokenIndex

            # get the class body from the token_stream_rewriter
            class_body = self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=start_index,
                stop=stop_index
            )

            self.code += f"import {self.source_package}.*;"
            self.code += self.NEW_LINE * 2
            self.code += f"// Class \"{self.class_identifier}\" moved here " \
                         f"from package {self.source_package} by CodART" + self.NEW_LINE + \
                         f"{class_body}"

            # delete class declaration from source class
            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=start_index,
                to_idx=stop_index
            )

            print("----------------------------")
            print("Class attributes: ", str(self.class_fields))
            print("Class methods: ", str(self.class_methods))
            print("----------------------------")

    # Enter a parse tree produced by JavaParserLabeled#fieldDeclaration.
    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if not self.enter_class:
            return

        list_of_fields = ctx.variableDeclarators().getText().split(",")

        for field in list_of_fields:
            self.class_fields.append(field)

    # Enter a parse tree produced by JavaParserLabeled#methodDeclaration.
    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.enter_class:
            return
        method_name = ctx.IDENTIFIER().getText()
        self.class_methods.append(method_name)

    # Exit a parse tree produced by JavaParserLabeled#compilationUnit.
    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        if not self.class_found:
            raise ValueError(f"Class \"{self.class_identifier}\" NOT FOUND!")

        file_address = self.dirname + '/' + self.target_package.replace('.',
                                                                        '/') + '/' + self.class_identifier + '.java'

        new_file = open(file_address, 'w')
        new_file.write(self.code.replace("\r", ""))
        print(f"The class \"{self.class_identifier}\" moved to the target package successfully!")



class ReplaceDependentObjectsListener(JavaParserLabeledListener):
    """
    To implement the move class refactoring
    a stream of tokens is sent to the listener, to build an object token_stream_rewriter
    and we move all class methods and fields from the source package to the target package
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, class_identifier: str = None,
                 source_package: str = None, target_package: str = None, filename: str = None, has_import: bool = None):
        """
        :param common_token_stream:
        """
        self.token_stream = common_token_stream

        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

        if class_identifier is not None:
            self.class_identifier = class_identifier
        else:
            raise ValueError("class_identifier is None")

        if filename is not None:
            self.filename = filename
        else:
            raise ValueError("filename is None")

        if has_import is not None:
            self.has_import = has_import
        else:
            raise ValueError("has_import is None")

        if source_package is not None:
            self.source_package = source_package
        else:
            raise ValueError("source_package is None")

        if target_package is not None:
            self.target_package = target_package
        else:
            raise ValueError("target_package is None")

        self.need_import = False
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    # Exit a parse tree produced by JavaParserLabeled#importDeclaration.
    def exitImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        if ctx.qualifiedName().getText() != self.source_package + '.' + self.class_identifier:
            return

        start_index = ctx.start.tokenIndex
        stop_index = ctx.stop.tokenIndex

        text_to_replace = "import " + self.target_package + '.' + self.class_identifier + ';'
        if ctx.STATIC() is not None:
            text_to_replace = text_to_replace.replace("import", "import static")

        # replace the import source package with target package
        self.token_stream_rewriter.replace(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            from_idx=start_index,
            to_idx=stop_index,
            text=text_to_replace
        )

    # Exit a parse tree produced by JavaParserLabeled#classOrInterfaceType.
    def exitClassOrInterfaceType(self, ctx: JavaParserLabeled.ClassOrInterfaceTypeContext):
        if not self.has_import or not self.need_import:
            if self.class_identifier in ctx.getText().split('.'):
                self.need_import = True

    # Exit a parse tree produced by JavaParserLabeled#createdName0.
    def exitCreatedName0(self, ctx: JavaParserLabeled.CreatedName0Context):
        if not self.has_import or not self.need_import:
            if self.class_identifier in ctx.getText().split('.'):
                self.need_import = True

    # Exit a parse tree produced by JavaParserLabeled#expression1.
    def exitExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        if not self.has_import or not self.need_import:
            if ctx.expression().getText == self.class_identifier:
                self.need_import = True

    # Exit a parse tree produced by JavaParserLabeled#typeDeclaration.
    def exitTypeDeclaration(self, ctx: JavaParserLabeled.TypeDeclarationContext):
        if ctx.classDeclaration() is not None:
            if not self.has_import or self.need_import:
                index = ctx.start.tokenIndex

                # delete class declaration from source class
                self.token_stream_rewriter.insertBefore(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    index=index,
                    text="import " + self.target_package + '.' + self.class_identifier + ';' + self.NEW_LINE
                )





filename = 'Color.java'
class_identifier = 'Color'
source_package = 'test_package'
target_package = 'new_package'

f_iteration_flag = False
directory = '/home/ali/Desktop/code/TestProject/src/'
file_counter = 0


def main(args):
    global f_iteration_flag

    # Step 1: Load input source into stream
    stream = FileStream(args.file, encoding='utf8')
    # Step 2: Create an instance of AssignmentStLexer
    lexer = JavaLexer(stream)
    # Step 3: Convert the input source into a list of tokens
    token_stream = CommonTokenStream(lexer)
    # Step 4: Create an instance of the AssignmentStParser
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    # Step 5: Create parse tree
    parse_tree = parser.compilationUnit()
    # Step 6: Create an instance of AssignmentStListener
    if f_iteration_flag:
        my_listener = MoveClassRefactoringListener(
            common_token_stream=token_stream, source_package=source_package, target_package=target_package,
            class_identifier=class_identifier, filename=args.file, dirname=directory
        )
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)

        with open(args.file, mode='w', newline='') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText().replace("\r", ""))

    else:
        has_import = False
        has_exact_import = False

        file_to_check = open(file=args.file, mode='r')
        for line in file_to_check.readlines():
            text_line = line.replace('\n', '').replace('\r', '').strip()
            if text_line.startswith('import') and text_line.endswith(source_package + '.' + class_identifier + ';'):
                has_import = True
                break
            if text_line.startswith('import') and text_line.endswith(target_package + '.' + class_identifier + ';'):
                has_exact_import = True
                break

        if not has_exact_import:
            print(f"Start checking file \"{file_to_check.name}\" *** {file_counter}/100")

            my_listener = ReplaceDependentObjectsListener(
                common_token_stream=token_stream, source_package=source_package, target_package=target_package,
                class_identifier=class_identifier, filename=args.file, has_import=has_import
            )
            walker = ParseTreeWalker()
            walker.walk(t=parse_tree, listener=my_listener)

            with open(args.file, mode='w', newline='') as f:
                f.write(my_listener.token_stream_rewriter.getDefaultText().replace("\r", ""))

            print(f"Finish checking file \"{file_to_check.name}\" *** {file_counter}/100")


def recursive_walk(dir):
    global f_iteration_flag, filename
    f_iteration_flag = True

    filename_without_extension, extension = os.path.splitext(filename)
    if extension == '.java':
        process_file("{}/{}".format(dir + '/' + source_package.replace('.', '/'), filename))
    else:
        raise ValueError(f"The filename format must be \".java\", but found {extension}!")

    f_iteration_flag = False

    for dirname, dirs, files in os.walk(dir):
        for file in files:
            if file == filename or file == class_identifier + '.java':
                continue
            file_without_extension, extension = os.path.splitext(file)
            if extension == '.java':
                process_file("{}/{}".format(dirname, file))


def process_file(file):
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help='Input source', default=file)

    args = argparser.parse_args()
    main(args)


if __name__ == '__main__':
    if not os.path.exists(directory + '/' + source_package.replace('.', '/')):
        raise NotADirectoryError(f"The package \"{source_package}\" NOT FOUND!")

    if not os.path.exists(directory + '/' + target_package.replace('.', '/')):
        raise NotADirectoryError(f"The package \"{target_package}\" NOT FOUND!")

    if not os.path.isfile(directory + '/' + source_package.replace('.', '/') + '/' + filename):
        raise FileNotFoundError(f"The file \"{filename}\" NOT FOUND in package {source_package}!")

    if os.path.isfile(directory + '/' + target_package.replace('.', '/') + '/' + class_identifier + '.java'):
        print(f"[Redundant]: doesn't need to refactor")
        print(f"The class \"{class_identifier}\" already exists in package \"{target_package}\"!")
        exit(0)

    recursive_walk(directory)
