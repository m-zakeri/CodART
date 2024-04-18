import os

from antlr4 import *

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from openunderstand.oudb.models import KindModel, EntityModel, ReferenceModel

PRJ_INDEX = 4


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ClassTypeData:
    def __init__(self):
        self.parentClass = None
        self.childClass: JavaParserLabeled.ClassDeclarationContext = None
        self.file_path: str = ""
        self.package_name: str = ""
        self.line: int = -1
        self.column: int = -1
        self.prefixes: list = []

    def set_child_class(self, child: JavaParserLabeled.ClassDeclarationContext):
        self.childClass = child

    def set_parent_class(self, parent):
        self.parentClass = parent

    def set_file_path(self, file_path: str):
        self.file_path = file_path

    def set_package_name(self, name: str):
        self.package_name = name

    def set_line(self, line: int):
        self.line = line

    def set_column(self, column: int):
        self.column = column

    def set_prefixes(self, prefix_list: list):
        self.prefixes = prefix_list

    def get_long_name(self) -> str:
        return self.package_name + "." + self.childClass.getText()

    def get_type(self) -> str:
        return "extends" + " " + self.parentClass

    def get_name(self) -> str:
        return str(self.childClass.IDENTIFIER())

    def get_contents(self) -> str:
        return self.childClass.getText()

    def get_prefixes(self) -> list:
        return self.prefixes


class DataBaseHandler:
    def __init__(self):
        self.classTypes: list = []

    def put(self, data: ClassTypeData):
        self.classTypes.append(data)

    def get_list_class_types(self):
        return [str(cls) for cls in self.classTypes]


class DSCmetric(JavaParserLabeledListener):
    def __init__(self, package_name):
        self.package_name = package_name
        self.dbHandler = DataBaseHandler()
        self.class_type_names = []

    @property
    def get_class_types(self):
        json_output = {"list_class": self.dbHandler.get_list_class_types()}
        return json_output

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        def check_generic_class():
            for child in ctx.children:
                if isinstance(child, JavaParserLabeled.TypeParametersContext):
                    return True
            return False

        if ctx.EXTENDS():
            return
        prefix_list = []
        for child in ctx.parentCtx.children:
            if type(child) == JavaParserLabeled.ClassDeclarationContext:
                break
            prefix_list.append(child.getText())
        if check_generic_class():
            prefix_list.append("generic")
        data = ClassTypeData()
        data.set_child_class(ctx)
        data.set_parent_class("java.lang.Object")
        data.set_column(0)
        data.set_prefixes(prefix_list=prefix_list)
        data.set_package_name(self.package_name)
        data.set_line(ctx.start.line)
        self.dbHandler.put(data)


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


def getNameEntity(prefixes) -> str:
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

    result_str = "Java{0}{1}{2} Class Type{3} Member".format(
        pattern_static, pattern_abstract, pattern_generic, pattern_visibility
    )
    return result_str


def get_parent(parent_file_path) -> EntityModel:
    return EntityModel.get_or_none(_longname=parent_file_path)


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
                    self.file_paths.append(path)
                    self.file_names.append(file)
                    add_java_file_entity(path, file)

    def imported_entity_factory(self, cls_data: ClassTypeData):
        parent_entity: EntityModel = get_parent(cls_data.file_path)
        kindModel = KindModel.get_or_none(_name=getNameEntity(cls_data.get_prefixes()))
        # if kindModel is None:
        #     print(getNameEntity(cls_data.get_prefixes()))
        extend_implicit_entity, _ = EntityModel.get_or_create(
            _kind=kindModel._id,
            _parent=parent_entity._id,
            _name=cls_data.get_name(),
            _type=cls_data.get_type(),
            _longname=cls_data.get_long_name(),
            _contents=cls_data.get_contents(),
        )
        entity_kind_object = 84
        java_lang_entity, _ = EntityModel.get_or_create(
            _kind=entity_kind_object,
            _parent=None,
            _name="Object",
            _type=None,
            _longname=cls_data.parentClass,
            _contents="",
        )
        return extend_implicit_entity, java_lang_entity


def get_parse_tree(file_path):
    file = FileStream(file_path, encoding="utf-8")
    lexer = JavaLexer(file)
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return parser.compilationUnit()


def add_java_file_entity(file_path, file_name):
    kind_id = KindModel.get_or_none(_name="Java File")._id
    obj, _ = EntityModel.get_or_create(
        _kind=kind_id,
        _name=file_name,
        _longname=file_path,
        _contents=FileStream(file_path, encoding="utf-8"),
    )
    return obj


def add_references(importing_ent, imported_ent, cls_data: ClassTypeData, file_path):

    ref, _ = ReferenceModel.get_or_create(
        _kind=KindModel.get_or_none(_name="Java Extend Couple Implicit")._id,
        _file_id=importing_ent._id,
        _line=cls_data.line,
        _column=cls_data.column,
        _ent_id=imported_ent._id,
        _scope_id=importing_ent._id,
    )

    inverse_ref, _ = ReferenceModel.get_or_create(
        _kind=KindModel.get_or_none(_name="Java Extend Coupleby Implicit")._id,
        _file_id=importing_ent._id,
        _line=cls_data.line,
        _column=cls_data.column,
        _ent_id=importing_ent._id,
        _scope_id=imported_ent._id,
    )


def main():
    p = Project(DB_PATH, PROJECT_PATH, PROJECT_NAME)
    p.init_db()
    p.get_java_files()
    for file_path, file_name in zip(p.file_paths, p.file_names):

        tree = get_parse_tree(file_path)
        walker = ParseTreeWalker()

        package_import_listener = PackageImportListener()
        walker.walk(package_import_listener, tree)

        my_listener = DSCmetric(package_import_listener.package_name)
        walker.walk(my_listener, tree)

        for classType in my_listener.dbHandler.classTypes:
            classType.set_file_path(file_path)
            imported_entity, importing_entity = p.imported_entity_factory(classType)
            add_references(importing_entity, imported_entity, classType, file_path)
