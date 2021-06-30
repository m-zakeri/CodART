from antlr4 import *
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
import numpy as np

"""
    An Extraction method refactoring class for using compiler listeners 
    Authors: Mohammad Sajad Naghizadeh, Sadegh Jafari, Sina Ziaee, Mohammad reza babaee
    
    Description about the code:
    - statements are each line of code showing an act for example a = 5; is an statement.
    - exact each method of each class.
"""

"""
    Conf object help:
        -- lines are calculated from beginning the beginning of file starting from 1 .
"""

"""
    limitations : 
        -- extracted lines must be a part of a method or a class constructor any other format simply would not work.(though we don't know java even supports any other format)
"""


def is_equivalent(a, b):
    if str(a) == str(b):
        return True
    return False


"""
    Extract method factoring class extending javaParserLabeledListener
"""


class ExtractMethodRefactoring(JavaParserLabeledListener):

    def __init__(self, lines: list,post_variables : list = []):

        # checks Target method and lines to be valid
        if lines is None or len(lines) == 0:
            raise Exception('target lines are not specified.')

        # setting variables
        self.lines = np.array(lines)
        self.lines.reshape((len(lines), 1))
        self.last_line = self.lines.max()
        self.first_line = self.lines.min()

        # tree helper variables
        self.target_method_found = False
        self.is_in_target_method = False
        # list of variables created and initialized before extracted lines
        self.pre_variables = {}
        # list of variables used after extracted lines
        self.post_variables = post_variables
        self.pre_assign_variable = False
        self.assign_variable_in_extract_lines = False
        self.used_variables = set([])
        self.created_variables = set([])
        self.assigned_variable = None
        self.method_stop_line = 0
        self.exception = None
        self.is_target_method_static=False

    ######################################
    # Overriding required methods to satisfy our extraction requirements
    ######################################

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if ctx.start.line <= self.first_line and ctx.stop.line >= self.last_line:
            self.is_in_target_method = True
            self.target_method_found = True
            for modifier in ctx.parentCtx.parentCtx.modifier():
                if modifier.getText() == 'static':
                    self.is_target_method_static = True
                    break
            if ctx.qualifiedNameList():
                print('ex found :',ctx.qualifiedNameList().getText())
                self.exception = ctx.qualifiedNameList().getText()
            self.method_start_line = ctx.start.line
            self.method_stop_line = ctx.stop.line

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.is_in_target_method = False

    def enterConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):
        if ctx.start.line <= self.first_line and ctx.stop.line >= self.last_line:
            self.is_in_target_method = True
            self.target_method_found = True
            for modifier in ctx.parentCtx.parentCtx.modifier():
                if modifier.getText() == 'static':
                    self.is_target_method_static = True
                    break
            self.method_start_line = ctx.start.line
            self.method_stop_line = ctx.stop.line

    def exitConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):
        self.is_in_target_method = False

    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        if self.is_in_target_method:
            if not set(range(ctx.start.line, ctx.stop.line + 1)).issubset(set(self.lines)):
                if ctx.start.line < self.last_line:
                    for var in ctx.variableDeclarators().variableDeclarator():
                        self.pre_variables[
                            var.variableDeclaratorId().getText()] = {
                            'type': ctx.typeType().getText(),
                            'init': str(var.getText()).__contains__('=')}
            else:
                self.created_variables.add(
                    ctx.variableDeclarators().variableDeclarator()[0].variableDeclaratorId().getText())

    def enterEnhancedForControl(self, ctx:JavaParserLabeled.EnhancedForControlContext):
        if self.is_in_target_method:
            if not set(range(ctx.start.line, ctx.stop.line + 1)).issubset(set(self.lines)):
                if ctx.start.line < self.last_line:
                    var = ctx.variableDeclaratorId()
                    self.pre_variables[
                        var.getText()] = {
                        'type': ctx.typeType().getText(),
                        'init': True}
            else:
                self.created_variables.add(
                    ctx.variableDeclarators().variableDeclarator()[0].variableDeclaratorId().getText())


    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        if self.is_in_target_method:
            self.pre_variables[ctx.variableDeclaratorId().getText()] = {'type': ctx.typeType().getText(), 'init': True}
            # self.variable_info['variables'][ctx.variableDeclaratorId().getText()] = ctx.typeType().getText()

    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        if self.is_in_target_method:
            if not set(range(ctx.start.line, ctx.stop.line + 1)).issubset(
                    set(self.lines)):
                if ctx.start.line < self.last_line:
                    self.pre_assign_variable = True
            else:
                self.assign_variable_in_extract_lines = True

    def enterEveryRule(self, ctx: ParserRuleContext):
        if self.is_in_target_method:
            if set(range(ctx.start.line, ctx.stop.line + 1)) & set(self.lines):
                if not set(self.lines).issubset(set(range(ctx.start.line, ctx.stop.line + 1))) and not set(
                        range(ctx.start.line, ctx.stop.line + 1)).issubset(self.lines):
                    raise Exception('input lines contains some part of a command,not the entire command!')

    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        # print('for variable:', str(ctx.IDENTIFIER()))
        if self.is_in_target_method:
            if self.assign_variable_in_extract_lines:
                # print(1)
                if self.pre_variables.keys().__contains__(str(ctx.IDENTIFIER())):
                    print(self.post_variables)
                    if self.assigned_variable and (
                    not is_equivalent(self.assigned_variable, str(ctx.IDENTIFIER()))) and len(self.post_variables) > 1:
                        raise Exception(
                            'Only one value assignment is allowed in extracted lines.(found \'' + self.assigned_variable + '\' before.)')
                    else:
                        if self.post_variables.__contains__(str(ctx.IDENTIFIER())):
                            self.assigned_variable = str(ctx.IDENTIFIER())
                        if not self.created_variables.__contains__(
                                str(ctx.IDENTIFIER())) and self.pre_variables.keys().__contains__(
                            str(ctx.IDENTIFIER())):
                            self.used_variables.add(str(ctx.IDENTIFIER()))
                self.assign_variable_in_extract_lines = False
            elif self.pre_assign_variable:
                # print(2)
                self.pre_assign_variable = False
                self.pre_variables[str(ctx.IDENTIFIER())]['init'] = True
            elif not set(range(ctx.start.line, ctx.stop.line + 1)).issubset(set(self.lines)):
                # print(3)
                if ctx.start.line > self.last_line:
                    self.post_variables.append(str(ctx.IDENTIFIER()))
            else:
                # print(4)
                # print(not self.created_variables.__contains__(
                #         str(ctx.IDENTIFIER())))
                # print(self.pre_variables.keys())
                # print(self.pre_variables.keys().__contains__(str(ctx.IDENTIFIER())))
                if not self.created_variables.__contains__(
                        str(ctx.IDENTIFIER())) and self.pre_variables.keys().__contains__(str(ctx.IDENTIFIER())):
                    self.used_variables.add(str(ctx.IDENTIFIER()))
                # if self.variable_info['variables'].keys().__contains__(str(ctx.IDENTIFIER())):
                #     self.used_variables.add(str(ctx.IDENTIFIER()))

    # def exitEveryRule(self, ctx: ParserRuleContext):
    #     if self.is_inside_rule is not None and self.is_inside_rule == ctx:
    #         self.is_inside_rule = None


# helper functions
def get_args(variables, all_variables):
    result = '('
    first = True
    for item in variables:
        if not all_variables[item]['init']:
            continue
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
        if not all_variables[item]['init']:
            continue
        if not first:
            result += ', '
        else:
            first = False
        result += all_variables[item]['type'] + ' ' + item
    result += ')'
    return result


# extract method function
def extract_method(conf):
    stream = FileStream(conf['target_file'], encoding="utf-8")
    lexer = JavaLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    tree = parser.compilationUnit()
    listener0 = ExtractMethodRefactoring(conf['lines'])
    walker0 = ParseTreeWalker()
    walker0.walk(
        listener=listener0,
        t=tree
    )
    listener = ExtractMethodRefactoring(conf['lines'],listener0.post_variables)
    walker1 = ParseTreeWalker()
    walker1.walk(
        listener=listener,
        t=tree
    )
    # print(parser.getTokenStream())
    # print(listener.variable_info)
    # print(listener.used_variables)
    # print(listener.created_variables)
    # print(listener.pre_variables)

    output = []
    file1 = open(conf['target_file'], 'r', encoding="utf-8")
    lines = file1.readlines()
    line_num = 1
    # func_added = False
    func = []
    print('extracting following lines:')
    for line in lines:
        if listener.lines.__contains__(line_num):
            print(line, end='')
            if line_num == listener.last_line:
                if listener.assigned_variable:
                    output.append('\t\t' + listener.assigned_variable + ' = ' + conf['new_method_name'] + get_args(
                        listener.used_variables, listener.pre_variables))
                else:
                    output.append(
                        '\t\t' + conf['new_method_name'] + get_args(listener.used_variables, listener.pre_variables))
            func.append(line)
        elif line_num == listener.method_stop_line:
            output.append(line)
            output.append('\tprivate '+ ('static ' if listener.is_target_method_static else '')+'void ' + conf['new_method_name'] + get_args_with_type(listener.used_variables,
                                                                                           listener.pre_variables) + ((' throws '+listener.exception) if listener.exception is not None else '') + '\n')
            output.append('\t{\n')
            for item in listener.pre_variables.keys():
                var = listener.pre_variables[item]
                if not var['init']:
                    output.append('\t\t'+var['type']+' '+item+';\n')
            output = output + func
            if listener.assigned_variable:
                output.append('\t\treturn ' + listener.assigned_variable + ';\n')
            output.append('\t}\n')
        else:
            output.append(line)
        line_num += 1
    file1.close()

    file2 = open(conf['output_file'], 'w', encoding="utf-8")
    for item in output:
        file2.write(item)
    file2.close()


"""
    driver method
"""


def main():
    print("Started Extract Method")
    _conf = {
        'target_file': "/mnt/d/Sajad/Uni/Spring00/Compiler/CodART/tests/extract_method/in/ExtractMethodTest.java",
        'output_file': "/mnt/d/Sajad/Uni/Spring00/Compiler/CodART/tests/extract_method/out/ExtractMethodTest.java",
        'lines': [7, 8],
        'new_method_name': 'printDetails',
    }
    extract_method(_conf)

    print("Finished Extract Method")


if __name__ == '__main__':
    main()

