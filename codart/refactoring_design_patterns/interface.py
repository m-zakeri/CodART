"""
The module implements extract interface refactoring
"""

__version__ = '0.1.1'
__author__ = 'Sadegh Jafari, Morteza Zakeri'

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from codart.gen.last.JavaParserLabeledListener import JavaParserLabeledListener
from codart.gen.last.JavaParserLabeled import JavaParserLabeled

from design_4_testability.utils.utils import Path, File, get_parser_and_tokens, get_parser
from design_4_testability import config



class InterfaceInfoListener(JavaParserLabeledListener):
    def __init__(self, class_name, base_dirs, class_path):
        self.class_name = class_name
        self.base_dirs = base_dirs
        self.class_path = class_path
        self.file_name = Path.get_file_name_from_path(class_path)

        self.current_class = None
        self.__depth = 0
        self.__package = None
        self.interface_info = {
            'package': str(),
            'name': f'I{class_name}',
            'path': f'{self.class_path[:-(len(self.file_name) + 5)]}I{self.file_name}_{class_name}.java',
            'methods': list()
        }

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.__package = ctx.qualifiedName().getText()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__depth += 1
        if self.__package is None:
            self.__package = Path.get_default_package(self.base_dirs, self.class_path)

        if self.__depth == 1:
            self.current_class = ctx.IDENTIFIER().getText()

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.__depth -= 1
        if self.__depth == 0:
            self.current_class = None

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.current_class == self.class_name:
            number_of_annotation_modifiers = 0
            can_add_to_interface = False
            if len(ctx.parentCtx.parentCtx.modifier()) == 0:
                can_add_to_interface = True
            else:
                for modifier in ctx.parentCtx.parentCtx.modifier():

                    if modifier.classOrInterfaceModifier() is not None:
                        if modifier.classOrInterfaceModifier().annotation() is not None:
                            number_of_annotation_modifiers += 1
                        if modifier.classOrInterfaceModifier().getText() == 'public':
                            can_add_to_interface = True
                            break

            if len(ctx.parentCtx.parentCtx.modifier()) == number_of_annotation_modifiers:
                can_add_to_interface = True

            if ctx.IDENTIFIER().getText() == 'main':
                can_add_to_interface = False

            if can_add_to_interface:
                method = {'name': ctx.IDENTIFIER().getText(), 'return_type': ctx.typeTypeOrVoid().getText(),
                          'formal_parameters': []}
                if ctx.formalParameters().formalParameterList() is not None:
                    for f in ctx.formalParameters().formalParameterList().formalParameter():
                        _type = f.typeType().getText()
                        identifier = f.variableDeclaratorId().getText()
                        method['formal_parameters'].append([_type, identifier])
                self.interface_info['methods'].append(method)

    def get_interface_info(self):
        self.interface_info['package'] = self.__package
        return self.interface_info


class AddingImplementStatementToClass(JavaParserLabeledListener):
    def __init__(self, common_token_stream, class_name, interface_package, interface_name):
        self.common_token_stream = common_token_stream
        self.class_name = class_name
        self.interface_package = interface_package
        self.interface_name = interface_name
        self.last_import_token_index = None
        self.implement_token_index = None
        self.implement_state = []

        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.last_import_token_index = ctx.stop.tokenIndex

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        self.last_import_token_index = ctx.stop.tokenIndex

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() == self.class_name:
            self.implement_token_index = ctx.IDENTIFIER().symbol.tokenIndex
            if ctx.EXTENDS() is not None:
                self.implement_state.append(ctx.EXTENDS().getText())
                self.implement_token_index = ctx.typeType().stop.tokenIndex
            if ctx.IMPLEMENTS() is not None:
                self.implement_state.append(ctx.IMPLEMENTS().getText())
                self.implement_token_index = ctx.typeList().typeType()[-1].stop.tokenIndex

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        import_text = f"\nimport {self.interface_package}.{self.interface_name};"
        self.token_stream_rewriter.insertAfter(
            self.last_import_token_index,
            import_text,
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME
        )

        if 'implements' in self.implement_state:
            implement_text = f",{self.interface_name}"
        else:
            implement_text = f" implements {self.interface_name}"

        self.token_stream_rewriter.insertAfter(
            self.implement_token_index,
            implement_text,
            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME
        )


class InterfaceCreator:
    def __init__(self, interface_info):
        self.interface_info = interface_info

    def make_interface_body(self):
        interface_text = 'package ' + self.interface_info['package'] + ';\n'
        interface_text += "public interface " + self.interface_info['name'] + "{"
        for method in self.interface_info['methods']:
            interface_text += "\n\t" + 'public ' + method['return_type'] + ' ' + method['name'] + '('
            for formalParameter in method['formal_parameters']:
                interface_text += formalParameter[0] + ' ' + formalParameter[1] + ', '
            if method['formal_parameters']:
                interface_text = interface_text[:-2]
            interface_text += ');'
        interface_text += "\n}\n\n"
        return interface_text

    def save(self):
        interface_text = self.make_interface_body()
        with open(self.interface_info['path'] + '/' + self.interface_info['name'] + '.java', mode='w') as f:
            f.write(interface_text)

    def get_import_text(self):
        return self.interface_info['package'] + '.' + self.interface_info['name']

    def add_implement_statement_to_class(self, class_path):
        parser, token_stream = get_parser_and_tokens(class_path)
        parse_tree = parser.compilationUnit()
        listener = AddingImplementStatementToClass(
            common_token_stream=token_stream,
            class_name=Path.get_file_name_from_path(class_path),
            interface_package=self.interface_info['package'],
            interface_name=self.interface_info['name']
        )
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=listener)

        with open(class_path, mode='w', newline='') as f:
            f.write(listener.token_stream_rewriter.getDefaultText())


class InterfaceAdapter:
    @staticmethod
    def convert_factory_info_to_interface_info(factory_info, base_dirs, name):
        interface_info = {'name': name}
        all_paths = [factory_info['factory']['path']]
        for product_info in factory_info['products']['classes']:
            all_paths.append(product_info['path'])
        path = Path.detect_path(Path.convert_str_paths_to_list_paths(set(all_paths)))
        interface_info['path'] = path
        package = Path.get_default_package(base_dirs, path + '/' + name + '.java')
        interface_info['package'] = package
        interface_info['methods'] = factory_info['products']['methods']
        return interface_info


def get_default_interface_info(class_long_name, index_dic, base_dirs):
    if index_dic[class_long_name]['type'] == 'class':
        class_path = index_dic[class_long_name]['path']
        class_name = class_long_name.split('-')[-1]
        parser = get_parser(class_path)
        tree = parser.compilationUnit()
        listener = InterfaceInfoListener(class_name, base_dirs, class_path)
        walker = ParseTreeWalker()
        walker.walk(listener=listener, t=tree)
        return listener.get_interface_info()


if __name__ == "__main__":
    java_project = "JSON-java"
    java_project_address = config.projects_info[java_project]['path']
    print('java_project_address', java_project_address)
    base_dirs = config.projects_info[java_project]['base_dirs']
    print('base_dirs', base_dirs)
    files = File.find_all_file(java_project_address, 'java')
    index_dic = File.indexing_files_directory(files, 'class_index.json', base_dirs)
    # ?
    interface_info = get_default_interface_info('com.products-GifReader-GifReader',
                                     index_dic, base_dirs)

    ic = InterfaceCreator(interface_info)
    print(ic.make_interface_body())
