__version__ = '0.2.0'
__author__ = 'Seyyed Ali Ayati'

import os
import subprocess
from pathlib import Path

try:
    import understand as und
except ImportError as e:
    print(e)

import networkx as nx
from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


class DependencyPreConditionListener(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None,
                 class_identifier: str = None):
        self.enter_class = False
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError("common_token_stream is None")
        self.field_dict = {}
        self.method_name = []  #
        self.method_no = 0
        self.connected_components = []

    # Groups methods in terms of their dependncies on the class attributes and one another
    def split_class(self):
        # 1- move the dictionay of fields into a new dictionary of methods operating on fields
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
            class_fields = [node for node in class_.nodes if class_.in_degree(node) == 0]
            class_methods = [class_.nodes[node]["method_name"] for node in class_.nodes if
                             class_.in_degree(node) > 0]
            self.connected_components.append(class_fields + class_methods)

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if ctx.IDENTIFIER().getText() != self.class_identifier:
            return
        self.enter_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.enter_class = False
        self.split_class()

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
        try:
            if not self.enter_class:
                return
            if self.method_no == 0:
                return
            current_method = self.method_name[-1]
            variable_name = ctx.IDENTIFIER().getText()
            if variable_name not in self.field_dict:
                return
            if not current_method in self.field_dict[variable_name]:
                self.field_dict[variable_name].append(current_method)
        except:
            x = 0


class MethodMapListener(JavaParserLabeledListener):
    def __init__(self, moved_fields: list, moved_methods: list):
        self.detected_usage = False
        self.detected_method = None
        self.map = {}
        self.moved_fields = moved_fields
        self.moved_methods = moved_methods

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.detected_method = ctx.IDENTIFIER().getText()
        self.map[self.detected_method] = set()

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.detected_method = None

    def enterPrimary1(self, ctx: JavaParserLabeled.Primary1Context):
        if ctx.THIS():
            self.detected_usage = True

    def exitExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        if self.detected_method and self.detected_usage:
            if ctx.IDENTIFIER():
                if ctx.IDENTIFIER().getText() not in self.moved_fields:
                    self.map[self.detected_method].add(ctx.IDENTIFIER().getText())
                self.detected_usage = False
            elif ctx.methodCall():
                if ctx.methodCall().IDENTIFIER().getText() not in self.moved_methods:
                    self.map[self.detected_method].add(ctx.methodCall().IDENTIFIER().getText())
                self.detected_usage = False


class ExtractClassRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(
            self, common_token_stream: CommonTokenStream = None,
            source_class: str = None, new_class: str = None,
            moved_fields=None, moved_methods=None, method_map: dict = None):
        if method_map is None:
            self.method_map = {}
        else:
            self.method_map = method_map

        if moved_methods is None:
            self.moved_methods = []
        else:
            self.moved_methods = moved_methods
        if moved_fields is None:
            self.moved_fields = []
        else:
            self.moved_fields = moved_fields

        if common_token_stream is None:
            raise ValueError("common_token_stream is None")
        else:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)

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
        self.package_name = ""
        self.file_cons = ""
        self.new_file_cons = ""
        self.parameters = []
        self.object_name = self.new_class.replace(self.new_class, self.new_class[0].lower() + self.new_class[1:])
        self.modifiers = ""

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        if ctx.qualifiedName() and not self.package_name:
            self.package_name = ctx.qualifiedName().getText()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = str(ctx.children[1])
        if class_identifier == self.source_class:
            self.is_source_class = True
            self.code += self.NEW_LINE * 2
            if self.package_name:
                self.code += f"package {self.package_name};{self.NEW_LINE}"
            self.code += f"// New class({self.new_class}) generated by CodART" + self.NEW_LINE
            self.code += f"class {self.new_class}{self.NEW_LINE}" + "{" + self.NEW_LINE
        else:
            self.is_source_class = False

    def enterClassBody(self, ctx: JavaParserLabeled.ClassBodyContext):
        if self.is_source_class:
            self.token_stream_rewriter.insertAfterToken(
                token=ctx.start,
                text="\n\t" + f"public {self.new_class} {self.object_name} = new {self.new_class}();",
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME
            )

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_source_class:
            self.code += "}"
            self.is_source_class = False

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        pass

    def enterVariableDeclaratorId(self, ctx: JavaParserLabeled.VariableDeclaratorIdContext):
        if not self.is_source_class:
            return None
        field_identifier = ctx.IDENTIFIER().getText()
        if field_identifier in self.moved_fields:
            self.detected_field = field_identifier

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        if not self.is_source_class:
            return None
        if self.detected_field is None:
            return None

        field_names = ctx.variableDeclarators().getText()
        field_names = field_names.split(',')
        grand_parent_ctx = ctx.parentCtx.parentCtx
        if any([self.detected_field in i for i in field_names]):
            field_type = ctx.typeType().getText()

            if len(field_names) == 1:
                self.code += f"public {field_type} {field_names[0]};{self.NEW_LINE}"
            else:
                self.code += f"public {field_type} {self.detected_field};{self.NEW_LINE}"
            # delete field from source class
            for i in field_names:
                if self.detected_field in i:
                    field_names.remove(i)

            if field_names:
                self.token_stream_rewriter.replaceRange(
                    from_idx=grand_parent_ctx.start.tokenIndex,
                    to_idx=grand_parent_ctx.stop.tokenIndex,
                    text=f"public {field_type} {','.join(field_names)};\n"
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

    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        if self.detected_method:
            self.parameters.append(
                ctx.variableDeclaratorId().IDENTIFIER().getText()
            )

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if not self.is_source_class:
            return None
        method_identifier = ctx.IDENTIFIER().getText()
        if self.detected_method == method_identifier:
            start_index = ctx.start.tokenIndex
            stop_index = ctx.stop.tokenIndex
            method_text = self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=start_index,
                stop=stop_index
            )
            self.code += self.NEW_LINE + ("public " + method_text + self.NEW_LINE)
            # delegate method body in source class
            if self.method_map.get(method_identifier):
                self.parameters.append("this")

            self.token_stream_rewriter.replaceRange(
                from_idx=ctx.methodBody().start.tokenIndex,
                to_idx=stop_index,
                text="{" + f"\nreturn this.{self.object_name}.{self.detected_method}(" + ",".join(
                    self.parameters) + ");\n" + "}"
            )
            self.parameters = []
            self.detected_method = None

    def exitConstructorDeclaration(self, ctx: JavaParserLabeled.ConstructorDeclarationContext):
        for i in ctx.children[2].children[1:-1]:
            text = self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=i.start.tokenIndex,
                stop=i.stop.tokenIndex
            )
            for moved in self.moved_fields:
                if moved in text:
                    self.new_file_cons += self.TAB + self.TAB + text + "\n"
                    self.token_stream_rewriter.delete(
                        program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                        from_idx=i.start.tokenIndex,
                        to_idx=i.stop.tokenIndex
                    )


class PropagateFieldUsageListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream, object_name: str, field_name: str, class_name: str,
                 line_number: int):
        self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        self.field_name = field_name
        self.class_name = class_name
        self.line_number = line_number
        self.object_name = object_name

    def enterExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        identifier = ctx.IDENTIFIER()
        if identifier is not None:
            if identifier.getText() == self.field_name:
                self.token_stream_rewriter.replaceSingleToken(
                    token=ctx.expression().primary().start,
                    text=f"this.{self.object_name}"
                )


class NewClassPropagation(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream, method_map: dict, source_class: str):
        self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        self.method_map = method_map
        self.source_class = source_class
        self.fields = None

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.fields = self.method_map.get(ctx.IDENTIFIER().getText())
        if self.fields:
            if ctx.formalParameters().getText() == "()":
                text = f"{self.source_class} ref"
            else:
                text = f", {self.source_class} ref"

            self.token_stream_rewriter.insertBeforeToken(
                token=ctx.formalParameters().stop,
                text=text,
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME
            )

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.fields = None

    def enterExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        if self.fields and ctx.expression().getText() == "this":
            for field in self.fields:
                if field in ctx.getText():
                    self.token_stream_rewriter.replaceSingleToken(
                        token=ctx.expression().primary().start,
                        text="ref"
                    )


class ExtractClassAPI:
    def __init__(self, udb_path, file_path, source_class, new_class, moved_fields, moved_methods,
                 new_file_path=None):
        self.file_path = file_path
        self.udb_path = udb_path
        self.new_file_path = new_file_path
        self.source_class = source_class
        self.new_class = new_class
        self.moved_fields = moved_fields
        self.moved_methods = moved_methods
        self.stream = FileStream(self.file_path, encoding="utf8")
        self.lexer = JavaLexer(self.stream)
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = JavaParserLabeled(self.token_stream)
        self.tree = self.parser.compilationUnit()
        self.walker = ParseTreeWalker()
        self.method_usage_map = {}
        self.pass_this = False
        self.TAB = "\t"
        self.object_name = ""

    def check_dependency_graph(self):
        listener = DependencyPreConditionListener(
            common_token_stream=self.token_stream,
            class_identifier=self.source_class
        )
        self.walker.walk(
            listener=listener,
            t=self.tree
        )
        component = sorted(self.moved_methods + self.moved_fields)
        if component in sorted(listener.connected_components):
            self.checked = True
        if len(listener.connected_components) == 0:
            self.checked = True

    def get_source_class_map(self):
        listener = MethodMapListener(moved_fields=self.moved_fields, moved_methods=self.moved_methods)
        self.walker.walk(
            listener=listener,
            t=self.tree
        )
        self.method_usage_map = listener.map

    def propagate_fields(self, usages):
        for usage in usages:
            file_path = usage.pop('file_path')
            stream = FileStream(file_path, encoding='utf8')
            lexer = JavaLexer(stream)
            token_stream = CommonTokenStream(lexer)
            parser = JavaParserLabeled(token_stream)
            parse_tree = parser.compilationUnit()
            my_listener = PropagateFieldUsageListener(common_token_stream=token_stream, object_name=self.object_name,
                                                      **usage)
            walker = ParseTreeWalker()
            walker.walk(t=parse_tree, listener=my_listener)

            # print(my_listener.token_stream_rewriter.getDefaultText())
            with open(file_path, 'w') as f:
                f.write(my_listener.token_stream_rewriter.getDefaultText())
            self.reformat(file_path)

    @staticmethod
    def reformat(file_path: str):
        formatter = os.path.abspath("../assets/formatter/google-java-format-1.10.0-all-deps.jar")
        subprocess.call(["java", "-jar", formatter, "--replace", file_path])

    def do_refactor(self):
        self.get_source_class_map()
        listener = ExtractClassRefactoringListener(
            common_token_stream=self.token_stream,
            new_class=self.new_class,
            source_class=self.source_class,
            moved_fields=self.moved_fields,
            moved_methods=self.moved_methods,
            method_map=self.method_usage_map
        )
        self.object_name = listener.object_name
        self.walker.walk(
            listener=listener,
            t=self.tree
        )

        # Find Field and Method Usages
        field_usages = []
        method_usages = []

        db = und.open(self.udb_path)
        for field in self.moved_fields:
            for ent in db.lookup(f"{self.source_class}.{field}"):
                # print(ent.name(), "  [", ent.kindname(), "]", sep="", end="\n")
                for ref in ent.refs("Useby"):
                    if self.source_class in ref.ent().name():
                        referencer = ref.ent().simplename()
                        if referencer in self.moved_methods:
                            continue
                    ref_ent = ref.ent()
                    field_usages.append({
                        'field_name': field,
                        'class_name': ref_ent.simplename(),
                        'file_path': ref.file().longname(),
                        'line_number': ref.line()
                    })

        # print(listener.token_stream_rewriter.getDefaultText())
        # print("=" * 25)
        # print(listener.code)
        stream = InputStream(listener.code)
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parser.getTokenStream()
        parse_tree = parser.compilationUnit()
        my_listener = NewClassPropagation(common_token_stream=token_stream, method_map=self.method_usage_map,
                                          source_class=self.source_class)
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=my_listener)
        # print(my_listener.token_stream_rewriter.getDefaultText())

        # Write Changes
        with open(self.file_path, 'w') as f:
            f.write(listener.token_stream_rewriter.getDefaultText())

        with open(self.new_file_path, 'w') as f:
            f.write(my_listener.token_stream_rewriter.getDefaultText())

        # Propagate and reformat
        self.propagate_fields(field_usages)
        self.reformat(self.file_path)
        self.reformat(self.new_file_path)


def get_java_files(directory):
    if not os.path.isdir(directory):
        raise ValueError("directory should be an absolute path of a directory!")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.split('.')[-1] == 'java':
                yield os.path.join(root, file), file


def main(udb_path, file_path, source_class, moved_fields, moved_methods):
    new_class = f"{source_class}Extracted"
    new_file_path = os.path.join(Path(file_path).parent, f"{new_class}.java")

    ExtractClassAPI(
        udb_path=udb_path,
        file_path=file_path,
        source_class=source_class,
        new_class=new_class,
        moved_fields=moved_fields,
        moved_methods=moved_methods,
        new_file_path=new_file_path
    ).do_refactor()


if __name__ == "__main__":
    main(
        udb_path="D:\Dev\JavaSample\JavaSample1.udb",
        file_path="D:\Dev\JavaSample\src\your_package\Soldier.java",
        source_class="Soldier",
        moved_fields=["health", ],
        moved_methods=[],
    )
