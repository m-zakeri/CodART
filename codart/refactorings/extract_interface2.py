"""
## Introduction

The module implements a light version of extract interface refactoring described in `extract_interface.py`


## Pre and post-conditions

### Pre-conditions:

1. The interface should not be already exist.

2. precondition is whether the package name, all the class names and method names in
those classes exist.

3. The parameter types and return types of each method should be the same across the
classes.

### Post-conditions:

No specific post-condition

"""

__version__ = '0.1.2'
__author__ = 'Morteza Zakeri'

import os

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from codart.gen.javaLabeled.JavaLexer import JavaLexer
from codart.gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from codart.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from codart import config


class InterfaceInfoListener(JavaParserLabeledListener):
    def __init__(self):
        self.current_class = None
        self.interface_info = {'package': str(), 'name': str(), 'path': str(), 'methods': []}
        self.enter_method_body_stack = list()

    def enterMethodBody(self, ctx: JavaParserLabeled.MethodBodyContext):
        self.enter_method_body_stack.append(True)

    def exitMethodBody(self, ctx: JavaParserLabeled.MethodBodyContext):
        self.enter_method_body_stack.pop()

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.interface_info['package'] = ctx.qualifiedName().getText()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if len(self.interface_info['name']) > 0:
            return
        # Todo: requires better handling
        if not hasattr(ctx.parentCtx, 'classOrInterfaceModifier'):
            return
        if ctx.parentCtx.classOrInterfaceModifier() is not None:
            if len(ctx.parentCtx.classOrInterfaceModifier()) > 0:
                if ctx.parentCtx.classOrInterfaceModifier()[0].getText() == "public":
                    self.current_class = ctx.IDENTIFIER().getText()
                    self.interface_info['name'] = self.current_class
            else:
                self.current_class = ctx.IDENTIFIER().getText()
                self.interface_info['name'] = self.current_class

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.current_class = None

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if len(self.enter_method_body_stack) > 0:
            return
        if hasattr(ctx.parentCtx.parentCtx, 'modifier'):
            modifiers = ctx.parentCtx.parentCtx.modifier()
        else:
            modifiers = ctx.parentCtx.parentCtx.parentCtx.modifier()

        do_extract = True
        for modifier in modifiers:
            if modifier.classOrInterfaceModifier() is not None:
                # print('modifier.classOrInterfaceModifier().getText()', modifier.classOrInterfaceModifier().getText())

                # Todo: Requires better handling
                if "private" in modifier.classOrInterfaceModifier().getText() or \
                        "static" in modifier.classOrInterfaceModifier().getText() or \
                        '?' in modifier.classOrInterfaceModifier().getText():
                    do_extract = False
                    break

        # Todo: Requires better handling
        if '?' in ctx.getChild(0).getText():
            do_extract = False

        if do_extract:
            method = {'name': ctx.IDENTIFIER().getText(), 'return_type': ctx.typeTypeOrVoid().getText(),
                      'formal_parameters': []}
            if ctx.formalParameters().formalParameterList() is not None:
                if hasattr(ctx.formalParameters().formalParameterList(), 'formalParameter'):
                    for f in ctx.formalParameters().formalParameterList().formalParameter():
                        _type = f.typeType().getText()
                        identifier = f.variableDeclaratorId().getText()
                        method['formal_parameters'].append([_type, identifier])
            self.interface_info['methods'].append(method)

    def get_interface_info(self):
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
    def __init__(self, interface_info, class_path):
        self.interface_info = interface_info
        self.class_path = class_path

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

    def get_import_text(self):
        return self.interface_info['package'] + '.' + self.interface_info['name']

    def add_implement_statement_to_class(self, ):
        stream = FileStream(self.class_path, encoding='utf8', errors='ignore')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        listener = AddingImplementStatementToClass(
            common_token_stream=token_stream,
            class_name=os.path.splitext(os.path.basename(self.class_path))[0],
            interface_package=self.interface_info['package'],
            interface_name=self.interface_info['name']
        )
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=listener)

        with open(self.class_path, encoding='utf8', errors='ignore', mode='w', newline='') as f:
            f.write(listener.token_stream_rewriter.getDefaultText())

    def save(self):
        interface_text = self.make_interface_body()
        if self.interface_info['path'] == '':
            self.interface_info['path'] = os.path.dirname(self.class_path)
        with open(
                os.path.join(self.interface_info['path'], f"{self.interface_info['name']}.java"),
                encoding='utf8',
                errors='ignore',
                mode='w'
        ) as f:
            f.write(interface_text)


def main(class_path):
    """

    Args:

        class_path (str): The java file path containing the public class

    """

    # Precondition 1: The interface should not be already exist.
    interface_path = os.path.join(
        os.path.dirname(class_path),
        f'I{os.path.splitext(os.path.basename(class_path))[0]}.java'
    )
    if os.path.exists(interface_path):
        return False

    stream = FileStream(class_path, encoding='utf-8', errors='ignore')
    lexer = JavaLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    tree = parser.compilationUnit()

    listener = InterfaceInfoListener()

    walker = ParseTreeWalker()
    walker.walk(listener=listener, t=tree)

    interface_info_ = listener.get_interface_info()
    interface_info_['name'] = 'I' + interface_info_['name']
    interface_info_['path'] = os.path.dirname(class_path)

    ic = InterfaceCreator(interface_info_, class_path)
    ic.add_implement_statement_to_class()
    ic.save()
    return True


# Tests
if __name__ == "__main__":
    class_path1 = "benchmarks/simple_injection/src/calculator/Calculator.java"
    class_path2 = "benchmarks/10_water-simulator/src/main/java/simulator/SA/GridGenerator.java"
    class_path3 = os.path.join(
        config.PROJECT_PATH,
        "src\\net\\sourceforge\\ganttproject\\gui\\server\\ConnectionPanel.java")
    print(class_path3)
    main(class_path=class_path3)
