import os
from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from oudb.fill import fill as db_fill
from oudb.api import create_db, open as db_open
from oudb.models import KindModel, EntityModel, ReferenceModel


def config_entity_type(type_entity):
    if type_entity == "class":
        return "Class Type"
    if type_entity == "interface":
        return "Interface Type"
    if type_entity == "variable":
        return "Variable"
    if type_entity == "method":
        return "Method"


def extract_is_constructor(prefixes):
    pattern_visibility = " Default"
    if "private" in prefixes:
        pattern_visibility = " Private"
    elif "public" in prefixes:
        pattern_visibility = " Public"
    elif "protected" in prefixes:
        pattern_visibility = " Protected"
    return f"Java Method Constructor Member{pattern_visibility}"


def extract_all_kind(prefixes, type_entity, is_constructor) -> str:
    if is_constructor:
        return extract_is_constructor(prefixes)

    pattern_static = ""
    pattern_generic = ""
    pattern_abstract = ""
    pattern_visibility = " Default"
    if "static" in prefixes:
        pattern_static = " Static"
    if "generic" in prefixes:
        pattern_generic = " Generic"
    if "abstract" in prefixes:
        pattern_abstract = " Abstract"
    elif "final" in prefixes:
        pattern_abstract = " Final"
    if "private" in prefixes:
        pattern_visibility = " Private"
    elif "public" in prefixes:
        pattern_visibility = " Public"
    elif "protected" in prefixes:
        pattern_visibility = " Protected"

    result_str = "Java{0}{1}{2} {3}{4} Member".format(
        pattern_static,
        pattern_abstract,
        pattern_generic,
        config_entity_type(type_entity),
        pattern_visibility,
    )
    if type_entity == "interface":
        result_str = result_str.replace("Member", "").strip()
    return result_str


DB_PATH = "../database/xerces2j-db.oudb"
PROJECT_PATH = "../projects/xerces2j"
PROJECT_NAME = "Sample App"


class Project:
    def __init__(self, db_name, project_dir, project_name=None):
        self.db_name = db_name
        self.project_dir = project_dir
        self.project_name = project_name
        self.file_paths = []
        self.file_names = []

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
                    path = os.path.abspath(path)
                    self.file_paths.append(path)
                    self.file_names.append(file)
                    add_java_file_entity(path, file)


def get_parse_tree(file_path):
    file = FileStream(file_path, encoding="utf-8")
    lexer = JavaLexer(file)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return parser.compilationUnit()


def get_parent_entity(file_path):
    return EntityModel.get_or_none(_longname=file_path)


def add_classes_to_entity(ref_dict, file_path):
    kind_name = extract_all_kind(
        prefixes=ref_dict["prefixes"],
        type_entity=ref_dict["mode"],
        is_constructor=False,
    )
    parent_entity = get_parent_entity(file_path)
    # creating child entity
    child_entity, _ = EntityModel.get_or_create(
        _kind=KindModel.get_or_none(_name=kind_name)._id,
        _parent=parent_entity._id,
        _name=ref_dict["child_class"].split(".")[-1],
        _longname=ref_dict["child_class"],
        _type=ref_dict["type"],
        _contents=ref_dict["content"],
    )
    # creating parent entity
    extended_entity, _ = EntityModel.get_or_create(
        _kind=84,  # because unknown class type kind_id is 84,
        _parent=None,
        _name=ref_dict["parent_class"].split(".")[-1],
        _longname=ref_dict["parent_class"],
        _contents="",
    )

    return child_entity, extended_entity


def add_java_file_entity(file_path, file_name):
    kind_id = KindModel.get_or_none(_name="Java File")._id
    obj, _ = EntityModel.get_or_create(
        _kind=kind_id,
        _name=file_name,
        _longname=file_path,
        _contents=FileStream(file_path, encoding="utf-8"),
    )
    return obj


def add_reference_files(child_entity, parent_entity, ref_dict, file_path):
    file_id = get_parent_entity(file_path)._id
    ReferenceModel.get_or_create(
        _kind_id=182,
        _file_id=file_id,
        _line=ref_dict["line"],
        _column=ref_dict["column"],
        _ent_id=child_entity._id,
        _scope_id=parent_entity._id,
    )
    ReferenceModel.get_or_create(
        _kind_id=183,
        _file_id=file_id,
        _line=ref_dict["line"],
        _column=ref_dict["column"],
        _ent_id=parent_entity._id,
        _scope_id=child_entity._id,
    )


class PackageImportListener(JavaParserLabeledListener):
    def __init__(self):
        self.package_name = ""
        self.imported_libraries = []

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_name = ctx.getText().replace("package", "").replace(";", "")

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        parsed_import = ctx.getText().replace("import", "").replace(";", "")
        if parsed_import[:4] == "java":
            self.imported_libraries.append(parsed_import)


def check_is_java_library(parent_class, import_list):
    for java_import in import_list:
        if java_import.split(".")[-1] == parent_class:
            return java_import
    return False


class ExtendCoupleListener(JavaParserLabeledListener):
    def __init__(self, package_name, import_list):
        self.inherited_classes = []
        self.package_name = package_name
        self.import_list = import_list

    def enterInterfaceDeclaration(
        self, ctx: JavaParserLabeled.InterfaceDeclarationContext
    ):
        if not ctx.EXTENDS():
            return
        child_types = list(map(lambda x: type(x), ctx.children))
        child_class = str(ctx.children[1])
        is_generic = False
        if JavaParserLabeled.TypeParametersContext not in child_types:  # not generic
            inherited_class_str = ctx.children[3].getText()
            column = ctx.children[3].start.column
        else:  # generic
            inherited_class_str = ctx.children[4].getText()
            is_generic = True
            column = ctx.children[4].start.column
        line = ctx.start.line
        children_string = [i.getText() for i in ctx.children]
        start_index = children_string.index("extends")
        class_type = " ".join(children_string[start_index:-1])
        prefix_of_class = ctx.parentCtx.children
        connect_prefix_class = ""
        for branch in prefix_of_class:
            if type(branch) == JavaParserLabeled.InterfaceDeclarationContext:
                break
            connect_prefix_class += branch.getText() + " "
        if is_generic:
            connect_prefix_class += "generic"
        first_condition = (
            "java." in inherited_class_str or "javax." in inherited_class_str
        )
        second_condition = check_is_java_library(inherited_class_str, self.import_list)
        # for column
        if first_condition:
            last_part = inherited_class_str.split(".")[-1]
            column += inherited_class_str.index(last_part)
        if first_condition or second_condition:
            self.inherited_classes.append(
                {
                    "child_class": self.package_name + "." + child_class,
                    "parent_class": (
                        inherited_class_str if first_condition else second_condition
                    ),
                    "line": line,
                    "column": column,
                    "prefixes": connect_prefix_class.strip(),
                    "content": ctx.getText(),
                    "type": class_type,
                    "mode": "interface",
                }
            )

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if not ctx.EXTENDS():
            return
        child_types = list(map(lambda x: type(x), ctx.children))
        child_class = str(ctx.children[1])
        is_generic = False
        if JavaParserLabeled.TypeParametersContext not in child_types:  # not generic
            inherited_class = ctx.children[3].children[0].children
            column = ctx.children[3].start.column
        else:  # generic
            inherited_class = ctx.children[4].children[0].children
            is_generic = True
            column = ctx.children[4].start.column

        inherited_class_str = "".join(list(map(lambda x: str(x), inherited_class)))
        line = ctx.start.line
        children_string = [i.getText() for i in ctx.children]
        start_index = children_string.index("extends")
        class_type = " ".join(children_string[start_index:-1])
        temp_ctx = ctx
        while (
            type(temp_ctx) != JavaParserLabeled.ClassBodyDeclaration2Context
            and type(temp_ctx) != JavaParserLabeled.TypeDeclarationContext
        ):
            temp_ctx = temp_ctx.parentCtx
        prefix_of_class = temp_ctx.children
        connect_prefix_class = ""
        for branch in prefix_of_class:
            if (
                type(branch) == JavaParserLabeled.ClassDeclarationContext
                or type(branch) == JavaParserLabeled.MemberDeclaration7Context
            ):
                break
            connect_prefix_class += branch.getText() + " "
        if is_generic:
            connect_prefix_class += "generic"
        first_condition = (
            "java." in inherited_class_str or "javax." in inherited_class_str
        )
        second_condition = check_is_java_library(inherited_class_str, self.import_list)
        # for column
        if first_condition:
            last_part = inherited_class_str.split(".")[-1]
            column += inherited_class_str.index(last_part)
        if first_condition or second_condition:
            self.inherited_classes.append(
                {
                    "child_class": self.package_name + "." + child_class,
                    "parent_class": (
                        inherited_class_str if first_condition else second_condition
                    ),
                    "line": line,
                    "column": column,
                    "prefixes": connect_prefix_class.strip(),
                    "content": ctx.getText(),
                    "type": class_type,
                    "mode": "class",
                }
            )


def main():
    p = Project(DB_PATH, PROJECT_PATH, PROJECT_NAME)
    p.init_db()
    p.get_java_files()

    for file_path, file_name in zip(p.file_paths, p.file_names):
        try:
            tree = get_parse_tree(file_path)
            walker = ParseTreeWalker()
            package_import_listener = PackageImportListener()
            walker.walk(package_import_listener, tree)
            extend_listener = ExtendCoupleListener(
                package_import_listener.package_name,
                package_import_listener.imported_libraries,
            )
            walker.walk(extend_listener, tree)
            for entity_dict in extend_listener.inherited_classes:
                child_entity, parent_entity = add_classes_to_entity(
                    entity_dict, file_path
                )
                add_reference_files(child_entity, parent_entity, entity_dict, file_path)
        except:
            print("some exception happened")
            continue


if __name__ == "__main__":
    main()
