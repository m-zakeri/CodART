# Group 13
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class SetInitAndSetByInitListener(JavaParserLabeledListener):
    def __init__(self, file_name):
        self.ex_name = ""
        self.in_expreession_21 = False
        self.has_primary_3 = False
        self.in_variable_initializer = False
        self.initializer_identifier_number = 0
        self.number_of_primary_4 = 0
        self.file_name = file_name
        self.package_name = ""
        self.set_init_by = []
        self.enterd_initialization = False
        self.call_function = False
        self.create_object = False
        self.method_name = ""
        self.class_name = ""
        self.ent_type = None
        self.stream = ""
        self.ss = ""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        name_of_file = self.file_name.split("\\")[
            self.file_name.split("\\").count(0) - 1
        ]
        self.ex_name = ctx.children[1].getText()
        long_name = name_of_file.replace(".java", "") + "." + self.ex_name
        line = ctx.children[0].symbol.line
        col = ctx.children[0].symbol.column

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):

        name_of_file = self.file_name.split("\\")[
            self.file_name.split("\\").count(0) - 1
        ]
        self.ex_name = ctx.children[1].getText()

    def enterVariableInitializer1(
        self, ctx: JavaParserLabeled.VariableInitializer1Context
    ):
        self.enterd_initialization = True
        self.create_object = False
        self.call_function = False

    def exitVariableInitializer1(
        self, ctx: JavaParserLabeled.VariableInitializer1Context
    ):
        try:
            name_of_file = self.file_name.split("\\")[
                self.file_name.split("\\").count(0) - 1
            ]
            node = ctx
            while node.getRuleIndex() not in (20, 7, 25):
                node = node.parentCtx
            if node.getRuleIndex() == 20:
                self.stream = node.parentCtx.parentCtx.getText()
                set_init_short_name = ctx.parentCtx.children[0].getText()
                self.ss = node.children[0].getText()
                set_init_long_name = (
                    self.package_name
                    + "."
                    + node.children[0].getText()
                    + "."
                    + self.ex_name
                    + "."
                    + ctx.parentCtx.children[0].getText()
                )
            elif node.getRuleIndex() == 25:
                self.stream = node.parentCtx.parentCtx.getText()
                set_init_short_name = ctx.parentCtx.children[0].getText()
                self.ss = node.children[0].getText()
                set_init_long_name = (
                    self.package_name
                    + "."
                    + node.children[0].getText()
                    + "."
                    + self.ex_name
                    + "."
                    + ctx.parentCtx.children[0].getText()
                )
            else:
                node1 = ctx
                while node1.getRuleIndex() != 26:
                    node1 = node1.parentCtx
                node2 = ctx
                while node2.getRuleIndex() != 0:
                    node2 = node2.parentCtx
                self.stream = node.parentCtx.parentCtx.getText()
                self.ss = node2.children[0].children[1].children[2].getText()
                set_init_short_name = (
                    node1.children[0].getText()
                    + "."
                    + ctx.parentCtx.children[0].getText()
                )
                set_init_long_name = (
                    self.package_name
                    + "."
                    + self.ex_name
                    + "."
                    + ctx.parentCtx.children[0].getText()
                )
            set_init_type = ctx.parentCtx.children[0].getText()
            line = ctx.parentCtx.children[0].children[0].symbol.line
            column = ctx.parentCtx.children[0].children[0].symbol.column
            if self.call_function:
                set_init_value = self.method_name
            elif self.create_object:
                set_init_value = self.class_name
            else:
                set_init_value = ctx.getText()
            sss = self.ss + "." + self.ex_name
            self.set_init_by.append(
                (
                    set_init_short_name,
                    set_init_long_name,
                    name_of_file,
                    set_init_value,
                    set_init_type,
                    line,
                    column,
                    self.ex_name,
                    self.ent_type,
                    self.stream,
                    sss,
                )
            )

        except:
            x = 0

        self.enterd_initialization = False
        self.call_function = False
        self.create_object = False
        self.method_name = ""
        self.class_name = ""

    def exitPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_name = ctx.children[1].getText()
