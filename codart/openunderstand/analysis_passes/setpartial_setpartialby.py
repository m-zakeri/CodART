from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from os.path import basename


class SetPartialAndSetByPartialListener(JavaParserLabeledListener):
    def __init__(self, file_name):
        self.ex_name = ""
        self.in_expreession_21 = False
        self.has_primary_3 = False
        self.in_variable_initializer = False
        self.initializer_identifier_number = 0
        self.number_of_primary_4 = 0
        self.file_name = basename(file_name)
        self.package_name = ""
        self.set_by_partial = []
        self.enterd_expression = False
        self.call_function = False
        self.create_object = False
        self.method_name = ""
        self.class_name = ""
        self.ent_type = None
        self.ss = ""
        self.set_value = ""

    def add_set_by_entry(
        self, set_short_name, set_long_name, name_of_file, line, column, ctx
    ):
        # print("nnnmmm", self.ss)
        sss = self.ss + "." + self.ex_name
        self.set_by_partial.append(
            (
                set_short_name,
                set_long_name,
                name_of_file,
                self.set_value,
                line,
                column,
                self.package_name,
                self.ex_name,
                self.ent_type,
                self.stream,
                sss,
            )
        )
        # print(f"========{self.setBy[0][2]}")

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        name_of_file = self.file_name
        # self.ex_name = ctx.children[1].getText()
        long_name = name_of_file.replace(".java", "") + "." + self.ex_name
        line = ctx.children[0].symbol.line
        col = ctx.children[0].symbol.column

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        name_of_file = self.file_name
        # self.ex_name = ctx.children[1].getText()

    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        self.enterd_initialization = True
        self.create_object = False
        self.call_function = False

    def exitExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        try:
            name_of_file = self.file_name
            set_short_name = ctx.children[0].getText()
            if int(ctx.children[0].getChildCount()) > 1:
                node = ctx
                if (
                    ctx.children[1].getText()
                    and ctx.children[0].children[1].getText() == "="
                ):
                    line = ctx.children[0].children[2].symbol.line
                    column = ctx.children[0].children[2].symbol.column
                    # print(self.file_name)

                else:
                    if ctx.children[1].getText() == "=":
                        if (
                            ctx.children[0].children[1].getText() == "."
                            and ctx.children[0].children[0].getText() != "this"
                        ):
                            self.ex_name = ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.children[
                                0
                            ].getText()
                            while node.getChildCount() != 0:
                                node = node.children[0]
                            node1 = ctx
                            while node1.getRuleIndex() not in (7, 25, 20):
                                node1 = node1.parentCtx
                            self.set_value = node1.children[0].getText()
                            self.ent_type = node1.children[0].getText()
                            self.stream = node1.parentCtx.parentCtx.getText()
                            self.ss = node1.children[0].getText()
                            set_long_name = (
                                self.package_name
                                + "."
                                + self.ex_name
                                + "."
                                + ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.children[
                                    1
                                ].getText()
                                + "."
                                + node.getText()
                            )
                            set_short_name = ctx.children[0].children[0].getText()
                            line = node.symbol.line
                            column = node.symbol.column
                            self.add_set_by_entry(
                                set_short_name,
                                set_long_name,
                                name_of_file,
                                line,
                                column,
                                ctx,
                            )

            else:
                pass

            self.add_set_by_entry(
                set_short_name, set_long_name, name_of_file, line, column, ctx
            )

        except:
            x = 0

        self.enterd_expression = False
        self.call_function = False
        self.create_object = False
        self.method_name = ""
        self.class_name = ""

    def exitPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_name = ctx.children[1].getText()
