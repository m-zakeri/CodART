"""
This class is for extracting kind of methods from a class that are duplicated.
You can read more about this kind of refactoring in https://refactoring.guru/extract-method

Authors: Arman Heydari, M.Amin Ghasvari

Description about the code:
- statements are each line of code showing an act for example this.x = 3 is an statement.
- exact duplications are the ones that have completely the same code.
- semi duplications are the ones that by using a variable we can make a new method and
avoid duplications.
"""
import os
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled, Token

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


def is_equal(a, b):
    """
    Check equality for strings
    :param a: the first object
    :param b: the second object
    :return: boolean that is true if they were equal
    """
    return str(a) == str(b)


class VariableTypes:
    """
    this class is to recognize the type of variable based on its token
    """
    DECIMAL_LITERAL = 51
    HEX_LITERAL = 52
    OCT_LITERAL = 53
    BINARY_LITERAL = 54
    FLOAT_LITERAL = 55
    HEX_FLOAT_LITERAL = 56
    BOOL_LITERAL = 57
    CHAR_LITERAL = 58
    STRING_LITERAL = 59
    MAP_TYPE = {
        DECIMAL_LITERAL: "int",
        HEX_LITERAL: "",
        OCT_LITERAL: "",
        BINARY_LITERAL: "boolean",
        FLOAT_LITERAL: "float",
        HEX_FLOAT_LITERAL: "float",
        BOOL_LITERAL: "boolean",
        CHAR_LITERAL: "char",
        STRING_LITERAL: "String",
    }


class Statement:
    """
    Each line of code in the methods is a statement.
    """

    def __init__(self, statement, expressions):
        self.statement = statement
        self.expressions = expressions
        self.variables = []  # variables are going to be used in semi duplications

    def copy(self):
        s = Statement(self.statement, self.expressions)
        s.variables = self.variables.copy()
        return s

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
        self.common_token_stream = common_token_stream
        self.tokens = common_token_stream.tokens
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
            # print(self.duplicates.duplications[0].statements[0].statement.getText())
            if self.duplicates is not None and len(self.duplicates.duplications) > 0:
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

    def check_semi_duplicate(self, sa, sb, k):
        """
        It checks if the statements are similar or not. Two statements are similar if
        we can omit duplicated code with adding new method that has some arguments
        :param sa: first statements
        :param sb: second statement
        :param k: the k represent the index of the statements.
        :return:
        """
        fta, ftb = sa.statement.start.tokenIndex, sb.statement.start.tokenIndex
        tta, ttb = sa.statement.stop.tokenIndex, sb.statement.stop.tokenIndex

        if tta - fta != ttb - ftb:
            return False, sa, sb

        count = 0

        m = min(tta - fta, ttb - ftb)
        for i in range(m):
            txt_token_a = self.tokens[fta + i].text
            txt_token_b = self.tokens[ftb + i].text
            if txt_token_a != txt_token_b:
                if self.tokens[fta + i].type != self.tokens[ftb + i].type:
                    return False, sa, sb
                else:
                    history_a = list(map(lambda x: x[2], sa.variables))
                    history_b = list(map(lambda x: x[2], sb.variables))
                    count += 1
                    if txt_token_a not in history_a:
                        sa.variables.append(
                            (self.tokens[fta + i].type,
                             "variable{}Number{}{}".format(self.tokens[fta + i].type, k, count), txt_token_a))
                    if txt_token_b not in history_b:
                        sb.variables.append(
                            (self.tokens[ftb + i].type,
                             "variable{}Number{}{}".format(self.tokens[ftb + i].type, k, count), txt_token_b))

        return True, sa, sb

    def get_duplicate_continues_statements(self, a_statements, b_statements):
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
                    method_a_b_duplications.append(
                        (count_duplicate_statement, a_duplicates.copy(), b_duplicates.copy()))
                j += 1
            i += 1

        # calculate the maximum based on the number of duplications
        max_exact_duplicate = None
        if len(method_a_b_duplications) > 1:
            max_exact_duplicate = max(method_a_b_duplications, key=lambda x: x[0])

        # diagnose semi duplications
        # here we search for duplications that can be avoided by passing variable
        method_a_b_semi_duplications = []
        i = 0
        while i < len_a_statement:
            j = 0
            while j < len_b_statement:
                count_duplicate_statement = 0
                a_duplicates = []
                b_duplicates = []
                k = 0
                while i + k < len_a_statement and j + k < len_b_statement:
                    sa = a_statements.copy()[i + k]
                    sb = b_statements.copy()[j + k]
                    if is_equal(sa.statement.getText(), sb.statement.getText()):
                        count_duplicate_statement += 1
                    else:
                        is_semi, sa, sb = self.check_semi_duplicate(sa.copy(), sb.copy(), k)
                        if not is_semi:
                            break
                        count_duplicate_statement += 1
                    a_duplicates.append(sa.copy())
                    b_duplicates.append(sb.copy())
                    k += 1
                if count_duplicate_statement != 0:
                    method_a_b_semi_duplications.append(
                        (count_duplicate_statement, a_duplicates.copy(), b_duplicates.copy()))
                j += 1
            i += 1

        # calculate the maximum based on the number of duplications
        max_semi_duplicate = None
        if len(method_a_b_semi_duplications) > 1:
            max_semi_duplicate = max(method_a_b_semi_duplications, key=lambda x: x[0])

        return max(max_exact_duplicate, max_semi_duplicate, key=lambda x: x[0])

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
        duplicates = {"statements": [], "lines": [], "text": "", "variables": []}
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
                        duplicates["variables"] = duplicate[1]
                        duplicates["lines"].append(duplicate[1][0].statement.start.line)
                        for d in duplicate[1]:
                            duplicates["text"] += d.statement.getText()

                    # here we check how many duplications have been occurred.
                    # trying to find out similar duplications to change them all together.
                    for i in range(1, 3):
                        print(duplicate[i][0].statement.start.line)
                        if duplicate[i][0].statement.start.line not in duplicates["lines"]:
                            temp = ""
                            for d in duplicate[i]:
                                temp += d.statement.getText()
                            if temp == duplicates["text"]:
                                duplicates["statements"].append(duplicate[i])
                            else:
                                is_ok = True
                                if len(duplicate[i]) != len(duplicates["statements"][0]):
                                    break
                                else:
                                    for s1 in duplicates["statements"][0]:
                                        for s2 in duplicate[i]:
                                            if len(s1.variables) != len(s2.variables):
                                                is_ok = False
                                                break
                                            else:
                                                for v1 in s1.variables:
                                                    for v2 in s2.variables:
                                                        if v1[0] != v2[0]:
                                                            is_ok = False
                                                            break
                                                    if is_ok:
                                                        duplicates["statements"].append(duplicate[i])
                j += 1
            i += 1
        self.duplicates = DuplicationRefactoring(duplicates["statements"])

    ###############
    # Refactoring
    # Refactoring is in 2 steps.
    # First: Creating a new method at the end of the class.
    # Second: Deleting the duplications and replacing with new method.
    ###############

    def create_new_method(self, start_index):
        """
        It creates a new method based on the given name to avoid duplication.
        :param start_index: the index of token.
        :return:
        """
        # here we are creating the arguments
        d = self.duplicates.duplications[0]
        func_args = []
        for s in d.statements:
            for v in s.variables:
                arg_type = v[0]
                arg_name = v[1]
                try:
                    func_args.append(VariableTypes.MAP_TYPE[arg_type] + " " + arg_name)
                except:
                    pass
        func_args = ", ".join(func_args)

        # adding the new method
        new_method = "\n"
        new_method += "\tpublic void " + self.new_method_name + "(" + func_args + ") {\n"
        k = 0
        for statement_obj in self.duplicates.duplications[0].statements:
            if len(statement_obj.variables) == 0:
                new_method += "\t\t{}\n".format(statement_obj.statement.getText())
            else:
                statement = "\t\t{}\n".format(statement_obj.statement.getText())
                for v in statement_obj.variables:
                    statement = statement.replace(v[2], v[1])
                new_method += statement
            k += 1
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
            # arguments
            variables = []
            for state in duplicate.statements:
                for v in state.variables:
                    variables.append(v)
            variables = list(map(lambda x: x[2], variables))
            # replacing
            start_index = duplicate.statements[0].statement.start.tokenIndex
            end_index = duplicate.statements[-1].statement.stop.tokenIndex
            self.token_stream_re_writer.replaceRange(start_index, end_index,
                                                     "{}({});".format(self.new_method_name, ", ".join(variables)))
        # print(self.token_stream_re_writer.getDefaultText())

    def refactor(self, ctx):
        """
        Main method for refactoring.
        :param ctx:
        :return:
        """
        self.create_new_method(ctx.stop.tokenIndex - 1)
        self.replace_duplicate_code()


if __name__ == "__main__":
    input_directory = r"D:\iust\term 6\compiler\project\CodART\benchmark_projects\JSON\src\main\java\org\json"
    output_directory = os.path.join(input_directory, "extract_method_refactored")
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    for input_file in os.listdir(input_directory):
        if input_file.endswith(".java"):
            stream = FileStream(os.path.join(input_directory, input_file), encoding='utf8')
            lexer = JavaLexer(stream)
            token_stream = CommonTokenStream(lexer)
            parser = JavaParserLabeled(token_stream)
            parser.getTokenStream()
            parse_tree = parser.compilationUnit()
            my_listener = ExtractMethodRefactoring(common_token_stream=token_stream, class_name="Student",
                                                   new_method_name="printStudent")
            walker = ParseTreeWalker()
            walker.walk(t=parse_tree, listener=my_listener)

            output_file = os.path.join(output_directory, input_file)
            with open(output_file, mode='w', newline='') as f:
                f.write(my_listener.token_stream_re_writer.getDefaultText())
        else:
            continue
