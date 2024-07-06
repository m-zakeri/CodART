"""
The module implements dependency injection patterns
"""

version = '0.1.1'
author = 'Sadegh Jafari, Morteza Zakeri'

import json

import networkx as nx
from csv import writer

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter


from design_4_testability.gen.JavaLexer import JavaLexer
from design_4_testability.gen.JavaParserLabeled import JavaParserLabeled
from design_4_testability.gen.JavaParserLabeledListener import JavaParserLabeledListener

from design_4_testability.utils.utils import Path, File, Struct, get_parser_and_tokens, get_parser
from .interface import InterfaceCreator, InterfaceInfoListener
from design_4_testability import config
from design_4_testability.class_diagram_extraction.class_diagram import ClassDiagram
from .injector import Injector


class ConstructorEditorListener(JavaParserLabeledListener):
    def __init__(self,
                 base_dirs,
                 file,
                 index_dic,
                 roots_long_name,
                 common_token_stream: CommonTokenStream = None
                 ):
        self.base_dirs = base_dirs
        self.file = file
        self.index_dic = index_dic
        self.file_name = Path.get_file_name_from_path(file)
        self.roots_long_name = roots_long_name

        self.dependees = dict()
        self.in_method = False
        self.current_constructor = None
        self.current_class = None
        self.current_class_long_name = None
        self.last_import_token_index = None
        self.imports = list()
        self.imports_star = list()
        self.method_depth = 0
        self.class_depth = 0
        self.field_variables = dict()
        self.constructors = list()
        self.generate_constructor_location = None
        self.no_constructor_injection_cases = 0
        self.statistics = dict()
        self.package = None
        self.dependencies = list()
        self.long_names_dict = dict()
        self.result = {
            "classes": dict(),
            "interfaces": set()
        }
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def get_long_name(self, name):
        if name in self.long_names_dict:
            return self.long_names_dict[name]
        else:
            splitted_name = name.split('.')
            package, file = Path.find_package_of_dependee(
                name,
                self.imports,
                self.imports_star,
                self.index_dic,
                current_package=self.package,
                current_file=name,
            )
            if len(splitted_name) == 1:
                return f'{package}-{file}-{name}'
            else:
                return f'{package}-{file}-{splitted_name[-1]}'

    @staticmethod
    def get_field_variable_struct():
        field_variable = {
            'modifiers': list(),
            'identifier': None,
            'type': None,
            'declaration_location': None,
            'initiation_location': None,
            'initiation_place': None,
            'assigned_variable': None,
            'dependencies': list(),
            'constructors_info': list()
        }
        return Struct(**field_variable)

    @staticmethod
    def get_constructor_info_struct(constructor=None, initiation_location=None):
        constructor_info = {
            'constructor': constructor,
            'dependencies': list(),
            'initiation_location': initiation_location
        }
        return Struct(**constructor_info)

    @staticmethod
    def get_dependee_struct():
        dependee = {
            'name': None,
            'package': None,
            'file': None,
            'type': None
        }
        return Struct(**dependee)

    @staticmethod
    def get_constructor_struct():
        constructor = {
            'formal_parameters': list(),
            'formal_parameters_start_location': None,
            'stop_location': None,
            'start_location': None
        }
        return Struct(**constructor)

    @staticmethod
    def get_formal_parameter_struct():
        formal_parameter = {
            'identifier': None,
            'type': None,
            'location': None
        }
        return Struct(**formal_parameter)

    def edit_variable_type(self, variable_type, location):
        self.token_stream_rewriter.replace(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            from_idx=location,
            to_idx=location,
            text=variable_type
        )

    def delete_new(self, start, stop):
        self.token_stream_rewriter.delete(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            from_idx=start,
            to_idx=stop
        )

    def edit_new(self, text, start, stop):
        self.token_stream_rewriter.replace(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            from_idx=start,
            to_idx=stop,
            text=text
        )

    def add_formal_parameter(self, text, location):
        self.token_stream_rewriter.insertAfter(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            index=location,
            text=text
        )

    def edit_formal_parameter(self, variable_type, location):
        self.token_stream_rewriter.replace(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            from_idx=location,
            to_idx=location,
            text=variable_type
        )

    def add_assignment(self, text, location):
        self.token_stream_rewriter.insertAfter(
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
            index=location,
            text=text
        )

    @staticmethod
    def check_modifiers(modifiers):
        invalid_modifiers = ['final', 'static']
        for modifier in modifiers:
            if modifier in invalid_modifiers:
                return False
        return True

    def check_constructor_injection_case1(self, field_variable):
        if field_variable.initiation_place == 'fieldDeclaration' and \
                self.check_modifiers(field_variable.modifiers) and \
                field_variable.type in self.dependees and \
                field_variable.initiation_location:
            for dependency in field_variable.dependencies:
                if dependency['type'] == 'method_call':
                    return False
            return True
        return False

    def check_constructor_injection_case2(self, field_variable, constructor):
        if field_variable.initiation_place == 'constructor' and \
                self.check_modifiers(field_variable.modifiers) and \
                field_variable.type in self.dependees and \
                field_variable.initiation_location:
            constructor_params = [formal_param.identifier for formal_param in constructor.formal_parameters]
            constructor_info = self.find_constructor_info_from_constructor(field_variable, constructor)
            if constructor_info is None:
                return False
            for dependency in constructor_info.dependencies:
                if dependency['type'] == 'identifier':
                    if dependency['value'] not in constructor_params:
                        return False
                elif dependency['type'] == 'method_call':
                    return False
            return True
        return False

    # def check_constructor_injection_case3(self, field_variable, constructor):
    #     if field_variable.initiation_place == 'constructor' and \
    #             self.check_modifiers(field_variable.modifiers) and \
    #             field_variable.type in self.dependees and \
    #             field_variable.assigned_variable:
    #         constructor_params = [formal_param.identifier for formal_param in constructor.formal_parameters]
    #         constructor_info = self.find_constructor_info_from_constructor(field_variable, constructor)
    #         if constructor_info is None:
    #             return False
    #         for dependency in constructor_info.dependencies:
    #             if dependency['type'] == 'identifier':
    #                 if dependency['value'] not in constructor_params:
    #                     return False
    #             elif dependency['type'] == 'method_call':
    #                 return False
    #         return True
    #     return False

    def get_statistics(self):
        result = {'case1': 0, 'case2': 0, 'case3': 0}
        for v in self.field_variables:
            if self.check_constructor_injection_case1(self.field_variables[v]):
                result['case1'] += 1

            for constructor in self.constructors:
                if self.check_constructor_injection_case2(self.field_variables[v], constructor):
                    result['case2'] += 1
                # elif self.check_constructor_injection_case3(self.field_variables[v], constructor):
                #     result['case3'] += 1
        return result

    def generate_constructor(self):
        text = ''
        formal_variable_text = ''
        assign_text = ''
        self.result['classes'][self.current_class_long_name].append([])
        for v in self.field_variables:
            v_info = self.field_variables[v]
            if self.check_constructor_injection_case1(v_info):
                dependency = {
                    'type': self.get_long_name(v_info.type),
                    'arguments': [d['value'] for d in v_info.dependencies]
                }
                self.result['classes'][self.current_class_long_name][-1].append(dependency)
                self.delete_new(v_info.initiation_location[0], v_info.initiation_location[1])

                variable_type = v_info.type
                if self.dependees[v_info.type].type == 'class':
                    variable_type = 'I' + v_info.type
                    location = v_info.declaration_location[0] + len(v_info.modifiers) - 1
                    self.edit_variable_type(variable_type, location)

                formal_variable_text += f"{variable_type} {v}, "
                assign_text += f"\n\t\tthis.{v} = {v};"
        formal_variable_text = formal_variable_text[:-1]
        assign_text = '{' + assign_text + '\n\t}'

        if assign_text == '':
            text += f"{self.current_class} ({formal_variable_text})\n\t{assign_text}\n\n\t"
            self.token_stream_rewriter.insertAfter(
                self.generate_constructor_location,
                text,
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME
            )

    @staticmethod
    def find_constructor_info_from_constructor(variable_info, constructor):
        for constructor_info in variable_info.constructors_info:
            if constructor_info.constructor == constructor:
                return constructor_info

    def edit_constructors(self):
        for c in self.constructors:
            assignments_text = ''
            formal_parameters_text = list()
            self.result['classes'][self.current_class_long_name].append([])
            for v in self.field_variables:
                v_info = self.field_variables[v]
                if self.check_constructor_injection_case1(v_info):
                    dependency = {
                        'type': self.get_long_name(v_info.type),
                        'arguments': [d['value'] for d in v_info.dependencies]
                    }
                    self.result['classes'][self.current_class_long_name][-1].append(dependency)
                    self.delete_new(v_info.initiation_location[0], v_info.initiation_location[1])
                    variable_type = v_info.type
                    if self.dependees[v_info.type].type == 'class':
                        self.result['interfaces'].add(self.get_long_name(v_info.type))
                        variable_type = 'I' + v_info.type
                        location = v_info.declaration_location[0] + len(v_info.modifiers) - 1
                        self.edit_variable_type(variable_type, location)

                    assignments_text += f"\n\t\tthis.{v} = {v};"
                    formal_parameters_text.append(f"{variable_type} {v}")

                elif self.check_constructor_injection_case2(v_info, c):
                    constructor_info = self.find_constructor_info_from_constructor(v_info, c)
                    dependency = {
                        'type': self.get_long_name(v_info.type),
                        'arguments': [d['value'] for d in constructor_info.dependencies]
                    }
                    self.result['classes'][self.current_class_long_name][-1].append(dependency)
                    if constructor_info.initiation_location:
                        self.edit_new(
                            v,
                            constructor_info.initiation_location[0],
                            constructor_info.initiation_location[1]
                        )
                        variable_type = v_info.type
                        # try:
                        #     self.dependees[v_info.type].type['type'] == 'class'
                        # except TypeError:
                        #     print('here')
                        if self.dependees[v_info.type].type == 'class':
                            self.result['interfaces'].add(self.get_long_name(v_info.type))
                            variable_type = 'I' + v_info.type
                            location = v_info.declaration_location[0] + len(v_info.modifiers) - 1
                            self.edit_variable_type(variable_type, location)

                        formal_parameters_text.append(f"{variable_type} {v}")
                # elif self.check_constructor_injection_case3(v_info, c):
                #     constructor_info = self.find_constructor_info_from_constructor(v_info, c)
                #     dependency = {
                #         'type': self.get_long_name(v_info.type),
                #         'arguments': [d['value'] for d in constructor_info.dependencies]
                #     }
                #     self.result['classes'][self.current_class_long_name][-1].append(dependency)
                #     if self.dependees[v_info.assigned_variable.type].type['type'] == 'class':
                #         self.result['interfaces'].add(self.get_long_name(v_info.assigned_variable.type))
                #         variable_type = 'I' + v_info.assigned_variable.type
                #         location = v_info.assigned_variable.location[0]
                #         self.edit_variable_type(variable_type, location)

            if assignments_text != '':
                if c.stop_location - c.start_location > 1:
                    assignment_location = c.stop_location - 2
                else:
                    assignment_location = c.stop_location - 1
                self.add_assignment(assignments_text, assignment_location)

            if len(formal_parameters_text) > 0:
                formal_parameter_location = c.formal_parameters_start_location
                formal_parameters_text = ', '.join(formal_parameters_text)
                if len(c.formal_parameters) > 0:
                    formal_parameters_text += ', '
                self.add_formal_parameter(formal_parameters_text, formal_parameter_location)

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package = ctx.qualifiedName().getText()
        self.last_import_token_index = ctx.stop.tokenIndex

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        self.last_import_token_index = ctx.stop.tokenIndex
        if '*' in ctx.getText():
            self.imports_star.append(ctx.qualifiedName().getText())
        else:
            self.imports.append(ctx.qualifiedName().getText())

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.package is None:
            self.package = Path.get_default_package(self.base_dirs, self.file)
        self.class_depth += 1
        if self.class_depth == 1:
            self.current_class = ctx.IDENTIFIER().getText()
            self.current_class_long_name = f'{self.package}-{self.file_name}-{self.current_class}'
            self.result['classes'][self.current_class_long_name] = []

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        # add current package dependee
        for key, value in self.index_dic.items():
            package, file_name, class_name = key.split('-')
            if (self.package == package) and (class_name not in self.dependees):
                dependee = self.get_dependee_struct()
                dependee.name = class_name
                dependee.package = package
                dependee.type = value['type']
                self.dependees[class_name] = dependee

        self.class_depth -= 1
        if self.class_depth == 0:
            long_name = f"{self.package}-{self.file_name}-{self.current_class}"
            if long_name not in self.roots_long_name:
                if len(self.constructors) == 0:     # only can case 1 happen
                    self.generate_constructor()
                else:
                    self.edit_constructors()

                self.statistics[long_name] = self.get_statistics()

            self.current_class = None
            self.current_class_long_name = None
            self.field_variables = dict()
            self.constructors = list()

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        if self.class_depth == 1:
            self.generate_constructor_location = ctx.LBRACE().symbol.tokenIndex

    def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        if self.class_depth == 1:
            self.in_method = True

    def exitMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        if self.class_depth == 1:
            self.in_method = False

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if self.class_depth == 1 and (not self.in_method):
            classBodyDeclaration = ctx.parentCtx.parentCtx
            self.generate_constructor_location = ctx.parentCtx.parentCtx.stop.tokenIndex + 1
            modifiers = []
            _type = ctx.typeType().getText()
            if _type not in self.dependees:
                dependee = self.get_dependee_struct()
                dependee.name = _type
                dependee.package, dependee.file = Path.find_package_of_dependee(
                    _type,
                    self.imports,
                    self.imports_star,
                    self.index_dic,
                    self.package,
                    self.file_name
                )
                if dependee.package is not None:
                    long_name = f"{dependee.package}-{dependee.file}-{dependee.name}"
                    if long_name in self.index_dic:
                        dependee.type = self.index_dic[long_name]["type"]
                        self.dependees[_type] = dependee
            start_declaration_location = ctx.start.tokenIndex

            for modifier in classBodyDeclaration.modifier():
                modifiers.append(modifier.getText())

            for identifier in ctx.variableDeclarators().variableDeclarator():
                if '[' in identifier.variableDeclaratorId().getText():
                    continue
                stop_declaration_location = identifier.variableDeclaratorId().stop.tokenIndex
                field_variable = self.get_field_variable_struct()
                field_variable.modifiers = modifiers
                field_variable.identifier = identifier.variableDeclaratorId().getText()
                field_variable.type = _type
                field_variable.declaration_location = (start_declaration_location, stop_declaration_location)
                self.field_variables[identifier.variableDeclaratorId().getText()] = field_variable

    def enterVariableInitializer1(self, ctx:JavaParserLabeled.VariableInitializer1Context):
        if self.class_depth == 1 and (not self.in_method):
            if ctx.children[0].children[0].getText() == 'new':
                for child in ctx.parentCtx.parentCtx.children:
                    if type(child).__name__ == 'VariableDeclaratorContext':
                        identifier = child.variableDeclaratorId().getText()
                        if identifier in self.field_variables:
                            self.field_variables[identifier].initiation_location = \
                                (ctx.start.tokenIndex - 2, ctx.stop.tokenIndex)
                            self.field_variables[identifier].initiation_place = 'fieldDeclaration'

                            if ctx.expression().creator().classCreatorRest() is not None:
                                if ctx.expression().creator().classCreatorRest().arguments().expressionList() is not None:
                                    for dependency in ctx.expression().creator().classCreatorRest().arguments().expressionList().expression():
                                        if 'primary' in dir(dependency):
                                            if 'IDENTIFIER' in dir(dependency.primary()):
                                                if dependency.primary().IDENTIFIER():
                                                    self.field_variables[identifier].dependencies.append(
                                                        {'type': 'identifier', 'value': dependency.getText()}
                                                    )
                                            elif 'literal' in dir(dependency.primary()):
                                                if dependency.primary().literal():
                                                    self.field_variables[identifier].dependencies.append(
                                                        {'type': 'literal', 'value': dependency.getText()}
                                                    )
                                        else:
                                            self.field_variables[identifier].dependencies.append(
                                                {'type': 'method_call', 'value': dependency.getText()}
                                            )

    def enterExpression4(self, ctx:JavaParserLabeled.Expression4Context):
        if self.class_depth == 1 and (not self.in_method):
            identifier_list = ctx.parentCtx.children[0].getText()
            identifier_list = identifier_list.split('.')
            if len(identifier_list) == 1:
                identifier = identifier_list[0]
            elif len(identifier_list) == 2 and identifier_list[0] == 'this':
                identifier = identifier_list[1]
            else:
                identifier = None

            if identifier is not None:
                if identifier in self.field_variables:
                    self.field_variables[identifier].initiation_location = \
                        (ctx.start.tokenIndex, ctx.stop.tokenIndex)
                    if self.current_constructor:
                        self.field_variables[identifier].initiation_place = 'constructor'
                        if len(self.field_variables[identifier].constructors_info) == 0:
                            constructor_info = self.get_constructor_info_struct(
                                constructor=self.current_constructor,
                                initiation_location=(ctx.start.tokenIndex, ctx.stop.tokenIndex)
                            )
                            self.field_variables[identifier].constructors_info.append(constructor_info)
                        elif self.field_variables[identifier].constructors_info[-1].constructor != self.current_constructor:
                            constructor_info = self.get_constructor_info_struct(
                                constructor=self.current_constructor,
                                initiation_location=(ctx.start.tokenIndex, ctx.stop.tokenIndex)
                            )
                            self.field_variables[identifier].constructors_info.append(constructor_info)
                        elif self.field_variables[identifier].constructors_info[-1].constructor == self.current_constructor and \
                                self.field_variables[identifier].constructors_info[-1].initiation_location is None:
                            self.field_variables[identifier].constructors_info[-1].initiation_location = \
                                (ctx.start.tokenIndex, ctx.stop.tokenIndex)

                        if ctx.creator().classCreatorRest() is not None:
                            if ctx.creator().classCreatorRest().arguments().expressionList() is not None:
                                for dependency in ctx.creator().classCreatorRest().arguments().expressionList().expression():
                                    if 'primary' in dir(dependency):
                                        if 'IDENTIFIER' in dir(dependency.primary()):
                                            if dependency.primary().IDENTIFIER():
                                                self.field_variables[identifier].constructors_info[-1].dependencies.append(
                                                    {'type': 'identifier', 'value': dependency.getText()}
                                                )
                                                self.field_variables[identifier].dependencies.append(
                                                    {'type': 'identifier', 'value': dependency.getText()}
                                                )
                                        elif 'literal' in dir(dependency.primary()):
                                            if dependency.primary().literal():
                                                self.field_variables[identifier].constructors_info[-1].dependencies.append(
                                                    {'type': 'literal', 'value': dependency.getText()}
                                                )
                                                self.field_variables[identifier].dependencies.append(
                                                    {'type': 'literal', 'value': dependency.getText()}
                                                )
                                    else:
                                        self.field_variables[identifier].constructors_info[-1].dependencies.append(
                                            {'type': 'method_call', 'value': dependency.getText()}
                                        )
                                        self.field_variables[identifier].dependencies.append(
                                            {'type': 'method_call', 'value': dependency.getText()}
                                        )

    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        if self.class_depth == 1:
            constructor = self.get_constructor_struct()
            constructor.start_location = ctx.block().start.tokenIndex
            constructor.stop_location = ctx.stop.tokenIndex
            constructor.formal_parameters_start_location = ctx.formalParameters().start.tokenIndex
            if ctx.formalParameters().formalParameterList() is not None:
                for formal_parameter in ctx.formalParameters().formalParameterList().formalParameter():
                    formal_parameter_s = self.get_formal_parameter_struct()
                    formal_parameter_s.identifier = formal_parameter.variableDeclaratorId().getText()
                    formal_parameter_s.type = formal_parameter.typeType().getText()
                    formal_parameter_s.location = (
                        formal_parameter.start.tokenIndex,
                        formal_parameter.stop.tokenIndex
                    )
                    constructor.formal_parameters.append(formal_parameter_s)
            self.constructors.append(constructor)
            self.current_constructor = constructor

    def exitConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):
        if self.class_depth == 1:
            self.current_constructor = None

    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        if self.class_depth == 1 and (not self.in_method):
            identifier_list = ctx.children[0].getText()
            identifier_list = identifier_list.split('.')
            if len(identifier_list) == 1:
                identifier = identifier_list[0]
            elif len(identifier_list) == 2 and identifier_list[0] == 'this':
                identifier = identifier_list[1]
            else:
                identifier = None

            right_value_list = ctx.children[-1].getText()
            right_value_list = right_value_list.split('.')
            if len(right_value_list) == 1:
                right_value = right_value_list[0]
            else:
                right_value = None

            if (identifier is not None) and (right_value is not None) and identifier in self.field_variables and\
                    self.current_constructor:
                if len(self.current_constructor.formal_parameters) == 2:
                    for formal_param in self.current_constructor.formal_parameters:
                        if formal_param.identifier == ctx.expression()[1].getText():
                            self.field_variables[identifier].assigned_variable = formal_param
                            break

                self.field_variables[identifier].initiation_place = 'constructor'
                if len(self.field_variables[identifier].constructors_info) == 0:
                    constructor_info = self.get_constructor_info_struct(
                        constructor=self.current_constructor
                    )
                    self.field_variables[identifier].constructors_info.append(constructor_info)
                elif self.field_variables[identifier].constructors_info[-1].constructor != self.current_constructor:
                    constructor_info = self.get_constructor_info_struct(
                        constructor=self.current_constructor
                    )
                    self.field_variables[identifier].constructors_info.append(constructor_info)

    def exitCompilationUnit(self, ctx:JavaParserLabeled.CompilationUnitContext):
        import_text = ''
        for interface in self.result['interfaces']:
            interface = interface.split('-')
            import_text += f"\nimport {interface[0]}.I{interface[2]};"
        self.token_stream_rewriter.insertAfter(
            self.last_import_token_index,
            import_text,
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME
        )


class Injection:
    def __init__(self, base_dirs, index_dic, files, class_diagram):
        self.base_dirs = base_dirs
        self.index_dic = index_dic
        self.index_dic_keys = list(index_dic.keys())
        self.files = files
        self.class_diagram = class_diagram

    def refactor(self):
        print('Start injection refactoring . . .')
        reports = {'case1': 0, 'case2': 0, 'case3': 0}
        interfaces = set()
        classes = dict()
        token_stream_rewriter_dict = dict()
        roots_long_name = [self.index_dic_keys[n] for n, d in self.class_diagram.in_degree() if d == 0]

        for f in self.files:
            parser, tokens = get_parser_and_tokens(f)
            tree = parser.compilationUnit()
            listener = ConstructorEditorListener(
                self.base_dirs,
                f,
                self.index_dic,
                roots_long_name,
                common_token_stream=tokens
            )
            walker = ParseTreeWalker()
            walker.walk(listener=listener, t=tree)
            # print("listener.statistics:", listener.statistics)
            interfaces = interfaces.union(listener.result['interfaces'])
            all_cases = 0
            for class_ in listener.statistics:
                all_cases += listener.statistics[class_]['case1'] + listener.statistics[class_]['case2']
                reports['case1'] += listener.statistics[class_]['case1']
                reports['case2'] += listener.statistics[class_]['case2']
            if all_cases > 0:
                for class_ in listener.result['classes']:
                    total_case = listener.statistics[class_]['case1'] + listener.statistics[class_]['case2']
                    if total_case != 0:
                        classes[class_] = listener.result['classes'][class_]

                # classes.update(listener)
                token_stream_rewriter_dict[f] = listener.token_stream_rewriter.getDefaultText()

        # add interfaces
        for interface in interfaces:
            class_name = interface.split('-')[-1]
            path = self.index_dic[interface]['path']
            self.create_injection_interface(path, class_name)

        self.prepare_injector(classes, list(self.index_dic))

        for path in token_stream_rewriter_dict:
            with open(r"" + path, mode='w', encoding='utf-8', newline='') as f:
                f.write(token_stream_rewriter_dict[path])

        print('End injection refactoring !')
        return reports


    def create_injection_interface(self, path, class_name):
        parser = get_parser(path)
        tree = parser.compilationUnit()
        listener = InterfaceInfoListener(
            class_name,
            self.base_dirs,
            path
        )
        walker = ParseTreeWalker()
        walker.walk(
            listener=listener,
            t=tree
        )
        interface_info = listener.get_interface_info()
        path_list = Path.convert_str_paths_to_list_paths([path])
        interface_info['path'] = '/'.join(path_list[0][:-1])
        ic = InterfaceCreator(interface_info)
        ic.save()
        ic.add_implement_statement_to_class(path)

    def find_injector_path(self, long_name):
        path = self.index_dic[long_name]['path']
        first_package = long_name.split('-')[0]
        first_package = first_package.split('.')[0]
        splitted_path = path.split('/')
        return '/'.join(splitted_path[:splitted_path.index(first_package) + 1]) + '/'

    def prepare_injector(self, classes, index_list):
        injector_path = self.find_injector_path(index_list[0])
        injector_name = 'Injector'

        injector = Injector(injector_name, injector_path, self.base_dirs, self.index_dic)
        injector.create(classes)
        injector.inject(index_list)


if __name__ == "__main__":
    project_name = '85_shop'
    java_project_address = config.projects_info[project_name]['path']
    base_dirs = config.projects_info[project_name]['base_dirs']
    files = File.find_all_file(java_project_address, 'java')
    index_dic_ = File.indexing_files_directory(files, 'class_index.json', base_dirs)
    #with open('class_index.json') as f:
    #    index_dic_ = json.load(f)
    cd = ClassDiagram(java_project_address, base_dirs, files, index_dic_)
    cd.make_class_diagram()
    # cd.set_stereotypes()
    # cd.save('class_diagram.gml')
    #cd.load('class_diagram.gml')
    # cd.show(cd.class_diagram_graph)
    g = cd.class_diagram_graph
    # g = cd.class_diagram_graph
    injection = Injection(base_dirs, index_dic_, files, cd.class_diagram_graph)
    reports = injection.refactor()
    print('reports:', reports)

    files = File.find_all_file(java_project_address, 'java')
    index_dic_ = File.indexing_files_directory(files, 'class_index.json', base_dirs)
    cd2 = ClassDiagram(java_project_address, base_dirs, files, index_dic_)
    cd2.make_class_diagram()
    # cd2.set_stereotypes()
    # cd2.show(cd2.class_diagram_graph)
