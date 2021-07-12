"""
The scripts implements different refactoring operations
"""
__version__ = '0.1.0'
__author__ = 'Morteza'

import networkx as nx

from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

import visualization.graph_visualization


class InlineClassRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(
            self, common_token_stream: CommonTokenStream = None,
            source_class: str = None, source_class_data: dict = None,
            target_class: str = None, target_class_data: dict = None, is_complete: bool = False):

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if source_class is None:
            raise ValueError("source_class is None")
        else:
            self.source_class = source_class
        if target_class is None:
            raise ValueError("new_class is None")
        else:
            self.target_class = target_class
        if target_class:
            self.target_class = target_class
        if source_class_data:
            self.source_class_data = source_class_data
        else:
            self.source_class_data = {'fields': [], 'methods': [], 'constructors': []}
        if target_class_data:
            self.target_class_data = target_class_data
        else:
            self.target_class_data = {'fields': [], 'methods': [], 'constructors': []}

        self.field_that_has_source = []
        self.has_source_new = False

        self.is_complete = is_complete
        self.is_target_class = False
        self.is_source_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:
            self.is_source_class = True
            self.is_target_class = False
        elif class_identifier == self.target_class:
            self.is_target_class = True
            self.is_source_class = False
        else:
            self.is_target_class = False
            self.is_source_class = False

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_target_class and (self.source_class_data['fields'] or
                                     self.source_class_data['constructors'] or
                                     self.source_class_data['methods']):
            if not self.is_complete:
                final_fields = merge_fields(self.source_class_data['fields'], self.target_class_data['fields'], self.target_class)
                final_constructors = merge_constructors(self.source_class_data['constructors'],
                                                        self.target_class_data['constructors'])
                final_methods = merge_methods(self.source_class_data['methods'], self.target_class_data['methods'])
                text = '\t'
                for field in final_fields:
                    text += field.text + '\n'
                for constructor in final_constructors:
                    text += constructor.text + '\n'
                for method in final_methods:
                    text += method.text + '\n'
                self.token_stream_rewriter.insertBeforeIndex(
                    index=ctx.stop.tokenIndex,
                    text=text
                )
                self.is_complete = True
                print(self.target_class_data['constructors'])
                print(final_constructors)
            else:
                self.is_target_class = False
        elif self.is_source_class:
            if ctx.parentCtx.classOrInterfaceModifier(0) == None:
                return
            self.is_source_class = False
            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.parentCtx.classOrInterfaceModifier(0).start.tokenIndex,
                to_idx=ctx.stop.tokenIndex
            )

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        if self.is_source_class:
            self.code += self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.start.tokenIndex + 1,
                stop=ctx.stop.tokenIndex - 1
            )
            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.parentCtx.start.tokenIndex,
                to_idx=ctx.parentCtx.stop.tokenIndex
            )
        else:
            return None

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if self.is_source_class or self.is_target_class:
            field_text = ''
            for child in ctx.children:
                if child.getText() == ';':
                    field_text = field_text[:len(field_text) - 1] + ';'
                    break
                field_text += child.getText() + ' '

            name = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText()

            if ctx.typeType().classOrInterfaceType() != None and ctx.typeType().classOrInterfaceType().getText() == self.source_class:
                self.field_that_has_source.append(name)
                return

            modifier_text = ''
            for modifier in ctx.parentCtx.parentCtx.modifier():
                modifier_text += modifier.getText() + ' '
            field_text = modifier_text + field_text
            if self.is_source_class:
                self.source_class_data['fields'].append(Field(name=name, text=field_text))
            else:
                self.target_class_data['fields'].append(Field(name=name, text=field_text))

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if self.is_target_class:
            if ctx.typeType().classOrInterfaceType().getText() == self.source_class:
                grand_parent_ctx = ctx.parentCtx.parentCtx
                self.token_stream_rewriter.delete(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=grand_parent_ctx.start.tokenIndex,
                    to_idx=grand_parent_ctx.stop.tokenIndex)



    def enterConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        if self.is_source_class or self.is_target_class:
            if ctx.formalParameters().formalParameterList():
                constructor_parameters = [ctx.formalParameters().formalParameterList().children[i] for i in
                                          range(len(ctx.formalParameters().formalParameterList().children)) if i % 2 == 0]
            else:
                constructor_parameters = []
            constructor_text = ''
            for modifier in ctx.parentCtx.parentCtx.modifier():
                constructor_text += modifier.getText() + ' '

            if self.is_source_class:
                constructor_text += self.target_class
            else:
                constructor_text += ctx.IDENTIFIER().getText()
            constructor_text += ' ( '
            for parameter in constructor_parameters:
                constructor_text += parameter.typeType().getText() + ' '
                constructor_text += parameter.variableDeclaratorId().getText() + ', '
            if constructor_parameters:
                constructor_text = constructor_text[:len(constructor_text) - 2]
            constructor_text += ')\n\t{'
            constructor_text += self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.block().start.tokenIndex + 1,
                stop=ctx.block().stop.tokenIndex - 1
            )
            constructor_text += '}\n'
            # print(constructor_text)
            # print("------")
            if self.is_source_class:
                self.source_class_data['constructors'].append(ConstructorOrMethod(
                    name=self.target_class, parameters=[Parameter(parameterType=p.typeType().getText(),
                                                                  name=p.variableDeclaratorId().IDENTIFIER().getText())
                                                        for p in constructor_parameters],
                    text=constructor_text, constructorBody=self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.block().start.tokenIndex + 1,
                stop=ctx.block().stop.tokenIndex - 1
                )))
            else:
                self.target_class_data['constructors'].append(ConstructorOrMethod(
                    name=self.target_class, parameters=[Parameter(parameterType=p.typeType().getText(),
                                                                  name=p.variableDeclaratorId().IDENTIFIER().getText())
                                                        for p in constructor_parameters],
                    text=constructor_text, constructorBody=self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.block().start.tokenIndex + 1,
                stop=ctx.block().stop.tokenIndex - 1
                )))

                # print("aaslkdjflksdjflksd")
                # print(self.source_class_data['constructors'])
                # print(self.target_class_data['constructors'][-1])
                # print("aaslkdjflks45345djflksd")
                proper_constructor = get_proper_constructor(self.target_class_data['constructors'][-1], self.source_class_data['constructors'])

                if proper_constructor == None:
                    return

                self.token_stream_rewriter.insertBeforeIndex(
                    index=ctx.stop.tokenIndex,
                    text=proper_constructor.constructorBody
                )

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_source_class or self.is_target_class:
            if ctx.formalParameters().formalParameterList():
                method_parameters = [ctx.formalParameters().formalParameterList().children[i] for i in
                                     range(len(ctx.formalParameters().formalParameterList().children)) if i % 2 == 0]
            else:
                method_parameters = []
            method_text = ''
            for modifier in ctx.parentCtx.parentCtx.modifier():
                method_text += modifier.getText() + ' '
            method_text += ctx.typeTypeOrVoid().getText() + ' ' + ctx.IDENTIFIER().getText()
            method_text += ' ( '
            for parameter in method_parameters:
                method_text += parameter.typeType().getText() + ' '
                method_text += parameter.variableDeclaratorId().getText() + ', '
            if method_parameters:
                method_text = method_text[:len(method_text) - 2]
            method_text += ')\n\t{'
            method_text += self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=ctx.methodBody().start.tokenIndex + 1,
                stop=ctx.methodBody().stop.tokenIndex - 1
            )
            method_text += '}\n'
            if self.is_source_class:
                self.source_class_data['methods'].append(ConstructorOrMethod(
                    name=ctx.IDENTIFIER().getText(),
                    parameters=[Parameter(
                        parameterType=p.typeType().getText(),
                        name=p.variableDeclaratorId().IDENTIFIER().getText())
                        for p in
                        method_parameters],
                    text=method_text))
            else:
                self.target_class_data['methods'].append(ConstructorOrMethod(
                    name=ctx.IDENTIFIER().getText(),
                    parameters=[Parameter(
                        parameterType=p.typeType().getText(),
                        name=p.variableDeclaratorId().IDENTIFIER().getText())
                        for p in
                        method_parameters],
                    text=method_text))


    def enterExpression1(self, ctx:JavaParserLabeled.Expression1Context):
        if ctx.IDENTIFIER().getText() in self.field_that_has_source:
            # print(dir(ctx.expression()))
            # print(ctx.expression().getText())
            field_text = ctx.expression().getText()
            # self.token_stream_rewriter.replaceIndex(
            #     index=ctx.start.tokenIndex,
            #     text=field_text
            # )

            self.token_stream_rewriter.replace(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex,
                text=field_text
            )

    def exitExpression21(self, ctx:JavaParserLabeled.Expression21Context):
        if self.has_source_new:
            self.has_source_new = False
            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.start.tokenIndex,
                to_idx=ctx.stop.tokenIndex
            )


    def enterExpression4(self, ctx:JavaParserLabeled.Expression4Context):
        if ctx.children[-1].children[0].getText() == self.source_class:
            self.has_source_new = True


    def enterCreatedName0(self, ctx: JavaParserLabeled.CreatedName0Context):
        if ctx.IDENTIFIER(0).getText() == self.source_class and self.target_class:
            self.token_stream_rewriter.replaceIndex(
                index=ctx.start.tokenIndex,
                text=self.target_class
            )

    def enterCreatedName1(self, ctx: JavaParserLabeled.CreatedName1Context):
        if ctx.getText() == self.source_class and self.target_class:
            self.token_stream_rewriter.replaceIndex(
                index=ctx.start.tokenIndex,
                text=self.target_class
            )

    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        class_type = ctx.typeType().classOrInterfaceType()
        if class_type:
            if class_type.IDENTIFIER(0).getText() == self.source_class and self.target_class:
                self.token_stream_rewriter.replaceIndex(
                    index=class_type.start.tokenIndex,
                    text=self.target_class
                )

    def enterQualifiedName(self, ctx: JavaParserLabeled.QualifiedNameContext):
        if ctx.IDENTIFIER(0).getText() == self.source_class and self.target_class:
            self.token_stream_rewriter.replaceIndex(
                index=ctx.start.tokenIndex,
                text=self.target_class
            )

    def exitExpression0(self, ctx: JavaParserLabeled.Expression0Context):
        if ctx.primary().getText() == self.source_class and self.target_class:
            self.token_stream_rewriter.replaceIndex(
                index=ctx.start.tokenIndex,
                text=self.target_class
            )

    def enterLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        if ctx.typeType().classOrInterfaceType():
            if ctx.typeType().classOrInterfaceType().getText() == self.source_class and self.target_class:
                self.token_stream_rewriter.replace(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=ctx.typeType().start.tokenIndex,
                    to_idx=ctx.typeType().stop.tokenIndex,
                    text=self.target_class
                )


class Field:
    def __init__(self, text: str = None, name: str = None, fieldType: str = None):
        self.text = text
        self.name = name
        self.fieldType = fieldType


class Parameter:
    def __init__(self, parameterType, name):
        self.parameterType = parameterType
        self.name = name


class ConstructorOrMethod:
    def __init__(self, text: str = None, name: str = None, parameters: Parameter = None, constructorBody: str = None):
        self.text = text
        self.name = name
        self.parameters = parameters
        self.constructorBody = constructorBody


def merge_fields(source_fields: Field, target_fields, target_class_type):
    final_fields = []
    target_field_names = [target_field.name for target_field in target_fields]
    for field in source_fields:
        if (field.name in target_field_names) or (field.fieldType == target_class_type):
            continue
        final_fields.append(field)
    return final_fields


def is_equal_constructor(first_constructor: ConstructorOrMethod, second_constructor: ConstructorOrMethod):
    if len(first_constructor.parameters) == len(
                        second_constructor.parameters):
                        second_constructor_params = [param.parameterType for param in second_constructor.parameters]
                        for param in first_constructor.parameters:
                            if param not in second_constructor_params:
                                # if first_constructor.text == second_constructor.text:
                                return True
    return False


def merge_constructors(source_constructors: ConstructorOrMethod, target_constructors: ConstructorOrMethod):
    final_constructors = []
    for source_constructor in source_constructors:
        flag = True
        for target_constructor in target_constructors:
            if source_constructor.name == target_constructor.name:
                if is_equal_constructor(source_constructor, target_constructor): # check equality of two constructor
                    flag = False
        if flag:
            final_constructors.append(source_constructor)
    return final_constructors


def merge_methods(source_methods: ConstructorOrMethod, target_methods: ConstructorOrMethod):
    final_methods = []
    for source_method in source_methods:
        flag = True
        for target_method in target_methods:
            if source_method.name == target_method.name:
                if len(source_method.parameters) == len(target_method.parameters):  # change equality of two methods
                    flag = False
        if flag:
            final_methods.append(source_method)
    return final_methods


def get_proper_constructor(target_constructor: ConstructorOrMethod, source_constructors: ConstructorOrMethod):

    for source_constructor in source_constructors:
        if is_equal_constructor(source_constructor, target_constructor):
            return source_constructor

    return None