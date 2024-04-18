# Group 13
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from os.path import basename


class SetAndSetByListener(JavaParserLabeledListener):
    def __init__(self, file_name):
        self.ex_name = ""
        self.in_expreession_21 = False
        self.has_primary_3 = False
        self.in_variable_initializer = False
        self.initializer_identifier_number = 0
        self.number_of_primary_4 = 0
        self.file_name = basename(file_name)
        self.package_name = ""
        self.setBy = []
        self.enterd_expression = False
        self.call_function = False
        self.create_object = False
        self.method_name = ""
        self.class_name = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        name_of_file = self.file_name
        self.ex_name = ctx.children[1].getText()
        long_name = name_of_file.replace(".java", "") + "." + self.ex_name
        line = ctx.children[0].symbol.line
        col = ctx.children[0].symbol.column

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):

        name_of_file = self.file_name
        self.ex_name = ctx.children[1].getText()

    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        self.enterd_initialization = True
        self.create_object = False
        self.call_function = False

    def exitExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        try:
            name_of_file = self.file_name
            set_long_name = (
                name_of_file.replace(".java", "")
                + "."
                + self.ex_name
                + "."
                + ctx.children[0].getText()
            )
            set_short_name = ctx.children[0].getText()
            line = ctx.children[0].children[0].children[0].symbol.line
            column = ctx.children[0].children[0].children[0].symbol.column
            if self.call_function:
                set_value = self.method_name
            elif self.create_object:
                set_value = self.class_name
            else:
                set_value = ctx.getText()
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
                )
            )

        except:
            x = 0

        self.enterd_expression = False
        self.call_function = False
        self.create_object = False
        self.method_name = ""
        self.class_name = ""

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        if self.enterd_expression:
            if not self.create_object:
                if not self.call_function:
                    self.call_function = True
                    self.method_name = ctx.IDENTIFIER()

    def enterCreatedName0(self, ctx: JavaParserLabeled.CreatedName0Context):
        if self.enterd_expression:
            if not self.create_object:
                if not self.call_function:
                    self.create_object = True
                    self.class_name = ctx.getText() + "(" + ")"
