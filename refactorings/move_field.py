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
