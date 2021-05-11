"""
This class is for extracting kind of methods from a class that are duplicated.
You can read more about this kind of refactoring in https://refactoring.guru/extract-method

Authors: Arman Heydari, M.Amin Ghasvari
"""

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


def is_equal(a, b):
    """
    Check equality for strings
    :param a: the first object
    :param b: the second object
    :return: boolean that is true if they were equal
    """
    return str(a) == str(b)


class Statement:
    """
    Each line of code in the methods is a statement.
    """

    def __init__(self, statement, expressions):
        self.statement = statement
        self.expressions = expressions

    def __str__(self):
        """
        For logging the statements
        :return: a string of statements
        """
        return "[\n\tstatement: {}\n\texpressions: {}\n]".format(
            self.statement.getText(),
            list(map(lambda x: x.getText(), self.expressions))
        )


class DuplicationRefactoring:
    """
    The refactor method can refactor the duplication by an instance of
    this class.
    There is a duplication attribute that shows all of duplications. They
    are all instances of Duplication class.
    """

    class Duplication:
        """
        Duplication class represent a bunch of duplicate statements.
        By creating new object from this class, it will calculate the
        starting index and ending index of the duplicate statements.
        """

        def __init__(self, statements):
            self.statements = statements
            self.from_line = statements[0].statement.start.line
            self.to_line = statements[-1].statement.stop.line

    def __init__(self, list_of_statements):
        duplications = []
        for statements in list_of_statements:
            duplications.append(DuplicationRefactoring.Duplication(statements))
        self.duplications = duplications


class ExtractMethodRefactoring(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, class_name: str = "Main",
                 new_method_name: str = "newMethod"):
        """
        :param common_token_stream:
        :param class_name: the name of the class that duplications should be considered
        :param new_method_name: the name of the new method that contains that statements
        """
        self.refactor_class_name = class_name
        self.new_method_name = new_method_name

        # make a copy of the tokens
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_re_writer = TokenStreamRewriter(common_token_stream)

        self.method_statements = {}  # dictionary that maps the methods to its statements

        # tree helper variables
        self.is_in_target_class = False
        self.is_in_a_method = False
        self.current_method_name = ""

        # refactoring
        self.duplicates = None  # if it is None, then we don't have any duplications

    ######################################
    # Collect statements from parse tree
    ######################################

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if is_equal(ctx.IDENTIFIER(), self.refactor_class_name):
            self.is_in_target_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if is_equal(ctx.IDENTIFIER(), self.refactor_class_name):
            self.is_in_target_class = False
            self.find_duplicates()
            if self.duplicates is not None:
                self.refactor(ctx)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_in_target_class:
            self.is_in_a_method = True
            self.current_method_name = ctx.IDENTIFIER()
            self.method_statements[self.current_method_name] = []

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.is_in_a_method = False

    def enterStatement15(self, ctx: JavaParserLabeled.Statement0Context):
        if self.is_in_target_class:
            if self.is_in_a_method:
                self.method_statements[self.current_method_name].append(
                    Statement(ctx, [])
                )

    def log_statements_of_methods(self):
        """
        It will print out statements of each method for the class.
        :return:
        """
        for method_name in self.method_statements.keys():
            print(method_name)
            statements = self.method_statements[method_name]
            for statement in statements:
                print(str(statement))
            print("---------------")

    ##########################
    # Searching Duplications
    ##########################

    @staticmethod
    def get_duplicate_continues_statements(a_statements, b_statements):
        """
        Find duplicate statements between two arrays of statements.
        :param a_statements: the first list of statements
        :param b_statements:  the second list of statements
        :return: (k, i, j) that k represent number of duplicated statements,
        and i, j are the list of the statements. The length of each of them is k.
        return could be None if there was not any duplications.
        There might be lots of duplications, but it would return the one that
        has the most duplicated statements.
        """
        len_a_statement = len(a_statements)
        len_b_statement = len(b_statements)

        # for any methods like such as getters or setters that have few number of
        # statements, we should return None.
        if len_b_statement <= 1 or len_a_statement <= 1:
            return None

        # diagnose exact duplications
        method_a_b_duplications = []
        i = 0
        while i < len_a_statement:
            j = 0
            while j < len_b_statement:
                sa = a_statements[i]
                sb = b_statements[j]
                count_duplicate_statement = 0
                a_duplicates = []
                b_duplicates = []
                k = 0
                while is_equal(sa.statement.getText(), sb.statement.getText()) \
                        and i + k < len_a_statement and j + k < len_b_statement:
                    sa = a_statements[i + k]
                    sb = b_statements[j + k]
                    count_duplicate_statement += 1
                    a_duplicates.append(sa)
                    b_duplicates.append(sb)
                    k += 1
                if count_duplicate_statement != 0:
                    method_a_b_duplications.append((count_duplicate_statement, a_duplicates, b_duplicates))
                j += 1
            i += 1

        # calculate the maximum based on the number of duplications
        max_duplicate = max(method_a_b_duplications, key=lambda x: x[0])
        return max_duplicate

    @staticmethod
    def log_duplication(duplicate, i, j, methods):
        """
        It will show you a report about the a duplications.
        :param duplicate: is a tuple that (k, i, j): k is the number of duplications,
        and i, j are the statements.
        :param i: index of the first method
        :param j: index of the second method
        :param methods: a list of methods that are existed in the class.
        :return:
        """
        print()
        print("lines {}-{} in {} and lines {}-{} {} are duplicated. count: {}\n".format(
            duplicate[1][0].statement.start.line, duplicate[1][-1].statement.start.line,
            methods[i].getText(), duplicate[2][0].statement.start.line,
            duplicate[2][-1].statement.start.line, methods[j].getText(), duplicate[0]),
            list(map(lambda x: x.statement.getText(), duplicate[1])))

    def find_duplicates(self):
        """
        This method is responsible for choosing duplication and
        set it to self.duplicates. It will find the maximum lines of
        duplication, and search through all of the methods.
        This method compare each one of those methods using
        self.get_duplicate_continues_statements method.
        :return:
        """

        # it is for representing the statements of each method
        # self.log_statements_of_methods()

        # Compare each one of methods with the other methods
        methods = list(self.method_statements.keys())
        len_method = len(methods)
        i = 0
        duplicates = {"statements": [], "lines": [], "text": ""}
        while i < len_method - 1:
            j = i + 1
            while j < len_method:
                duplicate = self.get_duplicate_continues_statements(
                    self.method_statements[methods[i]],
                    self.method_statements[methods[j]]
                )

                # return value is None when not any duplications have been found.
                if duplicate is not None:
                    self.log_duplication(duplicate, i, j, methods)
                    if len(duplicates["statements"]) == 0:
                        duplicates["statements"].append(duplicate[1])
                        duplicates["lines"].append(duplicate[1][0].statement.start.line)
                        for d in duplicate[1]:
                            duplicates["text"] += d.statement.getText()

                    for i in range(1, 3):
                        if duplicate[i][0].statement.start.line not in duplicates["lines"]:
                            temp = ""
                            for d in duplicate[i]:
                                temp += d.statement.getText()
                            if temp == duplicates["text"]:
                                duplicates["statements"].append(duplicate[i])

                j += 1
            i += 1
        self.duplicates = DuplicationRefactoring(duplicates["statements"])

    ###############
    # Refactoring
    # Refactoring is in 2 step.
    # First: Creating a new method at the end of the class.
    # Second: Deleting the duplications and replacing with new method.
    ###############

    def create_new_method(self, start_index):
        """
        It creates a new method based on the given name to avoid duplication.
        :param start_index: the index of token.
        :return:
        """
        new_method = "\n"
        new_method += "\tpublic void " + self.new_method_name + "() {\n"
        for statement_obj in self.duplicates.duplications[0].statements:
            new_method += "\t\t{}\n".format(statement_obj.statement.getText())
        new_method += "\t}\n"
        new_method += "\n"

        self.token_stream_re_writer.insertAfter(start_index, new_method)

    def replace_duplicate_code(self):
        """
        Replaces all of the duplications with new method.
        :return:
        """
        self.duplicates.duplications.sort(key=lambda x: x.to_line, reverse=True)
        for duplicate in self.duplicates.duplications:
            start_index = duplicate.statements[0].statement.start.tokenIndex
            end_index = duplicate.statements[-1].statement.stop.tokenIndex
            self.token_stream_re_writer.replaceRange(start_index, end_index, "{}();".format(self.new_method_name))
        print(self.token_stream_re_writer.getDefaultText())

    def refactor(self, ctx):
        """
        Main method for refactoring.
        :param ctx:
        :return:
        """
        self.create_new_method(ctx.stop.tokenIndex - 1)
        self.replace_duplicate_code()


if __name__ == "__main__":
    input_file = r"C:\Users\Amin\MAG\_term_6\CodART\tests\extract_method\input_file4.java"
    output_file = r"C:\Users\Amin\MAG\_term_6\CodART\tests\extract_method\output_file4.java"

    stream = FileStream(input_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = ExtractMethodRefactoring(common_token_stream=token_stream, class_name="Student",
                                           new_method_name="printStudent")
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(output_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_re_writer.getDefaultText())
