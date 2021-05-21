"""

"""

__version__ = '0.1.0'
__author__ = 'Morteza'

import networkx as nx
from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from visualization import graph_visualization
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

from utilization.setup_understand import *
import os

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

class ExtractClassRefactoringListener(JavaParserLabeledListener):
    """
    To implement extract class refactoring based on its actors.
    Creates a new class and move fields and methods from the old class to the new one
    """

    def __init__(
            self, common_token_stream: CommonTokenStream = None,
            source_class: str = None, new_class: str = None,
            moved_fields=None, moved_methods=None):
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
        self.file_cons=""
        self.new_file_cons=""

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_identifier = ctx.IDENTIFIER().getText()
        if class_identifier == self.source_class:

            self.is_source_class = True
            self.code += self.NEW_LINE * 2
            self.code += f"// New class({self.new_class}) generated by CodART" + self.NEW_LINE
            self.code += f"class {self.new_class}{self.NEW_LINE}" + "{" + self.NEW_LINE
        else:
            self.is_source_class = False
    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.is_source_class:
            self.code += "}"
            self.is_source_class = False

            self.token_stream_rewriter.insertAfter(
                index=ctx.stop.tokenIndex,
                text=self.code
            )
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
        field_names = ctx.variableDeclarators().getText().split(",")
        grand_parent_ctx = ctx.parentCtx.parentCtx
        if self.detected_field in field_names:
            modifier = grand_parent_ctx.modifier(0)
            if modifier:
                modifier = modifier.getText()
            else:
                modifier = ""
            field_type = ctx.typeType().getText()
            self.code += f"{modifier} {field_type} {self.detected_field};{self.NEW_LINE}"
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
            method_text = self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=start_index,
                stop=stop_index
            )
            self.code += self.NEW_LINE + (str(
                ctx.parentCtx.parentCtx.children[0].children[0].children[0]) + " " + method_text + self.NEW_LINE)
            # delete method from source class
            self.token_stream_rewriter.delete(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                from_idx=ctx.parentCtx.parentCtx.children[0].children[0].start.tokenIndex,
                to_idx=stop_index
            )
            self.detected_method = None
    def exitConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):

        for i in ctx.children[2].children[1:-1]:
            text = self.token_stream_rewriter.getText(
                program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                start=i.start.tokenIndex,
                stop=i.stop.tokenIndex
            )
            for moved in self.moved_fields:
                if(moved in text):
                    self.new_file_cons+=self.TAB+self.TAB+ text+"\n"
                    self.token_stream_rewriter.delete(
                        program_name=self.token_stream_rewriter.DEFAULT_PROGRAM_NAME,
                        from_idx=i.start.tokenIndex,
                        to_idx=i.stop.tokenIndex
                    )

class FindClassUsagesListener(JavaParserLabeledListener):
    def __init__(self, source_class: str = None, new_class: str = None):
        if source_class is None:
            raise ValueError("source_class is None")
        else:
            self.source_class = source_class
        if new_class is None:
            raise ValueError("new_class is None")
        else:
            self.new_class = new_class

        self.is_source_class = False
        self.is_new_class = False
        self.is_other_class = False
        self.type = None
        self.class_name = None
        self.method_name = None
        self.usages = []

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.class_name = ctx.IDENTIFIER().getText()
        self.is_new_class = self.class_name == self.new_class
        self.is_source_class = self.class_name == self.source_class
        self.is_other_class = not (self.is_new_class or self.is_source_class)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_other_class:
            self.method_name = ctx.IDENTIFIER().getText()

    def enterTypeType(self, ctx: JavaParserLabeled.TypeTypeContext):
        child = ctx.getChild(0)
        self.type = child.getText()

    def exitVariableDeclarator(self, ctx: JavaParserLabeled.VariableDeclaratorContext):
        if self.is_other_class:
            variable_name = ctx.variableDeclaratorId().IDENTIFIER().getText()
            # print(variable_name, "-->", self.type)
            if self.type == self.source_class:
                self.usages.append({
                    "identifier": variable_name,
                    "startTokenIndex": ctx.variableDeclaratorId().start.tokenIndex,
                    "inClass": self.class_name,
                    "inMethod": self.method_name
                })

class ChangeClassUsagesListener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream = None,
                 source_class: str = None, new_class: str = None,
                 moved_fields=None, moved_methods=None, usages=None):
        if moved_methods is None:
            self.moved_methods = []
        else:
            self.moved_methods = moved_methods
        if moved_fields is None:
            self.moved_fields = []
        else:
            self.moved_fields = moved_fields
        if usages is None:
            self.usages = []
        else:
            self.usages = usages

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
        self.is_new_class = False
        self.is_other_class = False
        self.type = None
        self.class_name = None
        self.method_name = None
        # print(self.usages)

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.class_name = ctx.IDENTIFIER().getText()
        self.is_new_class = self.class_name == self.new_class
        self.is_source_class = self.class_name == self.source_class
        self.is_other_class = not (self.is_new_class or self.is_source_class)

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_other_class:
            self.method_name = ctx.IDENTIFIER().getText()

    def enterExpression1(self, ctx: JavaParserLabeled.Expression1Context):
        # TODO: Complete this
        if self.is_other_class:
            children = ctx.children
            if len(children) > 2:
                if children[1].getText() == ".":
                    usage_names = [usage["identifier"] for usage in self.usages]
                    left_side = children[0].getText()
                    right_side = ctx.IDENTIFIER()
                    if left_side in usage_names:
                        if right_side is not None:
                            print(f"{right_side} is used attribute")
                            if str(right_side) in self.moved_fields:
                                print(f"Call Rename {self.source_class} --> {self.new_class}")
                        else:
                            right_side = ctx.methodCall().getText()
                            print(f"{right_side} is used method")

class PropagateClassRefactoringListener(JavaParserLabeledListener):
    """
    To implement propagate class refactoring based on its actors.
    Changes all methods and field those are using our class also it will set constructor!
    """

    def __init__(
            self, file_path,
            common_token_stream: CommonTokenStream = None,
            source_class: str = None, new_class: str = None,
            moved_fields=None, moved_methods=None):
        self.file_path=file_path
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
        self.added=""
        self.started=False
        #It will store all variable names we have on a method
        self.variablesNames=[]
        #It will store all variable types we have on a method
        self.variablesTypes = []

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.variablesNames = []
        self.variablesTypes = []

        if not self.is_source_class:
            return None
        # method_identifier = ctx.IDENTIFIER().getText()
        # if method_identifier in self.moved_methods:
        #     self.detected_method = method_identifier

    def enterVariableDeclaratorId(self, ctx: JavaParserLabeled.VariableDeclaratorIdContext):
        field_identifier = ctx.IDENTIFIER().getText()
        self.variablesNames.append(field_identifier)
        self.variablesTypes.append(ctx.parentCtx.start.text)
        # if field_identifier in self.moved_fields:
        #     self.detected_field = field_identifier

    def enterMethodCall0(self, ctx:JavaParserLabeled.MethodCall0Context):
        #When we enter on a method of one class, this listener will trigger
        methodName=self.new_class[0].lower()+self.new_class[1:]

        if (ctx.parentCtx.start.text in self.variablesNames):
            x = self.variablesNames.index(ctx.parentCtx.start.text)
            typeVar = self.variablesTypes[x]
            if ((typeVar == self.source_class) and (ctx.IDENTIFIER().getText() in self.moved_methods)):
                changed_text=ctx.parentCtx.start.text + "." + methodName
                #If it's one of our moved methods it will update that line to be compile
                self.token_stream_rewriter.replaceRange(
                    ctx.parentCtx.children[0].start.tokenIndex,
                    ctx.parentCtx.children[0].start.tokenIndex,
                    changed_text
                )
                with open(self.file_path, mode='w', newline='') as f:
                    f.write(self.token_stream_rewriter.getDefaultText())

    def enterExpression1(self, ctx:JavaParserLabeled.Expression2Context):
        #When we enter on a field of one class, this listener will trigger

        fieldName=self.new_class[0].lower()+self.new_class[1:]
        if (ctx.start.text in self.variablesNames):
            x = self.variablesNames.index(ctx.start.text)
            typeVar = self.variablesTypes[x]
            if ((typeVar == self.source_class) and (ctx.stop.text in self.moved_fields)):
                changed_text = ctx.start.text + "." + fieldName
                #If it's one of our moved fields it will update that line to be compile
                self.token_stream_rewriter.replaceRange(
                    ctx.parentCtx.children[0].start.tokenIndex,
                    ctx.parentCtx.children[0].start.tokenIndex,
                    changed_text
                )
                with open(self.file_path, mode='w', newline='') as f:
                    f.write(self.token_stream_rewriter.getDefaultText())


class ExtractClassAPI:
    def __init__(self, project_dir, file_path, source_class, new_class, moved_fields, moved_methods,
                 new_file_path=None):
        self.project_dir = project_dir
        self.file_path = file_path
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
        self.checked = False
        self.TAB = "\t"


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

    def find_usages(self, new_code):
        stream = InputStream(new_code)
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        tree = parser.compilationUnit()
        find_listener = FindClassUsagesListener(
            source_class=self.source_class,
            new_class=self.new_class,
        )
        self.walker.walk(
            listener=find_listener,
            t=tree
        )
        change_listener = ChangeClassUsagesListener(
            common_token_stream=token_stream,
            source_class=self.source_class,
            new_class=self.new_class,
            moved_fields=self.moved_fields,
            moved_methods=self.moved_methods,
            usages=find_listener.usages
        )
        self.walker.walk(
            listener=change_listener,
            t=tree
        )

        # print(change_listener.token_stream_rewriter.getDefaultText())

    def do_refactor(self):
        self.check_dependency_graph()
        if self.checked:
            listener = ExtractClassRefactoringListener(
                common_token_stream=self.token_stream,
                new_class=self.new_class,
                source_class=self.source_class,
                moved_fields=self.moved_fields,
                moved_methods=self.moved_methods
            )
            self.walker.walk(
                listener=listener,
                t=self.tree
            )
            s = listener.token_stream_rewriter.getDefaultText().split("\n")
            a = 0
            for i in s:
                if i == f"// New class({self.new_class}) generated by CodART":
                    a = s.index(i)
                    i +="\n"
                    s[a] = i
            s.append("\n}")
            firstcalss = s[0:a]
            file1 = open(self.new_file_path, "a")
            file1.truncate(0)
            file2 = open(self.file_path,"a")
            file2.truncate(0)
            if(len(listener.new_file_cons)>0):
                s[a+1]="public "+s[a+1]+"{"+f"\n{self.TAB}public {self.new_class}()"+"{\n"+listener.new_file_cons+self.TAB+"}"
            else:
                s[a + 1] = "public " + s[
                    a + 1] + "{" + f"\n{self.TAB}"
            tt=0
            for i in s[a+1:-1]:
                if(tt!=1):
                    i+="\n"
                    file1.write(i)
                tt=tt+1

            file1.close()
            temp = firstcalss[0].split("{")
            objectname = str(self.new_class)
            objectname = objectname.replace(objectname,objectname[0].lower()+objectname[1:len(objectname)])
            isinstance = f"   public {self.new_class} {objectname};"
            temp[0] = f"public class {self.source_class} "+"{\n"+isinstance
            for i in temp:
                if(f"{self.source_class}()" in i):
                    x=i.index(f"{self.source_class}()")
                    file2.write(i[:x+len(self.source_class)+2]+"{"+i[x+len(self.source_class)+2:])
                else:
                    file2.write(i)

            file2.close()
            print("Finished")
            print("=" * 50)
            # After Refactoring
            self.find_usages(listener.token_stream_rewriter.getDefaultText())


        else:
            print("Can not refactor!")


class PropagateClassAPI:
    def __init__(self, project_dir, file_path, source_class, new_class, moved_fields, moved_methods,
                 new_file_path=None):
        self.project_dir = project_dir
        self.file_path = file_path
        self.new_file_path = new_file_path or "/home/ali/Documents/dev/CodART/input.refactored.java"
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
        self.checked = False

    def do_propagate(self):
            listener = PropagateClassRefactoringListener(
                file_path=self.file_path,
                common_token_stream=self.token_stream,
                new_class=self.new_class,
                source_class=self.source_class,
                moved_fields=self.moved_fields,
                moved_methods=self.moved_methods
            )
            self.walker.walk(
                listener=listener,
                t=self.tree
            )

def get_java_files(directory):
    if not os.path.isdir(directory):
        raise ValueError("directory should be an absolute path of a directory!")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.split('.')[-1] == 'java':
                yield (os.path.join(root, file), file)

if __name__ == "__main__":
        ExtractClassAPI(
            project_dir="D:\\University\\Term 6\\Compiler\\TA\\iust-compiler992\\test_project",
            file_path="D:\\University\\Term 6\\Compiler\\CodART\\GodClass.java",
            source_class="GodClass",
            new_class="GodClassExtracted",
            moved_fields=["field1", "field2", ],
            moved_methods=["method1", "method3", ],
            new_file_path="D:\\University\\Term 6\\Compiler\\CodART\\GodClassExtracted.java"
        ).do_refactor()

        for i in get_java_files("D:\\University\\Term 6\\Compiler\\TA\\iust-compiler992\\test_project"):
            PropagateClassAPI(
                project_dir="D:\\University\\Term 6\\Compiler\\TA\\iust-compiler992\\test_project",
                file_path=i[0],
                source_class="GodClass",
                new_class="GodClassExtracted",
                moved_fields=["field1", "field2", ],
                moved_methods=["method1", "method3", ]
            ).do_propagate()
# public class GodClass {
#   int field1;
#   int field2;
#   int field3;
#
#   public int method1(){
#     return this.field1+this.field2;
#   }
#
#   public int method2(){
#     return this.field3;
#   }
#
#   public int method3(){
#     return this.field2;
#   }
# }


#
# public class GodClass {
#   int field1;
#   int field2;
#   int field3;
#
#   public GodClass(){
#     this.field1=0;
#     this.field2=0;
#     this.field3=0;
#   }
#
#   public int method1(){
#     return this.field1+this.field2;
#   }
#
#   public int method2(){
#     return this.field3;
#   }
#
#   public int method3(){
#     return this.field2;
#   }
# }