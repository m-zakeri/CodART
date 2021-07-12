"""
## Introduction

Moving a class in a file from source package to target package

## Pre and Post Conditions

### Pre Conditions:
1. The moving class should be independent from any other classes in the same file. eg. Consider
   moving class "A" from file "A.java" in "source" package to "target" package. If class "A" is
   dependent on class "B" in the same file("A.java"), then move class refactoring is not allowed.

2. The moving class should be public

3. The moving class should not exist in the target package. eg. Consider moving class "A" from
   file "A.java" in "source" package to "target" package. If "target" package includes a file
   name "A.java", the move class refactoring will not occur.

### Post Conditions:
1. After moving the class to the target package, the import declarations across the project must
   be refactored. eg. If we have used "A" class in a "test.java" file, the import declaration
   before moving class is "import source.A;". After moving the class, the import declaration changes
   to "import target.A;"

"""

import argparse
import os

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


def log_error(title, message):
    """
    log_error method is used for logging erros
    :param title: title of the error
    :param message: message of the error
    :return: None
    """
    if title == "Redundant":
        print(f"[{title}]: Refactoring is not necessary")
    else:
        print(f"[{title}]: Refactoring is not allowed")
    print(f"{message}")


class MoveClassPreConditionListener(JavaParserLabeledListener):
    def __init__(self):
        # Move all classes of a file into file_classes list
        self.file_classes = []

    """
    MoveClassPreConditionListener class is used to check the pre-conditions on 
    move class refactoring
    """

    # Enter a parse tree produced by CompilationUnitContext
    def enterCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        for declaration in ctx.children:
            if isinstance(declaration, JavaParserLabeled.TypeDeclarationContext):
                if declaration.classDeclaration() is None:
                    continue
                self.file_classes.append(declaration.classDeclaration().IDENTIFIER().getText())

    # Exit a parse tree produced by FieldDeclarationContext
    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if ctx.typeType() is None:
            return

        field_type = ctx.typeType().getText()
        if field_type in self.file_classes:
            log_error("Forbidden", "This class has fields that dependent on other classes")
            exit(0)

    # Exit a parse tree produced by Expression0Context
    def exitExpression0(self, ctx: JavaParserLabeled.Expression0Context):
        if ctx.primary() is None:
            return

        expression = ctx.primary().getText()
        if expression in self.file_classes:
            log_error("Forbidden", "This class has dependencies on other classes")
            exit(0)

    # Exit a parse tree produced by LocalVariableDeclarationContext
    def exitLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        if ctx.typeType() is None:
            return

        local_variable_type = ctx.typeType().getText()
        if local_variable_type in self.file_classes:
            log_error("Forbidden", "This class has local variables that dependent on other classes")
            exit(0)


class MoveClassRefactoringListener(JavaParserLabeledListener):
    """
    To implement the move class refactoring
    a stream of tokens is sent to the listener, to build an object token_stream_rewriter
    and we move all class methods and fields from the source package to the target package
    """

    def __init__(self, common_token_stream: CommonTokenStream = None, class_identifier: str = None,
                 source_package: str = None, target_package: str = None, filename: str = None, dirname: str = None):
        """
        :param common_token_stream: used to edit the content of the parsers
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
        self.mul_imports = []
        self.exact_imports = []

    # Enter a parse tree produced by CompilationUnitContext
    def enterCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        # Iterate over the declarations of context to save all import statements
        # in exact_imports and mul_imports
        for declaration in ctx.children:
            if isinstance(declaration, JavaParserLabeled.ImportDeclarationContext):
                imported_package = ""
                mul = None
                if declaration.qualifiedName() is not None:
                    imported_package += declaration.qualifiedName().getText()
                if declaration.MUL() is not None:
                    mul = declaration.MUL().getText()
                    imported_package += ".*"

                if mul is not None:
                    self.mul_imports.append(imported_package)
                else:
                    self.exact_imports.append(imported_package)

    # Exit a parse tree produced by JavaParserLabeled#importDeclaration.
    def exitImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        # extract the imported package from context
        imported_package = ""
        mul = None
        if ctx.qualifiedName() is not None:
            imported_package += ctx.qualifiedName().getText()
        if ctx.MUL() is not None:
            mul = ctx.MUL().getText()
            imported_package += '.' + ctx.MUL().getText()

        # return if the current import statement is not relevant to source package
        if self.source_package not in imported_package or (self.class_identifier not in imported_package and '*' not in imported_package):
            return

        start_index = ctx.start.tokenIndex
        stop_index = ctx.stop.tokenIndex

        target_exact_package = f"{self.target_package}.{self.class_identifier}"
        target_exact_import = f"import {target_exact_package};"

        if ctx.STATIC() is not None:
            target_exact_import = target_exact_import.replace("import", "import ")

        # handle import scenarios in files dependent on the moved class
        if target_exact_package in self.exact_imports:
            if mul is None:
                self.token_stream_rewriter.delete(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=start_index,
                    to_idx=stop_index + 1
                )
        else:
            if mul is not None:
                self.token_stream_rewriter.insertAfter(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    index=stop_index,
                    text=self.NEW_LINE + target_exact_import
                )
            else:
                print(ctx.getText())
                self.token_stream_rewriter.replace(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=start_index,
                    to_idx=stop_index,
                    text=target_exact_import
                )
            self.exact_imports.append(target_exact_package)

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

                # return if the file has already imported the package
                if (self.source_package + '.' + self.class_identifier not in self.exact_imports) \
                        or (self.target_package + '.' + self.class_identifier in self.exact_imports):
                    return

                # delete class declaration from source class
                self.token_stream_rewriter.insertBefore(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    index=index,
                    text="import " + self.target_package + '.' + self.class_identifier + ';' + self.NEW_LINE
                )


filename = 'MoveClass.java'
class_identifier = 'MoveClass'
source_package = 'source_package'
target_package = 'target_package'
directory = '/home/ali/Desktop/JavaTestProject/src/'
file_counter = 0


def move_class(token_stream, parse_tree, args):
    """
    move_class method uses MoveClassRefactorListener to move the class to the target package
    :param token_stream: common token stream
    :param parse_tree: generated parse tree
    :param args: file arguments
    :return: None
    """
    move_class_listener = MoveClassRefactoringListener(
        common_token_stream=token_stream, source_package=source_package, target_package=target_package,
        class_identifier=class_identifier, filename=args.file, dirname=directory
    )
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=move_class_listener)

    with open(args.file, mode='w', newline='') as f:
        f.write(move_class_listener.token_stream_rewriter.getDefaultText().replace("\r", ""))


def post_move_class_propagation(token_stream, parse_tree, args):
    """
    post_move_class_propagation method is used to propagate post-conditions after moving the class
    :param token_stream: common token stream
    :param parse_tree: generated parse tree
    :param args: file arguments
    :return: None
    """
    has_import = False
    has_exact_import = False

    file_to_check = open(file=args.file, mode='r')
    for line in file_to_check.readlines():
        text_line = line.replace('\n', '').replace('\r', '').strip()
        if (text_line.startswith('import') and text_line.endswith(source_package + '.' + class_identifier + ';')) \
                or (text_line.startswith('import') and text_line.endswith(source_package + '.*;')):
            has_import = True
            break
        if (text_line.startswith('import') and text_line.endswith(target_package + '.' + class_identifier + ';')) \
                or (text_line.startswith('import') and text_line.endswith(target_package + '.*;')):
            has_exact_import = True
            break

    if not has_exact_import:
        print(f"Start checking file \"{file_to_check.name}\" *** {file_counter}/100")

        replace_dependent_object_listener = ReplaceDependentObjectsListener(
            common_token_stream=token_stream, source_package=source_package, target_package=target_package,
            class_identifier=class_identifier, filename=args.file, has_import=has_import
        )
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=replace_dependent_object_listener)

        with open(args.file, mode='w', newline='') as f:
            f.write(replace_dependent_object_listener.token_stream_rewriter.getDefaultText().replace("\r", ""))

        print(f"Finish checking file \"{file_to_check.name}\" *** {file_counter}/100")


def get_argument_parser(file):
    """
    get_argument_parser method used to parse the arguments
    :param file: file name
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-n', '--file',
        help='Input source', default=file)

    args = arg_parser.parse_args()
    return args


def get_parse_tree_token_stream(args):
    """
    returns parse tree and token stream base on the file stream
    :param args: file arguments
    """

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

    return parse_tree, token_stream


def recursive_walk(dir_path):
    """
    walks through the specified directory files to implement refactoring
    :param dir_path: directory path
    """
    global filename
    args = get_argument_parser(source_file_path)
    parse_tree, token_stream = get_parse_tree_token_stream(args)

    # check if the class has dependencies on other classes in the same class
    pre_condition_listener = MoveClassPreConditionListener()
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=pre_condition_listener)

    filename_without_extension, extension = os.path.splitext(filename)
    if extension == '.java':
        move_class(token_stream, parse_tree, args)
    else:
        raise ValueError(f"The filename format must be \".java\", but found {extension}!")

    for dirname, dirs, files in os.walk(dir_path):
        for file in files:
            if file == filename or file == class_identifier + '.java':
                continue
            file_without_extension, extension = os.path.splitext(file)
            if extension == '.java':
                args = get_argument_parser(os.path.join(dirname, file))
                parse_tree, token_stream = get_parse_tree_token_stream(args)
                post_move_class_propagation(token_stream, parse_tree, args)


if __name__ == '__main__':
    source_package_directory = os.path.join(directory, source_package.replace('.', '/'))
    target_package_directory = os.path.join(directory, target_package.replace('.', '/'))
    source_file_path = os.path.join(source_package_directory, filename)
    target_file_path = os.path.join(target_package_directory, f"{class_identifier}.java")

    if not os.path.exists(source_package_directory):
        raise NotADirectoryError(f"The package \"{source_package}\" NOT FOUND!")

    if not os.path.exists(target_package_directory):
        raise NotADirectoryError(f"The package \"{target_package}\" NOT FOUND!")

    if not os.path.isfile(source_file_path):
        raise FileNotFoundError(f"The file \"{filename}\" NOT FOUND in package {source_package}!")

    if os.path.isfile(target_file_path):
        log_error("Redundant", f"The class \"{class_identifier}\" already exists in package \"{target_package}\"!")
        exit(0)

    # start refactoring
    recursive_walk(directory)
