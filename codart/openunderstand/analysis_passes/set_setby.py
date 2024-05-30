from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from os.path import basename


class SetAndSetByListener(JavaParserLabeledListener):
    def __init__(self, file_name):
        self.ex_name = ""
        self.in_expression_21 = False
        self.has_primary_3 = False
        self.in_variable_initializer = False
        self.initializer_identifier_number = 0
        self.number_of_primary_4 = 0
        self.file_name = basename(file_name)
        self.package_name = ""
        self.setBy = []
        self.entered_expression = False
        self.call_function = False
        self.create_object = False
        self.method_name = ""
        self.class_name = ""
        self.for_loop_counter = 0
        self.stream = ""
        self.ent_type = None
        self.ent_value = None
        self.ent_name = None
        self.ss = ""

    def add_set_by_entry(
        self, set_short_name, set_long_name, name_of_file, line, column, ctx
    ):
        if self.call_function:
            set_value = self.method_name
        elif self.create_object:
            set_value = self.class_name
        else:
            if (
                ("this" in ctx.children[0].getText())
                or (ctx.children[2].getChildCount() <= 1)
            ) and (ctx.getRuleIndex() == 83):
                set_value = None
            else:
                set_value = "String"

        sss = self.ss + "." + self.ex_name
        self.setBy.append(
            (
                set_short_name,
                set_long_name,
                name_of_file,
                set_value,
                line,
                column,
                self.package_name,
                self.ex_name,
                self.stream,
                self.ent_type,
                sss,
            )
        )

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.ex_name = ctx.children[1].getText()
        long_name = self.file_name.replace(".java", "") + "." + self.ex_name
        line = ctx.children[0].symbol.line
        col = ctx.children[0].symbol.column

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.ex_name = ctx.children[1].getText()

    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        self.entered_expression = True
        self.create_object = False
        self.call_function = False

    def exitExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        try:
            name_of_file = self.file_name
            set_long_name = (
                self.package_name + "." + self.ex_name + "." + ctx.children[0].getText()
            )
            set_short_name = ctx.children[0].getText()
            if int(ctx.children[0].getChildCount()) > 1:
                node = ctx
                if (
                    ctx.children[1].getText()
                    and ctx.children[0].children[1].getText() == "="
                ):
                    line = ctx.children[0].children[2].symbol.line
                    column = ctx.children[0].children[2].symbol.column
                    self.add_set_by_entry(
                        set_short_name, set_long_name, name_of_file, line, column, ctx
                    )
                else:
                    if ctx.children[1].getText() == "=":
                        if ctx.children[0].children[1].getText() == "[":
                            if ctx.children[0].children[0].getChildCount() > 1:
                                line = (
                                    ctx.children[0].children[0].children[2].symbol.line
                                )
                                column = (
                                    ctx.children[0]
                                    .children[0]
                                    .children[2]
                                    .symbol.column
                                )
                                node = ctx
                                node = self.get_parent_node(node, (25, 20, 7))
                                set_long_name = (
                                    self.package_name
                                    + "."
                                    + node.children[1].getText()
                                    + "."
                                    + ctx.children[0].children[0].children[0].getText()
                                )
                                self.add_set_by_entry(
                                    set_short_name,
                                    set_long_name,
                                    name_of_file,
                                    line,
                                    column,
                                    ctx,
                                )
                            else:
                                while node.getChildCount() != 0:
                                    node = node.children[0]
                                line = node.symbol.line
                                column = node.symbol.column
                                node = ctx
                                node = self.get_parent_node(node, (25, 20, 7))
                                set_long_name = (
                                    self.package_name
                                    + "."
                                    + node.children[1].getText()
                                    + "."
                                    + node.children[1].getText()
                                    + "."
                                    + ctx.children[0].children[0].getText()
                                )
                                self.add_set_by_entry(
                                    set_short_name,
                                    set_long_name,
                                    name_of_file,
                                    line,
                                    column,
                                    ctx,
                                )
                        elif (
                            ctx.children[0].children[1].getText() == "."
                            and ctx.children[0].children[0].getText() != "this"
                        ):
                            while node.getChildCount() != 0:
                                node = node.children[0]
                            node1 = ctx
                            node1 = self.get_parent_node(node1, (7, 25, 20))
                            self.ss = node1.children[0].getText()
                            set_long_name = (
                                self.package_name
                                + "."
                                + node1.children[0].getText()
                                + "."
                                + node1.children[1].getText()
                                + "."
                                + ctx.children[0].children[0].getText()
                            )
                            line = node.symbol.line
                            column = node.symbol.column
                            set_short_name = ctx.children[0].children[0].getText()
                            self.add_set_by_entry(
                                set_short_name,
                                set_long_name,
                                name_of_file,
                                line,
                                column,
                                ctx,
                            )
                            set_short_name = (
                                node1.children[0].getText()
                                + "."
                                + ctx.children[0].children[2].getText()
                            )
                            set_long_name = (
                                self.package_name
                                + "."
                                + node1.children[0].getText()
                                + "."
                                + ctx.children[0].children[2].getText()
                            )
                            self.add_set_by_entry(
                                set_short_name,
                                set_long_name,
                                name_of_file,
                                line,
                                column,
                                ctx,
                            )

                        else:
                            node = self.get_parent_node(ctx, (7, 25, 20))
                            self.ss = node.children[0].getText()
                            if node.getRuleIndex() == 25:
                                set_short_name = (
                                    node.children[0].getText()
                                    + "."
                                    + ctx.children[0].children[2].getText()
                                )
                                self.stream = node.parentCtx.parentCtx.getText()
                                self.scope_kind = (
                                    node.parentCtx.parentCtx.children[0].getText()
                                    + "."
                                    + node.children[0].getText()
                                )
                            set_long_name = (
                                self.package_name
                                + "."
                                + node.children[0].getText()
                                + "."
                                + ctx.children[0].children[2].getText()
                            )
                            line = (
                                ctx.children[0]
                                .children[0]
                                .children[0]
                                .children[0]
                                .symbol.line
                            )
                            column = (
                                ctx.children[0]
                                .children[0]
                                .children[0]
                                .children[0]
                                .symbol.column
                            )
                            self.add_set_by_entry(
                                set_short_name,
                                set_long_name,
                                name_of_file,
                                line,
                                column,
                                ctx,
                            )

            else:
                if ctx.children[1].getText() == "=":
                    node = ctx
                    node1 = self.get_parent_node(node, (7,))
                    line = ctx.children[0].children[0].children[0].symbol.line
                    if node.getRuleIndex() == 25:
                        self.stream = node.parentCtx.parentCtx.getText()
                        set_long_name = (
                            self.package_name
                            + "."
                            + node.children[0].getText()
                            + "."
                            + node1.children[1].getText()
                            + "."
                            + ctx.children[0].getText()
                        )
                    else:
                        set_long_name = (
                            self.package_name
                            + "."
                            + node1.children[1].getText()
                            + "."
                            + node.children[1].getText()
                            + "."
                            + ctx.children[0].getText()
                        )
                    column = ctx.children[0].children[0].children[0].symbol.column
                    self.add_set_by_entry(
                        set_short_name, set_long_name, name_of_file, line, column, ctx
                    )

        except Exception as e:
            print(f"Error occurred: {e}")

        self.entered_expression = False
        self.call_function = False
        self.create_object = False
        self.method_name = ""
        self.class_name = ""

    def enterVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        self.entered_expression = True
        self.create_object = False
        self.call_function = False

    def exitVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        try:
            name_of_file = self.file_name
            set_long_name = (
                self.package_name + "." + self.ex_name + "." + ctx.children[0].getText()
            )

            if int(ctx.getChildCount()) > 1 and ctx.children[1].getText() == "=":
                node = ctx
                node = self.get_parent_node(node, (25, 20, 7))
                set_short_name = node.children[0].getText()
                if ctx.parentCtx.parentCtx.parentCtx.parentCtx.getRuleIndex() == 77:
                    node1 = self.get_parent_node(node, (7,))
                    if node.getRuleIndex() == 20:
                        set_long_name = (
                            self.package_name
                            + "."
                            + node1.children[1].getText()
                            + "."
                            + node.children[1].getText()
                            + "."
                            + f"(for_loop_{self.for_loop_counter})"
                            + "."
                            + ctx.children[0].getText()
                        )
                    elif node.getRuleIndex() == 25:
                        self.stream = node.parentCtx.parentCtx.getText()
                        set_long_name = (
                            self.package_name
                            + "."
                            + node1.children[1].getText()
                            + "."
                            + node.children[0].getText()
                            + "."
                            + f"(for_loop_{self.for_loop_counter})"
                            + "."
                            + ctx.children[0].getText()
                        )
                    self.for_loop_counter += 1
                else:
                    if node.getRuleIndex() == 25:
                        set_long_name = (
                            self.package_name
                            + "."
                            + node.children[0].getText()
                            + "."
                            + ctx.children[0].getText()
                        )
                    elif node.getRuleIndex() == 20:
                        self.ss = node.children[0].getText()
                        node1 = self.get_parent_node(node, (7,))
                        set_short_name = ctx.children[0].getText()
                        set_long_name = (
                            self.package_name
                            + "."
                            + node1.children[1].getText()
                            + "."
                            + node.children[1].getText()
                            + "."
                            + ctx.children[0].getText()
                        )
                    else:
                        node2 = ctx
                        while node2.getRuleIndex() != 0:
                            node2 = node2.parentCtx
                        self.ss = node2.children[0].children[1].children[2].getText()
                        set_short_name = (
                            node.children[1].getText() + "." + ctx.children[0].getText()
                        )
                        set_long_name = (
                            self.package_name
                            + "."
                            + node.children[1].getText()
                            + "."
                            + ctx.children[0].getText()
                        )
                line = ctx.children[0].children[0].symbol.line
                column = ctx.children[0].children[0].symbol.column
                self.add_set_by_entry(
                    set_short_name, set_long_name, name_of_file, line, column, ctx
                )

        except Exception as e:
            print(f"Error occurred: {e}")

        self.entered_expression = False
        self.call_function = False
        self.create_object = False
        self.method_name = ""
        self.class_name = ""

    def exitPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        try:
            self.package_name = ctx.children[1].getText()

        except Exception as e:
            print(f"Error occurred: {e}")

    def exitMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        self.ent_value = ctx.children[0]

    def get_parent_node(self, node, indices):
        while node.getRuleIndex() not in indices:
            node = node.parentCtx
        return node
