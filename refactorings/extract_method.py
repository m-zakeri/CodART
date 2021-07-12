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


    def __init__(self, lines: list):

        # checks Target method and lines to be valid
        if lines is None or len(lines) == 0:
            raise Exception('target lines are not specified.')

        # setting variables
        self.lines = np.array(lines)
        self.lines.reshape((len(lines), 1))
        self.last_line = self.lines.max()
        self.first_line = self.lines.min()
        self.post_variables = {}
        self.pre_variables = {}
        self.mid_variables = {}
        self.is_in_target_method = False
        self.is_target_method_static = False
        self.is_result_valid = False
        self.exception_thrown_in_target_method = None
        self.assigning_value_pre = False
        self.assigning_value_mid = False
        self.assigning_value_post = False
        self.method_stop_line = 0
        self.return_variable = None
        self.return_variable_type = None
        self.methods_name = []


    ######################################
    # Overriding required methods to satisfy our extraction requirements
    ######################################


    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.methods_name.append(ctx.IDENTIFIER().getText())
        #checks if this is the method containing target lines
        if ctx.start.line <= self.first_line and ctx.stop.line >= self.last_line:
            print("Found method containing target lines.")
            self.is_in_target_method = True
            self.is_result_valid = True

            # checks if method is static
            for modifier in ctx.parentCtx.parentCtx.modifier():
                if modifier.getText() == 'static':
                    self.is_target_method_static = True
                    print("Target Method is static.")
                    break

            #checks if method throws any exception
            if ctx.qualifiedNameList():
                self.exception_thrown_in_target_method = ctx.qualifiedNameList().getText()
                print("Target Method throws exception.")
                # TODO : check extracted lines for exception occurrence instead ,
                #  as they may not throw exception even though their parent method does

            # save method's last line number
            self.method_stop_line = ctx.stop.line


    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.is_in_target_method = False


    def enterConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):

        # checks if this Constructor contains target lines
        if ctx.start.line <= self.first_line and ctx.stop.line >= self.last_line:
            print("Found Constructor containing target lines.")
            self.is_in_target_method = True
            self.is_result_valid = True

            # checks if Constructor is static
            for modifier in ctx.parentCtx.parentCtx.modifier():
                if modifier.getText() == 'static':
                    self.is_target_method_static = True
                    print("Target Method is static.")
                    break

            # checks if Constructor throws any exception
            if ctx.qualifiedNameList():
                self.exception_thrown_in_target_method = ctx.qualifiedNameList().getText()
                print("Target Method throws exception.")
                # TODO : check extracted lines for exception occurrence instead ,
                #  as they may not throw exception even though their parent method does

            # save method's last line number
            self.method_stop_line = ctx.stop.line


    def exitConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):
        self.is_in_target_method = False


    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):

        # checks if we are in target method
        if self.is_in_target_method:

            # checks if this statement is not in extracting lines
            if not set(range(ctx.start.line, ctx.stop.line + 1)).issubset(set(self.lines)):

                # checks if this statement is before extracting lines
                if ctx.start.line < self.last_line:

                    # adding all created variables
                    for var in ctx.variableDeclarators().variableDeclarator():
                        self.pre_variables[var.variableDeclaratorId().getText()] = \
                            {
                                'type': ctx.typeType().getText(),
                                'write': str(var.getText()).__contains__('=')
                            }

                # this statement is after extracting lines
                else:
                    pass

            # this statement is inside extracting lines
            else:

                # adding all created variables
                for var in ctx.variableDeclarators().variableDeclarator():
                    self.mid_variables[
                        var.variableDeclaratorId().getText()] = \
                        {
                            'type': ctx.typeType().getText(),
                            'write': str(var.getText()).__contains__('=')
                        }


    def enterEnhancedForControl(self, ctx:JavaParserLabeled.EnhancedForControlContext):

        # checks if we are in target method
        if self.is_in_target_method:

            # checks if this statement is not in extracting lines
            if not set(range(ctx.start.line, ctx.stop.line + 1)).issubset(set(self.lines)):

                # checks if this statement is before extracting lines
                if ctx.start.line < self.last_line:

                    # adding created variables
                    var = ctx.variableDeclaratorId()
                    self.pre_variables[var.getText()] = \
                        {
                            'type': ctx.typeType().getText(),
                            'write': True
                        }

                # this statement is after extracting lines
                else:
                    pass

            # this statement is inside extracting lines
            else:

                # adding created variables
                var = ctx.variableDeclaratorId()
                self.mid_variables[var.getText()] = \
                    {
                        'type': ctx.typeType().getText(),
                        'write': True
                    }



    # adding target method parameters to pre_variables
    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):

        # checks if we are in target method
        if self.is_in_target_method:

            # adding all created variables
            self.pre_variables[ctx.variableDeclaratorId().getText()] = \
            {
                'type': ctx.typeType().getText(),
                'write': True
            }


    # detecting writing value to variables
    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):

        # checks if we are in target method
        if self.is_in_target_method:

            # checks if this statement is not in extracting lines
            if not set(range(ctx.start.line, ctx.stop.line + 1)).issubset(set(self.lines)):

                # checks if this statement is before extracting lines
                if ctx.start.line < self.last_line:
                    self.assigning_value_pre = True

                # this statement is after extracting lines
                elif ctx.start.line > self.last_line:
                    self.assigning_value_post = True

                # any other case is useless
                else:
                    pass

            # this statement is inside extracting lines
            else:
                self.assigning_value_mid = True


    def enterEveryRule(self, ctx: ParserRuleContext):

        # checks if we are in target method
        if self.is_in_target_method:

            #checks if every statements are is either completely inside or outside of extracting lines
            if set(range(ctx.start.line, ctx.stop.line + 1)) & set(self.lines):
                if not set(self.lines).issubset(set(range(ctx.start.line, ctx.stop.line + 1))) and \
                        not set(range(ctx.start.line, ctx.stop.line + 1)).issubset(self.lines):
                    self.is_result_valid = False


    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):

        # checks if we are in target method
        if self.is_in_target_method:

            # print('entering:',ctx.getText())
            # print(self.assigning_value_pre)
            # print(self.assigning_value_mid)
            # print(self.assigning_value_post)

            # writing value to a variable in mid
            if self.assigning_value_mid:

                # adding variable
                action = 'write'
                if (isinstance(ctx.parentCtx.parentCtx,
                              JavaParserLabeled.Expression1Context) and ctx.parentCtx.parentCtx.DOT() )or\
                        (isinstance(ctx.parentCtx.parentCtx,
                              JavaParserLabeled.Expression2Context) and ctx.parentCtx.parentCtx.LBRACK()):
                    # print("exiting:", ctx.getText())
                    action = 'read'
                if self.mid_variables.keys().__contains__(str(ctx.IDENTIFIER())):
                    self.mid_variables[str(ctx.IDENTIFIER())][action] = True
                else:
                    self.mid_variables[str(ctx.IDENTIFIER())] = {action: True}
                self.assigning_value_mid=False

            # writing value to a variable in pre
            elif self.assigning_value_pre:

                # adding variable
                action = 'write'
                if (isinstance(ctx.parentCtx.parentCtx,
                              JavaParserLabeled.Expression1Context) and ctx.parentCtx.parentCtx.DOT() )or\
                        (isinstance(ctx.parentCtx.parentCtx,
                              JavaParserLabeled.Expression2Context) and ctx.parentCtx.parentCtx.LBRACK()):
                    # print("exiting:", ctx.getText())
                    action = 'read'
                if self.pre_variables.keys().__contains__(str(ctx.IDENTIFIER())):
                    self.pre_variables[str(ctx.IDENTIFIER())][action] = True
                else:
                    self.pre_variables[str(ctx.IDENTIFIER())] = {action: True}
                self.assigning_value_pre = False

            # writing value to a variable in post
            elif self.assigning_value_post:

                # adding variable
                action = 'write'
                if (isinstance(ctx.parentCtx.parentCtx,
                              JavaParserLabeled.Expression1Context) and ctx.parentCtx.parentCtx.DOT() )or\
                        (isinstance(ctx.parentCtx.parentCtx,
                              JavaParserLabeled.Expression2Context) and ctx.parentCtx.parentCtx.LBRACK()):
                    # print("exiting:", ctx.getText())
                    action = 'read'
                if self.post_variables.keys().__contains__(str(ctx.IDENTIFIER())):
                    self.post_variables[str(ctx.IDENTIFIER())][action] = True
                else:
                    self.post_variables[str(ctx.IDENTIFIER())] = {action : True}
                self.assigning_value_post = False

            # reading a variable value not in extracting lines
            elif not set(range(ctx.start.line, ctx.stop.line + 1)).issubset(set(self.lines)):

                # checks if this statement is after extracting lines
                if ctx.start.line > self.last_line:

                    # adding variable to post_variables
                    if self.post_variables.keys().__contains__(str(ctx.IDENTIFIER())):
                        self.post_variables[str(ctx.IDENTIFIER())]['read'] = True
                    else:
                        self.post_variables[str(ctx.IDENTIFIER())] = {'read' : True}

                # this statement is before extracting lines
                else:
                    pass

            # this statement is inside extracting lines
            else:
                if self.mid_variables.keys().__contains__(str(ctx.IDENTIFIER())):
                    self.mid_variables[str(ctx.IDENTIFIER())]['read'] = True
                else:
                    self.mid_variables[str(ctx.IDENTIFIER())] = {'read' : True}


    # helper functions
    # get method arguments for function call
    def get_args(self, include_type : bool):
        print(self.pre_variables)
        result = '('
        first = True
        for key in self.mid_variables.keys():
            if self.mid_variables[key].keys().__contains__('type'):
                continue
            if self.pre_variables.keys().__contains__(key) and\
                    self.pre_variables[key].keys().__contains__('write') and \
                    self.pre_variables[key]['write'] and \
                    self.pre_variables[key].keys().__contains__('type'):
                if not first:
                    result += ', '
                else:
                    first = False
                if include_type:
                    result += self.pre_variables[key]['type'] + ' ' + key
                else:
                    result += key
        result += ')' + ("" if include_type else ";")
        return result


    def get_write_variable(self):
        result = None
        for key in self.post_variables.keys():
            if self.mid_variables.__contains__(key) and self.mid_variables[key].__contains__('type') and self.mid_variables[key]['type']:
                if result is None:
                    self.return_variable = key
                    self.return_variable_type = self.mid_variables[key]['type']
                    result = self.mid_variables[key]['type'] + ' ' + key + ' = '
                else:
                    print('assignments on :',self.return_variable,",",key)
                    self.return_variable = None
                    raise Exception('only one assignment in extracting lines is acceptable!')

            elif self.pre_variables.__contains__(key) and self.pre_variables[key].__contains__('type') and self.pre_variables[key]['type'] and self.mid_variables.__contains__(key) and self.mid_variables[key].__contains__('write') and self.mid_variables[key]['write']:
                if result is None:
                    result = key + ' = '
                    self.return_variable = key
                    self.return_variable_type = self.pre_variables[key]['type']
                else:
                    print('assignments on :', self.return_variable, ",", key)
                    self.return_variable = None
                    raise Exception('only one assignment in extracting lines is acceptable!')
        return '' if result is None else result


def get_tabs(line : str):
    line_trim = line.lstrip()
    return line.split(line_trim)[0]





# extract method function
def extract_method(conf):
    stream = FileStream(conf['target_file'], encoding="utf-8")
    lexer = JavaLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    tree = parser.compilationUnit()
    listener = ExtractMethodRefactoring(conf['lines'])
    walker = ParseTreeWalker()
    walker.walk(
        listener=listener,
        t=tree
    )

    if not listener.is_result_valid:
        raise Exception('Some problem happened!')

    if listener.methods_name.__contains__(conf['new_method_name']):
        raise Exception('New method name already exists.')

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
                output.append(get_tabs(line) + listener.get_write_variable()
                              + conf['new_method_name'] + listener.get_args(False) + '\n')
            func.append(line)
        elif line_num == listener.method_stop_line:
            output.append(line)
            output.append(get_tabs(line)+'private '+ ('static ' if listener.is_target_method_static else '')+
                          (listener.return_variable_type if listener.return_variable_type else 'void') + ' '+
                          conf['new_method_name'] + listener.get_args(True) +
                          ((' throws '+listener.exception_thrown_in_target_method)
                           if listener.exception_thrown_in_target_method is not None else '') + '\n')
            output.append(get_tabs(line)+'{\n')
            for item in listener.pre_variables.keys():
                var = listener.pre_variables[item]
                if var.keys().__contains__('write') and not var['write']:
                    output.append(get_tabs(line)+'\t'+var['type']+' '+item+';\n')
            output = output + func
            if listener.return_variable is not None:
                output.append(get_tabs(line)+'\treturn ' + listener.return_variable + ';\n')
            output.append(get_tabs(line)+'}\n')
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
        'lines': [23,24],
        'new_method_name': 'method1',
    }
    extract_method(_conf)

    print("Finished Extract Method")


if __name__ == '__main__':
    main()

