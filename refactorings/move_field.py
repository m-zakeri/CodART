from gen.java.JavaParser import JavaParser
from gen.java.JavaParserListener import JavaParserListener

from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from gen.java.JavaLexer import JavaLexer
from refactorings.utils.utils_listener_fast import ExpressionName, MethodInvocation, LocalVariable, Field, UtilsListener

from pathlib import Path
from typing import Union, List, Callable

import os


class FieldUsageListener(UtilsListener):
    """
    FieldUsageListener finds all the usage of
    an specified field f, from a class c in
    package pkg.
    """

    def __init__(self, filename: str, source_class: str, source_package: str, target_class: str, target_package: str,
                 field_name: str, field_candidates: set, field_tobe_moved: Field):
        super().__init__(filename)
        self.source_class = source_class
        self.source_package = source_package
        self.target_class = target_class
        self.target_package = target_package
        self.field_name = field_name
        self.has_imported_source = False
        self.has_imported_target = False
        self.usages = []
        # current class name is the public class in each file.
        self.current_class_name = ""
        self.field_candidates = field_candidates
        self.rewriter = None
        # this represents the text to be added in target i.e. public int a;
        self.field_tobe_moved = field_tobe_moved
        self.methods_tobe_updated = []

    def enterCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
        super().enterCompilationUnit(ctx)
        self.rewriter = TokenStreamRewriter(ctx.parser.getTokenStream())

    def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        super().enterClassDeclaration(ctx)

        if ctx.parentCtx.classOrInterfaceModifier()[0].getText() == "public":
            self.current_class_name = ctx.IDENTIFIER().getText()
        else:
            return

        self.has_imported_source = self.file_info.has_imported_package(self.package.name) or \
                                   self.file_info.has_imported_class(self.package.name, self.source_class)

        # import target if we're not in Target and have not imported before
        if self.current_class_name != self.target_class:
            self.rewriter.insertBeforeIndex(ctx.parentCtx.start.tokenIndex,
                                            f"import {self.target_package}.{self.target_class};\n")

    def enterClassBody(self, ctx: JavaParser.ClassBodyContext):
        super().exitClassBody(ctx)
        if self.current_class_name == self.target_class:
            replacement_text = ""
            if self.field_tobe_moved.name == self.field_name:
                for mod in self.field_tobe_moved.modifiers:
                    replacement_text += f"{mod} "
                replacement_text += f"{self.field_tobe_moved.datatype} {self.field_tobe_moved.name};"
            self.rewriter.insertAfter(ctx.start.tokenIndex, f"\n\t{replacement_text}\n")

            # add getter and setter
            name = self.field_tobe_moved.name
            method_name = self.field_tobe_moved.name.upper() + self.field_tobe_moved.name[1:-1]
            type = self.field_tobe_moved.datatype

            getter = f"\tpublic {type} get{method_name}() {{ return this.{name}; }}\n"
            setter = f"\tpublic void set{method_name}({type} {name}) {{ this.{name} = {name}; }}\n"
            self.rewriter.insertBeforeIndex(ctx.stop.tokenIndex, getter)
            self.rewriter.insertBeforeIndex(ctx.stop.tokenIndex, setter)

    def exitFieldDeclaration(self, ctx: JavaParser.FieldDeclarationContext):
        super().exitFieldDeclaration(ctx)
        if self.current_class_name != self.source_class:
            return

        if self.field_tobe_moved is None:
            field = self.package.classes[self.current_class_name].fields[
                ctx.variableDeclarators().children[0].children[0].IDENTIFIER().getText()]
            if field.name == self.field_name:
                self.field_tobe_moved = field

    def exitClassBody(self, ctx: JavaParser.ClassBodyContext):
        super().exitClassBody(ctx)
        save(self.rewriter, self.filename)

    def exitMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        super().exitMethodDeclaration(ctx)
        # we will remove getter and setter from source
        # and add it to target so there is no need to
        # find usages there

        if self.current_class_name == self.source_class and \
                self.is_method_getter_or_setter(ctx.IDENTIFIER().getText()):
            self.rewriter.replaceRange(
                ctx.parentCtx.parentCtx.start.tokenIndex,
                ctx.parentCtx.parentCtx.stop.tokenIndex, "")

    def exitConstructorDeclaration(self, ctx: JavaParser.ConstructorDeclarationContext):
        self.current_method.name = ctx.IDENTIFIER().getText()
        self.current_method.returntype = self.current_method.class_name
        self.handleMethodUsage(ctx, True)
        super().exitConstructorDeclaration(ctx)

    def exitMethodBody(self, ctx: JavaParser.MethodBodyContext):
        super().exitMethodBody(ctx)
        self.handleMethodUsage(ctx, False)

    def handleMethodUsage(self, ctx, is_constructor: bool):
        method_identifier = ctx.IDENTIFIER().getText() if is_constructor else ctx.parentCtx.IDENTIFIER().getText()
        formal_params = ctx.formalParameters() if is_constructor else ctx.parentCtx.formalParameters()
        target_added = False
        target_param_name = "$$target"
        target_param = f"Target {target_param_name}" if \
            len(self.current_method.parameters) == 0 \
            else f", Target {target_param_name}"

        # if we have not imported source package or
        # Source class just ignore this
        if not self.has_imported_source:
            return

        local_candidates = set()
        if self.current_class_name == self.source_class:
            # we will remove getter and setter from source
            # and add it to target so there is no need to
            # find usages there
            if self.is_method_getter_or_setter(method_identifier):
                self.rewriter.replaceRange(ctx.start.tokenIndex, ctx.stop.tokenIndex, "")
                return
            local_candidates.add("this")

        # find parameters with type Source
        for t, identifier in self.current_method.parameters:
            if t == self.source_class:
                local_candidates.add(identifier)

        # find all local variables with type Source
        for var_or_exprs in self.current_method.body_local_vars_and_expr_names:
            if type(var_or_exprs) is LocalVariable:
                if var_or_exprs.datatype == self.source_class:
                    local_candidates.add(var_or_exprs.identifier)

        should_ignore = False

        for var_or_exprs in self.current_method.body_local_vars_and_expr_names:
            if type(var_or_exprs) is ExpressionName:
                # we're going to find source.field
                try:
                    local_ctx = var_or_exprs.parser_context.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx
                    creator = local_ctx.expression()[0].getText()
                    if creator.__contains__(
                            f"new{self.source_class}") and local_ctx.IDENTIFIER().getText() == self.field_name:
                        self.propagate_field(local_ctx, target_param_name)

                except:
                    pass

                if len(var_or_exprs.dot_separated_identifiers) < 2:
                    continue
                if (var_or_exprs.dot_separated_identifiers[0] in local_candidates or
                    var_or_exprs.dot_separated_identifiers[0] in self.field_candidates) and \
                        var_or_exprs.dot_separated_identifiers[1] == self.field_name:
                    if not target_added:
                        # add target to param
                        self.rewriter.insertBeforeIndex(formal_params.stop.tokenIndex,
                                                        target_param)
                        self.methods_tobe_updated.append(self.current_method)
                        target_added = True

                    self.usages.append(var_or_exprs.parser_context)
                    self.propagate_field(var_or_exprs.parser_context, target_param_name)

            elif type(var_or_exprs) is MethodInvocation:
                # we are going to find getter or setters
                # if len(var_or_exprs.dot_separated_identifiers) < 2:
                #     continue
                if var_or_exprs.dot_separated_identifiers[0] == f"new{self.source_class}":
                    if var_or_exprs.parser_context.methodCall() is not None and \
                            self.is_method_getter_or_setter(
                                var_or_exprs.parser_context.methodCall().IDENTIFIER().getText()):
                        self.propagate_getter_setter(var_or_exprs.parser_context, target_param_name)
                elif self.is_method_getter_or_setter(var_or_exprs.dot_separated_identifiers[0]):
                    if not target_added:
                        # add target to param
                        self.rewriter.insertBeforeIndex(formal_params.stop.tokenIndex,
                                                        target_param)
                        self.methods_tobe_updated.append(self.current_method)
                        target_added = True
                    if not should_ignore and var_or_exprs.parser_context is not None and type(
                            var_or_exprs.parser_context) is not JavaParser.ExpressionContext:
                        continue
                    self.usages.append(var_or_exprs.parser_context)
                    self.propagate_getter_setter_form2(var_or_exprs.parser_context, target_param_name)
                elif len(var_or_exprs.dot_separated_identifiers) > 1 and self.is_getter_or_setter(
                        var_or_exprs.dot_separated_identifiers[0],
                        var_or_exprs.dot_separated_identifiers[1], local_candidates):
                    if not target_added:
                        # add target to param
                        self.rewriter.insertBeforeIndex(formal_params.stop.tokenIndex,
                                                        target_param)
                        self.methods_tobe_updated.append(self.current_method)
                        target_added = True

                    self.usages.append(var_or_exprs.parser_context)
                    self.propagate_getter_setter(var_or_exprs.parser_context, target_param_name)

    def is_getter_or_setter(self, first_id: str, second_id: str, local_candidates: set):
        return (first_id in local_candidates or first_id in self.field_candidates) and (
                second_id == f"set{self.field_name[0].upper() + self.field_name[1:-1]}" or
                second_id == f"get{self.field_name[0].upper() + self.field_name[1:-1]}" or
                second_id == f"has{self.field_name[0].upper() + self.field_name[1:-1]}" or
                second_id == f"is{self.field_name[0].upper() + self.field_name[1:-1]}"
        )

    def is_method_getter_or_setter(self, method: str):
        return (
                method == f"set{self.field_name[0].upper() + self.field_name[1:-1]}" or
                method == f"get{self.field_name[0].upper() + self.field_name[1:-1]}" or
                method == f"has{self.field_name[0].upper() + self.field_name[1:-1]}" or
                method == f"is{self.field_name[0].upper() + self.field_name[1:-1]}"
        )

    def propagate_getter_setter(self, ctx: JavaParser.ExpressionContext, target_name: str):
        index = ctx.DOT().symbol.tokenIndex
        self.rewriter.replaceRange(ctx.start.tokenIndex, index - 1, target_name)

    def propagate_getter_setter_form2(self, ctx: JavaParser.ExpressionContext, target_name: str):
        """
        form 2 is getA() setA()...
        """
        self.rewriter.insertBeforeIndex(ctx.start.tokenIndex, f"{target_name}.")

    def propagate_field(self, ctx: JavaParser.ExpressionContext, target_name: str):
        index = ctx.DOT().symbol.tokenIndex
        self.rewriter.replaceRange(ctx.start.tokenIndex, index - 1, target_name)


def save(rewriter: TokenStreamRewriter, file_name: str, filename_mapping=lambda x: x + ".rewritten.java"):
    new_filename = filename_mapping(file_name).replace("\\", "/")
    path = new_filename[:new_filename.rfind('/')]
    if not os.path.exists(path):
        os.makedirs(path)
    with open(new_filename, mode='w', newline='') as file:
        print("write?", new_filename)
        file.write(rewriter.getDefaultText())


class MethodUsageListener(UtilsListener):
    def __init__(self, filename: str, methods: str, target_class: str):
        super().__init__(filename)
        self.methods = methods
        self.method_names = set(map(lambda m: m.name, methods))
        self.rewriter = None
        self.target_class = target_class

    def enterCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
        super().enterCompilationUnit(ctx)
        self.rewriter = TokenStreamRewriter(ctx.parser.getTokenStream())

    def enterClassCreatorRest(self, ctx: JavaParser.ClassCreatorRestContext):
        if type(ctx.parentCtx) is JavaParser.CreatorContext:
            if ctx.parentCtx.createdName().IDENTIFIER()[0].getText() not in self.method_names:
                return
        text = f"new {self.target_class}()" if ctx.arguments().expressionList() is None else f", new {self.target_class}()"
        index = ctx.arguments().RPAREN().symbol.tokenIndex
        self.rewriter.insertBeforeIndex(index, text)

    def exitMethodCall(self, ctx: JavaParser.MethodCallContext):
        super().exitMethodCall(ctx)
        if ctx.THIS() is not None:
            return
        if ctx.IDENTIFIER().getText() in self.method_names:
            text = f"new {self.target_class}()" if ctx.expressionList() is None else f", new {self.target_class}()"
            self.rewriter.insertBeforeIndex(ctx.RPAREN().symbol.tokenIndex, text)

    def exitClassBody(self, ctx: JavaParser.ClassBodyContext):
        super().exitClassBody(ctx)
        save(self.rewriter, self.filename)


def get_filenames_in_dir(directory_name: str, filter=lambda x: x.endswith(".java")) -> list:
    result = []
    for (dirname, dirnames, filenames) in os.walk(directory_name):
        result.extend([dirname + '/' + name for name in filenames if filter(name)])
    return result


def clean_up_dir(files: list) -> list:
    """
    :param files: List of files in the project directory
    :return: list

    Cleans up trashed files and gives original files
    """

    original_files = list()
    for file in files:
        if "rewritten.java" in file:
            os.remove(file)
        else:
            original_files.append(file)
    return original_files


class PreConditionListener(UtilsListener):
    def __init__(self, filename):
        super().__init__(filename)
        self.can_convert = True

    def enterInterfaceDeclaration(self, ctx: JavaParser.InterfaceDeclarationContext):
        super().enterInterfaceDeclaration(ctx)
        if ctx.INTERFACE() is not None:
            self.can_convert = False

    def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        super().enterClassDeclaration(ctx)
        if self.nest_count > 0:
            self.can_convert = False

    def exitMethodBody(self, ctx: JavaParser.MethodBodyContext):
        super().exitMethodBody(ctx)
        if self.current_method is None:
            self.can_convert = False


# class FieldUsageListener(UtilsListener):
#     """
#     FieldUsageListener finds all the usage of
#     an specified field f, from a class c in
#     package pkg.
#     """
#
#     def __init__(self, filename: str, source_class: str, source_package: str, target_class: str, target_package: str,
#                  field_name: str, field_candidates: set, field_tobe_moved: Field):
#         super().__init__(filename)
#         self.source_class = source_class
#         self.source_package = source_package
#         self.target_class = target_class
#         self.target_package = target_package
#         self.field_name = field_name
#         self.has_imported_source = False
#         self.has_imported_target = False
#         self.usages = []
#         # current class name is the public class in each file.
#         self.current_class_name = ""
#         self.field_candidates = field_candidates
#         self.rewriter = None
#         # this represents the text to be added in target i.e. public int a;
#         self.field_tobe_moved = field_tobe_moved
#         self.methods_tobe_updated = []
#
#     def enterCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
#         super().enterCompilationUnit(ctx)
#         self.rewriter = TokenStreamRewriter(ctx.parser.getTokenStream())
#
#     def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
#         super().enterClassDeclaration(ctx)
#
#         if ctx.parentCtx.classOrInterfaceModifier()[0].getText() == "public":
#             self.current_class_name = ctx.IDENTIFIER().getText()
#         else:
#             return
#
#         self.has_imported_source = self.file_info.has_imported_package(self.package.name) or \
#             self.file_info.has_imported_class(self.package.name, self.source_class)
#
#         # import target if we're not in Target and have not imported before
#         if self.current_class_name != self.target_class:
#             self.rewriter.insertBeforeIndex(ctx.parentCtx.start.tokenIndex,
#                                             f"import {self.target_package}.{self.target_class};\n")
#
#     def enterClassBody(self, ctx: JavaParser.ClassBodyContext):
#         super().exitClassBody(ctx)
#         if self.current_class_name == self.target_class:
#             replacement_text = ""
#             if self.field_tobe_moved.name == self.field_name:
#                 for mod in self.field_tobe_moved.modifiers:
#                     replacement_text += f"{mod} "
#                 replacement_text += f"{self.field_tobe_moved.datatype} {self.field_tobe_moved.name};"
#             self.rewriter.insertAfter(ctx.start.tokenIndex, f"\n\t{replacement_text}\n")
#
#             # add getter and setter
#             name = self.field_tobe_moved.name
#             method_name = self.field_tobe_moved.name.upper() + self.field_tobe_moved.name[1:-1]
#             type = self.field_tobe_moved.datatype
#
#             getter = f"\tpublic {type} get{method_name}() {{ return this.{name}; }}\n"
#             setter = f"\tpublic void set{method_name}({type} {name}) {{ this.{name} = {name}; }}\n"
#             self.rewriter.insertBeforeIndex(ctx.stop.tokenIndex, getter)
#             self.rewriter.insertBeforeIndex(ctx.stop.tokenIndex, setter)
#
#     def exitFieldDeclaration(self, ctx: JavaParser.FieldDeclarationContext):
#         super().exitFieldDeclaration(ctx)
#         if self.current_class_name != self.source_class:
#             return
#
#         if self.field_tobe_moved is None:
#             field = self.package.classes[self.current_class_name].fields[
#                 ctx.variableDeclarators().children[0].children[0].IDENTIFIER().getText()]
#             if field.name == self.field_name:
#                 self.field_tobe_moved = field
#
#     def exitClassBody(self, ctx: JavaParser.ClassBodyContext):
#         super().exitClassBody(ctx)
#
#     def exitMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
#         super().exitMethodDeclaration(ctx)
#         # we will remove getter and setter from source
#         # and add it to target so there is no need to
#         # find usages there
#
#         if self.current_class_name == self.source_class and \
#                 self.is_method_getter_or_setter(ctx.IDENTIFIER().getText()):
#             self.rewriter.replaceRange(
#                 ctx.parentCtx.parentCtx.start.tokenIndex,
#                 ctx.parentCtx.parentCtx.stop.tokenIndex, "")
#
#     def exitConstructorDeclaration(self, ctx: JavaParser.ConstructorDeclarationContext):
#         self.current_method.name = ctx.IDENTIFIER().getText()
#         self.current_method.returntype = self.current_method.class_name
#         self.handleMethodUsage(ctx, True)
#         super().exitConstructorDeclaration(ctx)
#
#     def exitMethodBody(self, ctx: JavaParser.MethodBodyContext):
#         super().exitMethodBody(ctx)
#         self.handleMethodUsage(ctx, False)
#
#     def handleMethodUsage(self, ctx, is_constructor: bool):
#         method_identifier = ctx.IDENTIFIER().getText() if is_constructor else ctx.parentCtx.IDENTIFIER().getText()
#         formal_params = ctx.formalParameters() if is_constructor else ctx.parentCtx.formalParameters()
#         target_added = False
#         target_param_name = "$$target"
#         target_param = f"Target {target_param_name}" if \
#             len(self.current_method.parameters) == 0 \
#             else f", Target {target_param_name}"
#
#         # if we have not imported source package or
#         # Source class just ignore this
#         if not self.has_imported_source:
#             return
#
#         local_candidates = set()
#         if self.current_class_name == self.source_class:
#             # we will remove getter and setter from source
#             # and add it to target so there is no need to
#             # find usages there
#             if self.is_method_getter_or_setter(method_identifier):
#                 self.rewriter.replaceRange(ctx.start.tokenIndex, ctx.stop.tokenIndex, "")
#                 return
#             local_candidates.add("this")
#
#         # find parameters with type Source
#         for t, identifier in self.current_method.parameters:
#             if t == self.source_class:
#                 local_candidates.add(identifier)
#
#         # find all local variables with type Source
#         for var_or_exprs in self.current_method.body_local_vars_and_expr_names:
#             if type(var_or_exprs) is LocalVariable:
#                 if var_or_exprs.datatype == self.source_class:
#                     local_candidates.add(var_or_exprs.identifier)
#
#         should_ignore = False
#
#         for var_or_exprs in self.current_method.body_local_vars_and_expr_names:
#             if type(var_or_exprs) is ExpressionName:
#                 # we're going to find source.field
#                 try:
#                     local_ctx = var_or_exprs.parser_context.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx
#                     creator = local_ctx.expression()[0].getText()
#                     if creator.__contains__(
#                             f"new{self.source_class}") and local_ctx.IDENTIFIER().getText() == self.field_name:
#                         self.propagate_field(local_ctx, target_param_name)
#
#                 except:
#                     pass
#
#                 if len(var_or_exprs.dot_separated_identifiers) < 2:
#                     continue
#                 if (var_or_exprs.dot_separated_identifiers[0] in local_candidates or
#                     var_or_exprs.dot_separated_identifiers[0] in self.field_candidates) and \
#                         var_or_exprs.dot_separated_identifiers[1] == self.field_name:
#                     if not target_added:
#                         # add target to param
#                         self.rewriter.insertBeforeIndex(formal_params.stop.tokenIndex,
#                                                         target_param)
#                         self.methods_tobe_updated.append(self.current_method)
#                         target_added = True
#
#                     self.usages.append(var_or_exprs.parser_context)
#                     self.propagate_field(var_or_exprs.parser_context, target_param_name)
#
#             elif type(var_or_exprs) is MethodInvocation:
#                 # we are going to find getter or setters
#                 # if len(var_or_exprs.dot_separated_identifiers) < 2:
#                 #     continue
#                 if var_or_exprs.dot_separated_identifiers[0] == f"new{self.source_class}":
#                     if var_or_exprs.parser_context.methodCall() is not None and \
#                             self.is_method_getter_or_setter(
#                                 var_or_exprs.parser_context.methodCall().IDENTIFIER().getText()):
#                         self.propagate_getter_setter(var_or_exprs.parser_context, target_param_name)
#                 elif self.is_method_getter_or_setter(var_or_exprs.dot_separated_identifiers[0]):
#                     if not target_added:
#                         # add target to param
#                         self.rewriter.insertBeforeIndex(formal_params.stop.tokenIndex,
#                                                         target_param)
#                         self.methods_tobe_updated.append(self.current_method)
#                         target_added = True
#                     if not should_ignore and var_or_exprs.parser_context is not None and type(
#                             var_or_exprs.parser_context) is not JavaParser.ExpressionContext:
#                         continue
#                     self.usages.append(var_or_exprs.parser_context)
#                     self.propagate_getter_setter_form2(var_or_exprs.parser_context, target_param_name)
#                 elif len(var_or_exprs.dot_separated_identifiers) > 1 and self.is_getter_or_setter(
#                         var_or_exprs.dot_separated_identifiers[0],
#                         var_or_exprs.dot_separated_identifiers[1], local_candidates):
#                     if not target_added:
#                         # add target to param
#                         self.rewriter.insertBeforeIndex(formal_params.stop.tokenIndex,
#                                                         target_param)
#                         self.methods_tobe_updated.append(self.current_method)
#                         target_added = True
#
#                     self.usages.append(var_or_exprs.parser_context)
#                     self.propagate_getter_setter(var_or_exprs.parser_context, target_param_name)
#
#     def is_getter_or_setter(self, first_id: str, second_id: str, local_candidates: set):
#         return (first_id in local_candidates or first_id in self.field_candidates) and (
#             second_id == f"set{self.field_name[0].upper() + self.field_name[1:-1]}" or
#             second_id == f"get{self.field_name[0].upper() + self.field_name[1:-1]}" or
#             second_id == f"has{self.field_name[0].upper() + self.field_name[1:-1]}" or
#             second_id == f"is{self.field_name[0].upper() + self.field_name[1:-1]}"
#         )
#
#     def is_method_getter_or_setter(self, method: str):
#         return (
#             method == f"set{self.field_name[0].upper() + self.field_name[1:-1]}" or
#             method == f"get{self.field_name[0].upper() + self.field_name[1:-1]}" or
#             method == f"has{self.field_name[0].upper() + self.field_name[1:-1]}" or
#             method == f"is{self.field_name[0].upper() + self.field_name[1:-1]}"
#         )
#
#     def propagate_getter_setter(self, ctx: JavaParser.ExpressionContext, target_name: str):
#         index = ctx.DOT().symbol.tokenIndex
#         self.rewriter.replaceRange(ctx.start.tokenIndex, index - 1, target_name)
#
#     def propagate_getter_setter_form2(self, ctx: JavaParser.ExpressionContext, target_name: str):
#         """
#         form 2 is getA() setA()...
#         """
#         self.rewriter.insertBeforeIndex(ctx.start.tokenIndex, f"{target_name}.")
#
#     def propagate_field(self, ctx: JavaParser.ExpressionContext, target_name: str):
#         index = ctx.DOT().symbol.tokenIndex
#         self.rewriter.replaceRange(ctx.start.tokenIndex, index - 1, target_name)
#
#     def save(self, override: bool, filename_mapping=lambda x: x.replace(".java", ".rewritten.java")):
#         if not override:
#             new_filename = filename_mapping(self.filename).replace("\\", "/")
#         else:
#             new_filename = self.filename
#         path = new_filename[:new_filename.rfind('/')]
#         if not os.path.exists(path):
#             os.makedirs(path)
#         with open(new_filename, mode='w', newline='') as file:
#             file.write(self.rewriter.getDefaultText())
#
#
# class MethodUsageListener(UtilsListener):
#     def __init__(self, filename: str, methods: str, target_class: str):
#         super().__init__(filename)
#         self.methods = methods
#         self.method_names = set(map(lambda m: m.name, methods))
#         self.rewriter = None
#         self.target_class = target_class
#
#     def enterCompilationUnit(self, ctx: JavaParser.CompilationUnitContext):
#         super().enterCompilationUnit(ctx)
#         self.rewriter = TokenStreamRewriter(ctx.parser.getTokenStream())
#
#     def enterClassCreatorRest(self, ctx: JavaParser.ClassCreatorRestContext):
#         if type(ctx.parentCtx) is JavaParser.CreatorContext:
#             if ctx.parentCtx.createdName().IDENTIFIER()[0].getText() not in self.method_names:
#                 return
#         text = f"new {self.target_class}()" if ctx.arguments(
#         ).expressionList() is None else f", new {self.target_class}()"
#         index = ctx.arguments().RPAREN().symbol.tokenIndex
#         self.rewriter.insertBeforeIndex(index, text)
#
#     def exitMethodCall(self, ctx: JavaParser.MethodCallContext):
#         super().exitMethodCall(ctx)
#         if ctx.THIS() is not None:
#             return
#         if ctx.IDENTIFIER().getText() in self.method_names:
#             text = f"new {self.target_class}()" if ctx.expressionList() is None else f", new {self.target_class}()"
#             self.rewriter.insertBeforeIndex(ctx.RPAREN().symbol.tokenIndex, text)
#
#     def save(self, override: bool, filename_mapping=lambda x: x.replace(".java", ".rewritten.java")):
#
#         if not override:
#             new_filename = filename_mapping(self.filename).replace("\\", "/")
#         else:
#             new_filename = self.filename
#         path = new_filename[:new_filename.rfind('/')]
#         if not os.path.exists(path):
#             os.makedirs(path)
#         with open(new_filename, mode='w', newline='') as file:
#             file.write(self.rewriter.getDefaultText())
#
#
# class PreConditionListener(UtilsListener):
#     def __init__(self, filename):
#         super().__init__(filename)
#         self.can_convert = True
#
#     def enterInterfaceDeclaration(self, ctx: JavaParser.InterfaceDeclarationContext):
#         super().enterInterfaceDeclaration(ctx)
#         if ctx.INTERFACE() is not None:
#             self.can_convert = False
#
#     def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
#         super().enterClassDeclaration(ctx)
#         if self.nest_count > 0:
#             self.can_convert = False
#
#     def exitMethodBody(self, ctx: JavaParser.MethodBodyContext):
#         super().exitMethodBody(ctx)
#         if self.current_method is None:
#             self.can_convert = False


class MoveField:

    def __init__(self,
                 src_package: str,
                 src_class: str,
                 field_name: str,
                 target_package: str,
                 target_class: str,
                 project_dir: Union[str, Path],
                 override: bool = False,
                 filename_map: Callable = lambda x: x + ".rewritten.java"
                 ) -> None:

        self.src_package = src_package
        self.src_class = src_class
        self.field_name = field_name
        self.target_package = target_package
        self.target_class = target_class
        self.files = MoveField.get_filenames_in_dir(project_dir)
        self.override = override
        self.filename_maping = filename_map

    @staticmethod
    def get_filenames_in_dir(dir: Union[str, Path],
                             filter=lambda x: x.endswith(".java")
                             ) -> List[str]:
        result = []
        for (dirname, dirnames, filenames) in os.walk(dir):
            result.extend([dirname + '/' + name for name in filenames if filter(name)])
        return result

    def clean_up_dir(self) -> None:
        """
        Cleans up trashed files and gives original files
        """
        original_files = list()
        for file in self.files:
            if "rewritten.java" in file:
                os.remove(file)
            else:
                original_files.append(file)

        self.files = original_files

    def transfer_field(self):
        methods_tobe_update = []
        field = None
        for file in self.files:
            stream = FileStream(file, encoding='utf8')
            lexer = JavaLexer(stream)
            token_stream = CommonTokenStream(lexer)
            parser = JavaParser(token_stream)
            tree = parser.compilationUnit()
            utils_listener = PreConditionListener(file)
            walker = ParseTreeWalker()
            walker.walk(utils_listener, tree)

            if not utils_listener.can_convert:
                continue

            if len(utils_listener.package.classes) > 1:
                exit(1)

            # find fields with the type Source first and store it
            field_candidate = set()
            for klass in utils_listener.package.classes.values():
                for f in klass.fields.values():
                    if f.datatype == self.src_class:
                        field_candidate.add(f.name)

            listener = FieldUsageListener(
                file,
                self.src_class,
                self.src_package,
                self.target_class,
                self.target_package,
                self.field_name,
                field_candidate,
                field)
            walker.walk(listener, tree)
            # listener.save(override=self.override, filename_mapping=self.filename_maping)

            methods_tobe_update = listener.methods_tobe_updated + methods_tobe_update

            if file.__contains__(self.src_class):
                field = listener.field_tobe_moved

        return methods_tobe_update

    def update_method_calls(self, methods):

        if not self.override:
            files_to_apply = [self.filename_maping(file) for file in self.files]

        else:
            files_to_apply = self.files

        for i, file in enumerate(self.files):
            stream = FileStream(files_to_apply[i], encoding='utf8')
            lexer = JavaLexer(stream)
            token_stream = CommonTokenStream(lexer)
            parser = JavaParser(token_stream)
            tree = parser.compilationUnit()
            listener = MethodUsageListener(file, methods, self.target_class)
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            # listener.save(override=self.override, filename_mapping=self.filename_maping)

    def refactor(self):
        self.clean_up_dir(self.files)
        methods_to_be_update = self.transfer_field()
        self.update_method_calls(methods_to_be_update)


if __name__ == "__main__":
    move_field = MoveField(
        src_class="Source",
        src_package="src",
        target_class="Target",
        target_package="target",
        field_name="a",
        project_dir="/home/amiresm/Projects/personal/src"
    )

    move_field.refactor()
