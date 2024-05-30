import os
from antlr4 import *
from pathlib import Path
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from openunderstand.oudb.models import KindModel, EntityModel, ReferenceModel, ProjectModel

PRJ_INDEX = 3
REF_NAME = "import"


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
    project_path = f"../../benchmarks/{project_name}"

    return {
        "PROJECT_NAME": project_name,
        "DB_PATH": db_path,
        "PROJECT_PATH": project_path,
    }


def find_java_files(root_dir):
    java_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".java"):
                java_files.append(file)
    return java_files


def get_parse_tree(file_path):
    file = FileStream(file_path, encoding="utf-8")
    lexer = JavaLexer(file)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return parser.compilationUnit()


class Project:
    def __init__(self, db_name, project_dir, project_name=None):
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
                    add_java_file_entity(path, file)


class ImportListener(JavaParserLabeledListener):
    def __init__(self, files):
        self.project_files = find_java_files(ProjectModel.select()[0].root)
        self.repository = []
        self.files = files

    def enterImportDeclaration(self, ctx: JavaParserLabeled.importDeclaration):
        imported_class_longname = ctx.qualifiedName().getText()
        imported_class_name = imported_class_longname.split(".")[-1]
        imported_class_file_name = None

        is_built_in = True
        for ICN in imported_class_longname.split(".")[::-1]:
            imported_class_file_name = ICN + ".java"
            if imported_class_file_name in self.project_files:
                is_built_in = False
                break

        if is_built_in:
            imported_class_file_name = None
        line = ctx.children[0].symbol.line
        col = ctx.children[0].symbol.column
        if (
            (ctx.children[1].getText() != "static")
            or ((ctx.children[1].getText() == "static") and not is_built_in)
            or (
                (ctx.children[1].getText() == "static")
                and ctx.getText().endswith(".*;")
            )
        ):
            self.repository.append(
                {
                    "imported_class_name": imported_class_name,
                    "imported_class_longname": imported_class_longname,
                    "is_built_in": is_built_in,
                    "imported_class_file_name": imported_class_file_name,
                    "line": line,
                    "column": col,
                }
            )


class ImportedEntityListener(JavaParserLabeledListener):
    def __init__(self, name):
        self.body = None
        self.branches = None
        self.type = None
        self.name = name

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if self.name == ctx.IDENTIFIER().getText():
            self.body = ctx.getText()
            self.branches = ctx.parentCtx.children

    def enterInterfaceDeclaration(
        self, ctx: JavaParserLabeled.InterfaceDeclarationContext
    ):
        if self.name == ctx.IDENTIFIER().getText():
            self.body = ctx.getText()
            self.branches = ctx.parentCtx.children

    def enterEnumDeclaration(self, ctx: JavaParserLabeled.EnumDeclarationContext):
        if self.name == ctx.IDENTIFIER().getText():
            self.body = ctx.getText()
            self.branches = ctx.parentCtx.children


def get_parent(parent_file_name, files):
    file_names, file_paths = zip(*files)
    parent_file_index = file_names.index(parent_file_name)
    parent_file_path = file_paths[parent_file_index]
    parent_entity = EntityModel.get_or_none(
        _kind=1,  # Java File
        _name=parent_file_name,
        _longname=parent_file_path,
    )
    return parent_entity, parent_file_path


def add_imported_entity(i, files):
    if i["is_built_in"]:
        imported_entity, _ = EntityModel.get_or_create(
            _kind=84,  # Java Unknown Class Type Member
            _parent=None,
            _name=i["imported_class_name"],
            _longname=i["imported_class_longname"],
        )
    else:
        parent_entity, parent_file_path = get_parent(
            i["imported_class_file_name"], files
        )
        prefixes, class_body, kind = get_imported_entity(parent_file_path)
        entity_kind = get_kind_name(prefixes, kind)
        imported_entity, _ = EntityModel.get_or_create(
            _kind=KindModel.get_or_none(_name=entity_kind).get_id(),
            _parent=parent_entity.get_id(),
            _name=i["imported_class_name"],
            _longname=i["imported_class_longname"],
            _contents=class_body,
        )
    return imported_entity


def get_imported_entity(file_path):
    tree = get_parse_tree(file_path)
    listener = ImportedEntityListener(Path(file_path).stem)
    walker = ParseTreeWalker()
    walker.walk(listener=listener, t=tree)

    prefixes = ""
    kind = ""
    for branch in listener.branches:
        if type(branch) == JavaParserLabeled.ClassDeclarationContext:
            kind = "Class"
            break
        elif type(branch) == JavaParserLabeled.InterfaceDeclarationContext:
            kind = "Interface"
            break
        elif type(branch) == JavaParserLabeled.EnumDeclarationContext:
            kind = "Enum Class"
            break
        prefixes += branch.getText() + " "
    return prefixes, listener.body, kind


def get_kind_name(prefixes, kind):
    p_static = ""
    p_abstract = ""
    p_generic = ""
    p_type = "Type"
    p_visibility = "Default"
    p_member = "Member"

    if "static" in prefixes:
        p_static = "Static"

    if "generic" in prefixes:
        p_generic = "Generic"

    if "abstract" in prefixes:
        p_abstract = "Abstract"
    elif "final" in prefixes:
        p_abstract = "Final"

    if "private" in prefixes:
        p_visibility = "Private"
    elif "public" in prefixes:
        p_visibility = "Public"
    elif "protected" in prefixes:
        p_visibility = "Protected"

    if kind == "Interface":
        p_member = ""

    if kind == "Method":
        p_type = ""

    s = f"Java {p_static} {p_abstract} {p_generic} {kind} {p_type} {p_visibility} {p_member}"
    s = " ".join(s.split())
    return s


def add_java_file_entity(file_path, file_name):
    kind_id = 1  # Java File
    obj, _ = EntityModel.get_or_create(
        _kind=kind_id,
        _name=file_name,
        _longname=file_path,
        _contents=FileStream(file_path, encoding="utf-8"),
    )
    return obj


def add_references(importing_ent, imported_ent, ref_dict):
    ref, _ = ReferenceModel.get_or_create(
        _kind=206,  # Java Import
        _file=importing_ent.get_id(),
        _line=ref_dict["line"],
        _column=ref_dict["column"],
        _ent=imported_ent.get_id(),
        _scope=importing_ent.get_id(),
    )
    inverse_ref, _ = ReferenceModel.get_or_create(
        _kind=207,  # Java Importby
        _file=importing_ent.get_id(),
        _line=ref_dict["line"],
        _column=ref_dict["column"],
        _ent=importing_ent.get_id(),
        _scope=imported_ent.get_id(),
    )

    # print(f"1. ref name: Java Import")
    # print(
    #     f"2. ref scope: {importing_ent._longname} || kind: {KindModel.get_or_none(_id=importing_ent._kind)._name}"
    # )
    # print(
    #     f"3. ref ent: {imported_ent._longname} || kind: {KindModel.get_or_none(_id=imported_ent._kind)._name}"
    # )
    # print(
    #     f'4. file location: {EntityModel.get_or_none(_id=importing_ent.get_id())} || line: {ref_dict["line"]}'
    # )
    # print("-" * 25)


def main():
    info = get_project_info(PRJ_INDEX, REF_NAME)
    p = Project(info["DB_PATH"], info["PROJECT_PATH"], info["PROJECT_NAME"])
    p.init_db()
    p.get_java_files()

    for file_name, file_path in p.files:
        importing_entity = add_java_file_entity(file_path, file_name)

        tree = get_parse_tree(file_path)
        listener = ImportListener(p.files)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        for i in listener.repository:
            imported_entity = add_imported_entity(i, p.files)
            add_references(importing_entity, imported_entity, i)
