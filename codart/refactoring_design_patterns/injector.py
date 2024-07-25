from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from codart.gen.JavaParserLabeledListener import JavaParserLabeledListener
from codart.gen.JavaParserLabeled import JavaParserLabeled

from design_4_testability.utils.utils import get_parser, get_parser_and_tokens, Path
from design_4_testability import config


class CreatorListener(JavaParserLabeledListener):
    def __init__(self, base_dirs, index_dic, file_name, file, target_classes):
        self.constructors_info = dict()
        self.current_class = None
        self.__package = None
        self.__depth = 0
        self.imports_star = list()
        self.imports = list()

        self.target_classes = target_classes
        self.base_dirs = base_dirs
        self.file_name = file_name
        self.file = file
        self.index_dic = index_dic

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.__package = ctx.qualifiedName().getText()

    def enterImportDeclaration(self, ctx:JavaParserLabeled.ImportDeclarationContext):
        if '*' in ctx.getText():
            self.imports_star.append(ctx.qualifiedName().getText())
        else:
            self.imports.append(ctx.qualifiedName().getText())

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__depth += 1
        if self.__package is None:
            self.__package = Path.get_default_package(self.base_dirs, self.file)
        if self.__depth == 1:
            self.current_class = self.__package + '-' + self.file_name + '-' + ctx.IDENTIFIER().getText()
            if self.current_class in self.target_classes:
                self.constructors_info[self.current_class] = []

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__depth -= 1
        if self.__depth == 0:
            self.current_class = None

    def enterConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):
        if self.__depth == 1 and self.current_class in self.target_classes:
            formal_parameters = []
            if ctx.formalParameters().formalParameterList() is not None:
                for f in ctx.formalParameters().formalParameterList().formalParameter():
                    type_ = f.typeType().getText()
                    type_package, _ = Path.find_package_of_dependee(
                        type_,
                        self.imports,
                        self.imports_star,
                        self.index_dic,
                    )
                    if type_package:
                        type_ = f'{type_package}.{type_}'
                    identifier = f.variableDeclaratorId().getText()
                    formal_parameters.append({'type': type_, 'identifier': identifier})
            self.constructors_info[self.current_class].append(formal_parameters)


class InjectorListener(JavaParserLabeledListener):
    def __init__(self, base_dirs, index_dic,
                 file_name, file, supported_classes,
                 common_token_stream,
                 injector_package,
                 injector_name):
        self.current_class = None
        self.__package = None
        self.__depth = 0
        self.imports_star = list()
        self.imports = list()

        self.supported_classes = supported_classes
        self.base_dirs = base_dirs
        self.file_name = file_name
        self.file = file
        self.index_dic = index_dic
        self.injector_object_statement = injector_package + '.' + injector_name

        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.__package = ctx.qualifiedName().getText()

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        if '*' in ctx.getText():
            self.imports_star.append(ctx.qualifiedName().getText())
        else:
            self.imports.append(ctx.qualifiedName().getText())

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__depth += 1
        if self.__package is None:
            self.__package = Path.get_default_package(self.base_dirs, self.file)
        if self.__depth == 1:
            self.current_class = self.__package + '-' + self.file_name + '-' + ctx.IDENTIFIER().getText()

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__depth -= 1
        if self.__depth == 0:
            self.current_class = None

    def enterExpression4(self, ctx:JavaParserLabeled.Expression4Context):
        dependee = ctx.creator().createdName().getText()
        package, file_name = Path.find_package_of_dependee(
            dependee,
            self.imports,
            self.imports_star,
            self.index_dic,
        )
        dependee_long_name = f'{package}-{file_name}-{dependee.split(".")[-1]}'
        if dependee_long_name in self.supported_classes:
            injector_method_name = package.split('.') + [file_name, dependee.split('.')[-1]]
            injector_method_name = 'get_' + '_'.join(injector_method_name)
            self.token_stream_rewriter.replace(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.creator().createdName().stop.tokenIndex,
                text=self.injector_object_statement + '.' + injector_method_name
            )


class Injector:
    def __init__(self, name, path, base_dirs, index_dic):
        self.name = name
        self.path = path
        self.index_dic = index_dic
        self.base_dirs = base_dirs

        self.package = None
        self.supported_classes = list()

    # classes parameter is dictionary that keys are long name of class and values are their dependencies
    def create(self, classes: dict):
        classes_info = {}
        for class_ in classes:
            f = self.index_dic[class_]['path']
            file_name = Path.get_file_name_from_path(f)
            parser = get_parser(f)
            tree = parser.compilationUnit()
            listener = CreatorListener(
                self.base_dirs,
                self.index_dic,
                file_name,
                f,
                classes
            )
            walker = ParseTreeWalker()
            walker.walk(listener=listener, t=tree)
            for c in listener.constructors_info:
                classes_info[c] = []
                if len(listener.constructors_info[c]) > 0:
                    i = 0
                    for constructor in listener.constructors_info[c]:
                        classes_info[c].append({'params': constructor, 'dependencies': classes[c][i]})
                        i += 1
                else:
                    classes_info[c].append({'params': [], 'dependencies': classes[c][0]})

        self.__make_injector_body(classes_info)
        self.supported_classes = list(classes)

    def inject(self, classes: list):
        for class_ in classes:
            f = self.index_dic[class_]['path']
            file_name = Path.get_file_name_from_path(f)
            parser, tokens = get_parser_and_tokens(f)
            tree = parser.compilationUnit()
            listener = InjectorListener(
                self.base_dirs,
                self.index_dic,
                file_name,
                f,
                self.supported_classes,
                common_token_stream=tokens,
                injector_package=self.package,
                injector_name=self.name
            )
            walker = ParseTreeWalker()
            walker.walk(listener=listener, t=tree)

            with open(f, mode='w', newline='', encoding='utf8', errors='ignore') as f:
                f.write(listener.token_stream_rewriter.getDefaultText())

    def __make_injector_body(self, classes_info):
        text = ''

        # write package statement
        self.package = Path.get_default_package(self.base_dirs, self.path)
        text += f'package {self.package};\n'
        for class_ in classes_info:
            package, class_name, _ = class_.split('-')
            text += f'import {package}.{class_name};\n'

        class_body = ''
        # write methods statement
        for class_ in classes_info:
            for constructor in classes_info[class_]:
                splitted_class = class_.split('-')
                class_name = class_.replace('-', '_').replace('.', '_')
                method_params_statement = ''
                for param in constructor['params']:
                    method_params_statement += f'{param["type"]} {param["identifier"]},'
                method_params_statement = method_params_statement[:-1]
                # method_body = f'\t public static {splitted_class[0]}.{splitted_class[2]} get_{class_name}({method_params_statement})' + '{' + '\n'
                method_body = f'\t public static {splitted_class[2]} get_{class_name}({method_params_statement})' + '{' + '\n'

                dependee_number = 0
                dependees_params = []
                for dependee in constructor['dependencies']:
                    dependee_number += 1
                    splitted_dependee = dependee['type'].split('-')
                    dependee_name = f'dependee{dependee_number}'
                    dependees_params.append(dependee_name)
                    method_body += f'\t\t{".".join(splitted_dependee[:-1])} {dependee_name}'
                    # method_body += f' = new {splitted_dependee[0]}.{splitted_dependee[2]}('
                    method_body += f' = new {splitted_dependee[2]}('
                    method_body += ', '.join(dependee["arguments"]) + ');\n'

                # write method return statement
                method_body += f'\t\t{".".join(splitted_class[:-1])} obj'
                method_body += f' = new {splitted_class[0]}.{splitted_class[2]}('
                obj_params = [param['identifier'] for param in constructor['params']]
                method_body += ', '.join(dependees_params + obj_params) + ');\n'
                method_body += '\t\treturn obj;\n\t}'
                class_body += method_body + '\n\n'
        class_body = class_body[:-2]
        text += f'public class {self.name}\n' + '{\n' + class_body + '\n}'
        if class_body != '':
            with open(f'{self.path}{self.name}.java', mode='w', newline='', encoding='utf8', errors='ignore') as f:
                f.write(text)


from design_4_testability.utils.utils import File
if __name__ == '__main__':
    java_project = "JSON-java"
    java_project_address = config.projects_info[java_project]['path']
    print('java_project_address', java_project_address)
    base_dirs = config.projects_info[java_project]['base_dirs']
    print('base_dirs', base_dirs)
    files = File.find_all_file(java_project_address, 'java')
    print(files)
    index_dic = File.indexing_files_directory(files, 'class_index.json', base_dirs)
    # ?
    injector_path = 'benchmarks/javaproject/com/creator/'
    injector = Injector('Injector', injector_path, base_dirs, index_dic)
    classes = dict()
    for c in index_dic:
        classes[c] = [[{''}]]

    print('classes', classes)
    injector.create(classes)
    injector.inject(['com.creator-Creator-Creator'])
