from antlr4 import *
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

"""
    An Extraction method refactoring class for using compiler listeners 
    Authors: Mohammad Sajad Naghizadeh, Sadegh Jafari, Sina Ziaee
    
    Description about the code:
    - statements are each line of code showing an act for example a = 5; is an statement.
    - exact each method of each class.
"""

"""
    Conf object help:
        1.if package is not important or is unknown enter None for its value.
        2.lines are calculated from beginning of method you are willing to extract counting from 0.
"""


def is_equivalent(a, b):
    if str(a) == str(b):
        return True
    return False


"""
    Extract method factoring class extending java parser labeled listener
"""


class ExtractMethodRefactoring(JavaParserLabeledListener):

    def __init__(self,
                 target_package: str = None, target_class: str = None,
                 target_method: str = None, lines=None):
        # TODO add target method None possibility

        # checks Target method not to be None
        if lines is None:
            raise Exception('Extract lines are not specified.')
        if target_method is None:
            raise Exception('Target method should be specified.')

        # checks lines not to be Empty
        if len(lines) == 0:
            raise Exception('lines list should not be empty.')

        # getting targets
        self.target_package = target_package
        self.target_class = target_class
        self.target_method = target_method

        # tree helper variables
        self.is_in_target_package = self.target_package is None
        self.is_in_target_class = False
        self.is_in_a_method = False
        self.is_in_target_method = False
        self.used_variables = set([])
        self.lines = lines
        # self.extract_lines = set([])
        self.remain_lines = set([])
        self.variable_info = {'class': self.target_class, 'method': self.target_method, 'variables': {}}
        self.method_start_line = 0
        self.method_stop_line = 0
        self.is_inside_rule = None

    ######################################
    # Overriding required methods to satisfy our extraction requirements
    ######################################

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        if self.target_package is None or is_equivalent(ctx.qualifiedName().getText(), self.target_package):
            self.is_in_target_package = True

    # def exitPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
    #     if self.target_package is None or is_equivalent(ctx.qualifiedName().getText(), self.target_package):
    #         self.is_in_target_package = False
    #         # todo: do code smell removal in phase 2

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_in_target_package and self.target_class is None or is_equivalent(ctx.IDENTIFIER(),
                                                                                    self.target_class):
            self.is_in_target_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_in_target_package and self.target_class is None or is_equivalent(ctx.IDENTIFIER(),
                                                                                    self.target_class):
            self.is_in_target_class = False
            # todo: do code smell removal in phase 2

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        # checking if current method is the target method
        if self.is_in_target_package and self.is_in_target_class and is_equivalent(ctx.IDENTIFIER(),
                                                                                   self.target_method):
            self.is_in_target_method = True
            self.method_start_line = ctx.start.line
            new_lines = []
            for line in self.lines:
                new_lines.append(line + self.method_start_line)
            self.lines = new_lines
            self.method_stop_line = ctx.stop.line

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.is_in_a_method = False
        if self.is_in_target_package and self.is_in_target_class and self.is_in_target_method:
            self.is_in_target_method = False
        # todo: do code smell removal in phase 2

    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        # print('dec detected')
        if self.is_in_target_method:
            # print('inside target with :', ctx.getText())
            if set(range(ctx.start.line, ctx.stop.line + 1)).issubset(set(self.lines)):
                # print('dec in extract lines')
                self.remain_lines = self.remain_lines.union(range(ctx.start.line, ctx.stop.line + 1))
                # self.extract_lines =
                # print('new remain lines :', self.remain_lines)
            elif not ctx.start.line > max(self.lines):
                # print('dec not in extract lines')
                self.variable_info['variables'][ctx.variableDeclarators().variableDeclarator()[
                    0].variableDeclaratorId().getText()] = ctx.typeType().getText()
                # print('new variables :', self.variable_info)

    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        if self.is_in_target_method:
            self.variable_info['variables'][ctx.variableDeclaratorId().getText()] = ctx.typeType().getText()

    def enterEveryRule(self, ctx: ParserRuleContext):
        if self.is_in_target_method:
            # print('for rule',ctx.getText())
            # print(set(range(ctx.start.line, ctx.stop.line + 1)),'&',set(self.lines))
            if set(range(ctx.start.line, ctx.stop.line + 1)) & set(self.lines):
                if not set(self.lines).issubset(set(range(ctx.start.line, ctx.stop.line + 1))) and not set(
                        range(ctx.start.line, ctx.stop.line + 1)).issubset(self.lines):
                    raise Exception('input lines contains some part of a command,not the entire command!')
            if self.is_inside_rule is None:
                if set(range(ctx.start.line, ctx.stop.line + 1)).issubset(set(self.lines)):
                    # self.extract_lines = self.extract_lines.union(range(ctx.start.line, ctx.stop.line + 1))
                    # print(ctx.getText())
                    self.is_inside_rule = ctx
                    # self.stack.append(ctx)
            # else:
            #     self.stack.append(ctx)

    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        if self.is_inside_rule is not None:
            if self.variable_info['variables'].keys().__contains__(str(ctx.IDENTIFIER())):
                self.used_variables.add(str(ctx.IDENTIFIER()))

    def exitEveryRule(self, ctx: ParserRuleContext):
        if self.is_inside_rule is not None and self.is_inside_rule == ctx:
            self.is_inside_rule = None


# helper functions
def get_args(variables):
    # print(variables)
    result = '('
    first = True
    for item in variables:
        if not first:
            result += ', '
        else:
            first = False
        result += item
    result += ');\n'
    return result


def get_args_with_type(variables, all_variables):
    result = '('
    first = True
    for item in variables:
        if not first:
            result += ', '
        else:
            first = False
        result += all_variables[item] + ' ' + item
    result += ')'
    return result


# extract method function
def extract_method(conf):
    stream = FileStream(conf['target_file'])
    lexer = JavaLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    tree = parser.compilationUnit()
    # TODO : too many params for ExtractMethodRefactoring constructor
    listener = ExtractMethodRefactoring(conf['target_package'], conf['target_class'], conf['target_method'],
                                        conf['lines'])
    walker = ParseTreeWalker()
    walker.walk(
        listener=listener,
        t=tree
    )
    # print(parser.getTokenStream())
    # print(listener.variable_info)

    output = []
    file1 = open(conf['target_file'], 'r')
    lines = file1.readlines()
    line_num = 1
    # func_added = False
    func = []
    print('extracting following lines:')
    for line in lines:
        if listener.lines.__contains__(line_num):
            print(line, end='')
            if line_num == min(listener.lines):
                output.append('\t\t' + conf['new_method_name'] + get_args(listener.used_variables))
            if listener.remain_lines.__contains__(line_num):
                output.append(line)
            func.append(line)
        elif line_num == listener.method_stop_line:
            output.append(line)
            output.append('\tpublic void ' + conf['new_method_name'] + get_args_with_type(listener.used_variables,
                                                                                          listener.variable_info[
                                                                                              'variables']) + '\n')
            output.append('\t{\n')
            output = output + func
            output.append('\t}\n')
        else:
            output.append(line)
        line_num += 1
    file1.close()
    print('--------------------')

    file2 = open(conf['output_file'], 'w')
    for item in output:
        file2.write(item)
    file2.close()


"""
    driver method
"""


def main():
    print("Started Extract Method")
    _conf = {
        'target_package': None,
        'target_file': "/home/ali/Desktop/JavaTestProject/src/ExtractMethod.java",
        'output_file': "/home/ali/Desktop/JavaTestProject/src/ExtractMethod.java",
        'target_class': 'ExtractMethod',
        'target_method': 'printOwing',
        'lines': [3, 4, 5, ],
        'new_method_name': 'printDetails',
    }
    extract_method(_conf)

    print("Finished Extract Method")


if __name__ == '__main__':
    main()

    # todo: remember in java we need the name of static classes to be exactly the same as file name
    # todo: remember in java we need static variables to only be used in static method
