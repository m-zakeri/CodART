import os
from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from openunderstand.oudb.models import KindModel, EntityModel, ReferenceModel

PRJ_INDEX = 0
REF_NAME = "import demand"


def get_project_info(index, ref_name):
    project_names = [
        "calculator_app",
        "JSON",
        "testing_legacy_code",
        "jhotdraw-develop",
        "xerces2j",
        "jvlt-1.3.2",
        "jfreechart",
        "ganttproject",
        "105_freemind",
    ]
    project_name = project_names[index]
    db_path = f"../../databases/{ref_name}/{project_name}"
    if ref_name == "origin":
        db_path = db_path + ".udb"
    else:
        db_path = db_path + ".oudb"
    project_path = f"E:/comppppppp/OpenUnderstand/benchmark/{project_name}"

    return {
        "PROJECT_NAME": project_name,
        "DB_PATH": db_path,
        "PROJECT_PATH": project_path,
    }


def get_parse_tree(file_path):
    file = FileStream(file_path, encoding="utf-8")
    lexer = JavaLexer(file)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return parser.compilationUnit()


class Project:
    def _init_(self, db_name, project_dir, project_name=None):
        self.db_name = db_name
        self.project_dir = project_dir
        self.project_name = project_name
        self.files = []

    def init_db(self):
        create_db(self.db_name, self.project_dir, self.project_name)
        db_fill()
        db_open(self.db_name)

    def get_java_files(self):
        for dir_path, _, file_names in os.walk(self.project_dir):
            for file in file_names:
                if ".java" in str(file):
                    path = os.path.join(dir_path, file)
                    path = path.replace("/", "\\")
                    self.files.append((file, path))
                    # add java file entity to database
                    # add_java_file_entity(path, file)


class ImportListenerDemand(JavaParserLabeledListener):
    def __init__(self, files):
        self.names = []
        self.longnames = []
        self.is_unknown_class = []
        self.parents = []
        self.line = 0
        self.col = 0
        self.files = files
        self.repository = []
        self.dict = {}

    def enterImportDeclaration(self, ctx: JavaParserLabeled.CompilationUnitContext):
        self.longname = ctx.qualifiedName().getText()
        self.name = ctx.getText().split(".")[-1]
        a = self.name.split(";")[0]

        if a == "*":
            self.line = ctx.children[0].symbol.line
            self.col = ctx.children[0].symbol.column
            self.repository.append(
                {
                    "longname": self.longname,
                    "line": self.line,
                    "col": self.col,
                    "name": self.name,
                }
            )


class ClassEntityListener(JavaParserLabeledListener):
    def __init__(self):
        self.class_body = None

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        print("inside class declaration", ctx.getText())
        self.class_body = ctx.getText()


def get_class_body(path):
    file = FileStream(path)
    lexer = JavaLexer(file)
    tokens = CommonTokenStream(lexer)

    parser = JavaParserLabeled(tokens)

    tree = parser.compilationUnit()

    listener = ClassEntityListener()

    walker = ParseTreeWalker()
    walker.walk(listener=listener, t=tree)
    return listener.class_body


def main():
    info = get_project_info(PRJ_INDEX, REF_NAME)
    p = Project(info["DB_PATH"], info["PROJECT_PATH"], info["PROJECT_NAME"])
    p.get_java_files()
    n = 1
    for file_name, file_path in p.files:
        tree = get_parse_tree(file_path)
        listener = ImportListener(p.files)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        for i in listener.repository:
            path = file_path.replace("/", "\\")
            ent, _ = EntityModel.get_or_create(
                _kind=1,
                _parent="None",
                _name=path,
                _longname=i["longname"],
                _contents=FileStream(file_path, encoding="utf-8"),
            )

            ReferenceModel.get_or_create(
                _kind=204,
                _file=file_path,
                _line=i["line"],
                _column=i["col"],
                _ent=ent.get_id(),
                _scope=file_path,
            )
            n = n + 1
