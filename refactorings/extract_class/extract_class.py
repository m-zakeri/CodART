import networkx as nx
from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

# from visualization import graph_visualization
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class ExtractClassRecognizerListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream = None, class_identifier: str = None):
        self.enter_class = False
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')
        self.field_dict = {}
        self.method_name = []
        self.method_no = 0
        self.connected_components = []

    # Groups methods in terms of their dependencies on the class attributes and one another
    def split_class(self):
        # 1- move the dictionary of fields into a new dictionary of methods operating on fields
        method_dict = {}
        for key, value in self.field_dict.items():
            for method in value:
                if not str(method) in method_dict:
                    method_dict[str(method)] = [key]
                else:
                    method_dict[str(method)].append(key)
        # 2- Group methods in terms of their dependencies on one another
        method_group = dict()
        # _____________________To be modified ________________________
        # 3- Group methods in terms of their dependencies on the class attributes
        for key, value in method_dict.items():
            if not str(value) in method_group:
                method_group[str(value)] = [key]
            else:
                method_group[str(value)].append(key)
        # --------------------------------------
        # 4- Create graph
        G = nx.DiGraph()
        for field, methods in self.field_dict.items():
            for method in methods:
                G.add_node(method[1], method_name=method[0])
                G.add_edge(field, method[1])

        # graph_visualization.draw(g=G)
        S = [G.subgraph(c).copy() for c in nx.weakly_connected_components(G)]

        for class_ in S:
            # print('class_', class_.nodes.data())
            class_fields = [node for node in class_.nodes if class_.in_degree(node) == 0]
            class_methods = [class_.nodes[node]['method_name'] for node in class_.nodes if
                             class_.in_degree(node) > 0]
            self.connected_components.append(class_fields + class_methods)

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() != self.class_identifier:
            return
        self.enter_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() != self.class_identifier:
            return
        self.enter_class = False
        self.split_class()

        print("----------------------------")
        print("Class attributes: ", str(self.field_dict.keys()))
        print("Class methods: ", str([element[0] for element in self.method_name]))
        print("----------------------------")

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if not self.enter_class:
            return
        field_id = ctx.variableDeclarators().variableDeclarator(i=0).variableDeclaratorId().IDENTIFIER().getText()
        self.field_dict[field_id] = []

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.enter_class:
            return
        m = []
        m_name = ctx.IDENTIFIER().getText()
        self.method_no = self.method_no + 1
        m.append(m_name)
        m.append(self.method_no)
        self.method_name.append(m)

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.enter_class:
            return

    def exitExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        if not self.enter_class:
            return
        if self.method_no == 0:
            return
        current_method = self.method_name[-1]

        if ctx.IDENTIFIER() is not None:
            variable_name = ctx.IDENTIFIER().getText()
            if variable_name not in self.field_dict:
                return
            if current_method not in self.field_dict[variable_name]:
                self.field_dict[variable_name].append(current_method)


class ExtractClassRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None,
                 source_class: str = None, new_class: str = None,
                 moved_fields=None, moved_methods=None, filename: str = None):

        if moved_methods is None:
            self.moved_methods = []
        else:
            self.moved_methods = moved_methods

        if moved_fields is None:
            self.moved_fields = []
        else:
            self.moved_fields = moved_fields

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if filename is None:
            raise ValueError('filename is None')
        else:
            self.filename = filename

        if source_class is None:
            raise ValueError("source_class is None")
        else:
            self.source_class = source_class

        if new_class is None:
            raise ValueError("new_class is None")
        else:
            self.new_class = new_class

        self.is_source_class = False
        self.detected_field = None
        self.detected_method = None
        self.TAB = "\t"
        self.NEW_LINE = "\n"
        self.code = ""

    # Exit a parse tree produced by JavaParserLabeled#importDeclaration.
    def exitImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        text_to_replace = "import " + ctx.qualifiedName().getText() + ';'
        if ctx.STATIC() is not None:
            text_to_replace = text_to_replace.replace("import", "import static")

        self.code += text_to_replace + self.NEW_LINE

    # Enter a parse tree produced by JavaParserLabeled#packageDeclaration.
    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        package_name = ctx.getText().split("package")[1].replace(';', '')
        self.code += f"package {package_name};"

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        print("Refactoring started, please wait...")
        class_identifier = ctx.IDENTIFIER().getText()

        if class_identifier == self.source_class:
            self.is_source_class = True
            self.code += f"// New class({self.new_class}) generated by CodART" + self.NEW_LINE
            self.code += f"public class {self.new_class}{self.NEW_LINE}" + "{" + self.NEW_LINE
        else:
            self.is_source_class = False

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_source_class:
            self.code += "}"
            self.is_source_class = False

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        print("Finished Processing...")
        new_file = open(file='/'.join(self.filename.split('/')[:-1]) + '/' + self.new_class + '.java', mode='w')
        new_file.write(self.code)
        # self.token_stream_rewriter.insertAfter(
        #     index=ctx.stop.tokenIndex,
        #     text=self.code
        # )

    def enterVariableDeclaratorId(self, ctx: JavaParserLabeled.VariableDeclaratorIdContext):
        if not self.is_source_class:
            return None

        field_identifier = ctx.IDENTIFIER().getText()
        if field_identifier in self.moved_fields:
            self.detected_field = field_identifier

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if not self.is_source_class:
            return None
        field_names = ctx.variableDeclarators().getText().split(",")
        grand_parent_ctx = ctx.parentCtx.parentCtx

        if self.detected_field in field_names:
            modifier = grand_parent_ctx.modifier(0).getText()
            field_type = ctx.typeType().getText()
            self.code += f"{self.TAB}{modifier} {field_type} {self.detected_field};{self.NEW_LINE}"

            # delete field from source class
            field_names.remove(self.detected_field)
            if field_names:
                self.token_stream_rewriter.replaceRange(
                    from_idx=grand_parent_ctx.start.tokenIndex,
                    to_idx=grand_parent_ctx.stop.tokenIndex,
                    text=f"{modifier} {field_type} {','.join(field_names)};"
                )
            else:
                self.token_stream_rewriter.delete(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=grand_parent_ctx.start.tokenIndex,
                    to_idx=grand_parent_ctx.stop.tokenIndex
                )
            self.detected_field = None

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.is_source_class:
            return None
        method_identifier = ctx.IDENTIFIER().getText()
        if method_identifier in self.moved_methods:
            self.detected_method = method_identifier

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.is_source_class:
            return None
        method_identifier = ctx.IDENTIFIER().getText()

        if self.detected_method == method_identifier:
            start_index = ctx.start.tokenIndex
            stop_index = ctx.stop.tokenIndex

            if ctx.parentCtx.parentCtx.modifier() is not None:
                start_index = ctx.parentCtx.parentCtx.start.tokenIndex
                stop_index = ctx.parentCtx.parentCtx.stop.tokenIndex

            method_text = self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=start_index,
                stop=stop_index
            )
            self.code += (self.NEW_LINE + self.TAB + method_text + self.NEW_LINE)

            # delete method from source class
            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=start_index,
                to_idx=stop_index
            )
            self.detected_method = None


class ReplaceDependentObjectsListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(self, common_token_stream: CommonTokenStream = None,
                 source_class: str = None, new_class: str = None,
                 moved_fields=None, moved_methods=None, filename: str = None):

        if moved_methods is None:
            self.moved_methods = []
        else:
            self.moved_methods = moved_methods

        if moved_fields is None:
            self.moved_fields = []
        else:
            self.moved_fields = moved_fields

        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

        if filename is None:
            raise ValueError('filename is None')
        else:
            self.filename = filename

        if source_class is None:
            raise ValueError("source_class is None")
        else:
            self.source_class = source_class

        if new_class is None:
            raise ValueError("new_class is None")
        else:
            self.new_class = new_class

        self.NEW_LINE = "\n"
        self.BACKSLASH = "\\"

        self.import_token_index = 0
        self.import_text = ''
        self.write_import = False

    def exitExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        if ctx.expression().getText() != self.source_class:
            return
        if ctx.methodCall() is not None:
            if ctx.methodCall().IDENTIFIER() is not None:
                method_name = ctx.methodCall().IDENTIFIER().getText()
                if method_name in self.moved_methods:
                    if not self.write_import:
                        self.token_stream_rewriter.insertAfter(
                            program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                            index=self.import_token_index,
                            text='\n' + self.import_text
                        )
                        self.write_import = True

                    self.token_stream_rewriter.replace(
                        program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                        from_idx=ctx.expression().start.tokenIndex,
                        to_idx=ctx.expression().stop.tokenIndex,
                        text=f"{self.new_class}"
                    )
        elif ctx.IDENTIFIER() is not None:
            field_name = ctx.IDENTIFIER().getText()
            if field_name in self.moved_fields:
                if not self.write_import:
                    self.token_stream_rewriter.insertAfter(
                        program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                        index=self.import_token_index,
                        text='\n' + self.import_text
                    )
                    self.write_import = True

                self.token_stream_rewriter.replace(
                    program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                    from_idx=ctx.expression().start.tokenIndex,
                    to_idx=ctx.expression().stop.tokenIndex,
                    text=f"{self.new_class}"
                )

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        print("Finished Processing...")
        new_file = open(file=self.filename, mode='w')
        new_file.write(self.token_stream_rewriter.getDefaultText().replace('\r', ''))

    def exitImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        if not ctx.qualifiedName().getText().endswith(self.source_class):
            return

        self.import_token_index = ctx.stop.tokenIndex

        self.import_text = ctx.getText().replace('import', 'import ').\
            replace('.' + self.source_class, '.' + self.new_class)
