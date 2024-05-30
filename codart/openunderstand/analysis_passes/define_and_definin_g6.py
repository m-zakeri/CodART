import os

from antlr4 import *
from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
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


class Project:
    def __init__(self, db_name, project_dir, project_name=None):
        self.db_name = db_name
        self.project_dir = project_dir
        self.project_name = project_name
        self.file_paths = []
        self.file_names = []

    def get_java_files(self):
        for dir_path, _, file_names in os.walk(self.project_dir):
            for file in file_names:
                if ".java" in str(file):
                    path = os.path.join(dir_path, file)
                    # path = path.replace("/", "\\")
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


def add_java_file_entity(file_path, file_name):
    kind_id = KindModel.get_or_none(_name="Java File")._id
    obj, _ = EntityModel.get_or_create(
        _kind=kind_id,
        _name=file_name,
        _longname=file_path,
        _contents=FileStream(file_path, encoding="utf-8"),
    )
    return obj


def traverse_parent_reach_class_or_interface(tmp_ctx):
    while (
        type(tmp_ctx) != JavaParserLabeled.ClassDeclarationContext
        and type(tmp_ctx) != JavaParserLabeled.InterfaceDeclarationContext
    ):
        tmp_ctx = tmp_ctx.parentCtx
    return tmp_ctx.children[1].getText()


def form_parent(ctx, second_parent_needed):
    if second_parent_needed:
        tmp_ctx = ctx
        while (
            type(tmp_ctx) != JavaParserLabeled.InterfaceMethodDeclarationContext
            and type(tmp_ctx) != JavaParserLabeled.MethodDeclarationContext
            and type(tmp_ctx) != JavaParserLabeled.ConstructorDeclarationContext
        ):
            tmp_ctx = tmp_ctx.parentCtx
        if type(tmp_ctx) != JavaParserLabeled.ConstructorDeclarationContext:
            parent_name_1 = tmp_ctx.children[
                1
            ].getText()  # parent name which is the method name this parameter declared in
        else:
            parent_name_1 = tmp_ctx.children[
                0
            ].getText()  # parent name which is the method name this parameter declared in

        parent_name_2 = traverse_parent_reach_class_or_interface(tmp_ctx)
        return f"{parent_name_2}.{parent_name_1}"
    else:
        parent_name = traverse_parent_reach_class_or_interface(ctx)
        return parent_name


def derive_type_and_name(which_declaration, ctx, value_needed):
    parameter_value = "" if not value_needed else ctx.getText()
    if which_declaration == 1:
        parameter_type = ctx.children[0].getText()
        parameter_name = ctx.children[1].getText()
        return parameter_type, parameter_name, parameter_value

    elif which_declaration == 2:
        field_name = ctx.children[0].children[1].children[0].getText()
        field_type = ctx.children[0].children[0].getText()
        return field_type, field_name, parameter_value

    elif which_declaration == 3:
        field_name = ctx.children[1].children[0].children[0].getText()
        field_type = ctx.children[0].getText()
        return field_type, field_name, parameter_value

    elif which_declaration == 4:
        class_name = ctx.children[1].getText()
        children_string = [i.getText() for i in ctx.children]
        try:
            start_index = children_string.index("extends")
            class_type = " ".join(children_string[start_index:-1])
        except ValueError:
            class_type = ""
        return class_type, class_name, parameter_value

    elif which_declaration == 5:
        if ctx.children[0].getText() != "final":
            field_name = ctx.children[1].children[0].children[0].getText()
            field_type = ctx.children[0].getText()
        else:
            field_name = ctx.children[2].children[0].children[0].getText()
            field_type = ctx.children[1].children[0].children[0].getText()
        return field_type, field_name, parameter_value

    elif which_declaration == 6:
        parameter_type = ""
        parameter_name = ctx.children[0].getText()
        return parameter_type, parameter_name, parameter_value


def form_prefix(ctx, prefix_needed, stop_prefix):
    if prefix_needed[0]:
        tmp_ctx = ctx
        for i in range(prefix_needed[1]):
            tmp_ctx = tmp_ctx.parentCtx
        field_prefixes = ""
        for child in tmp_ctx.children:
            if type(child) == stop_prefix:
                break
            field_prefixes += child.getText() + " "
        return field_prefixes


def add_declaration(
    ctx,
    which_declaration,
    kind_name,
    save_dict,
    prefix_needed,
    second_parent_needed,
    stop_prefix,
    is_generic,
    class_or_interface,
    needs_content,
    value_needed,
):
    entity_type, entity_name, entity_value = derive_type_and_name(
        which_declaration, ctx, value_needed
    )

    parent_name = (
        form_parent(ctx, second_parent_needed) if not class_or_interface else ""
    )

    line = ctx.start.line  # get line
    column = ctx.start.column  # get column

    def get_key():
        return f"{parent_name}.{entity_name}.{line}"

    save_dict[get_key()] = {
        "name": entity_name,
        "type": entity_type,
        "value": entity_value,
        "parent_name": parent_name,
        "line": line,
        "column": column,
        "contents": ctx.getText() if needs_content else "",
    }
    if prefix_needed[0]:
        save_dict[get_key()]["prefixes"] = form_prefix(ctx, prefix_needed, stop_prefix)
    else:
        save_dict[get_key()]["kind_name"] = kind_name

    if is_generic:
        save_dict[get_key()]["prefixes"] += " generic"


def define_is_generic(ctx):
    child_types = list(map(lambda x: type(x), ctx.children))
    is_generic = (
        True if JavaParserLabeled.TypeParametersContext in child_types else False
    )
    return is_generic


# for define , parent in entity is same as scope in reference
class DefineListener(JavaParserLabeledListener):
    def __init__(self):
        self.package = {}
        self.formal_parameters = {}  # parameter of method
        self.methods = {}
        self.classes = {}
        self.interfaces = {}
        self.local_variables = {}  # variable defined in method
        self.fields = {}  # fields defined in class

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package["package_name"] = (
            ctx.getText().replace("package", "").replace(";", "")
        )
        self.package["line"] = ctx.start.line
        self.package["column"] = ctx.start.column

    def enterFormalParameter(self, ctx: JavaParserLabeled.FormalParameterContext):
        add_declaration(
            prefix_needed=(False, 0),
            ctx=ctx,
            which_declaration=1,
            kind_name="Java Parameter",
            save_dict=self.formal_parameters,
            second_parent_needed=True,
            stop_prefix=False,
            is_generic=False,
            class_or_interface=False,
            needs_content=False,
            value_needed=False,
        )

    def enterInterfaceMemberDeclaration0(
        self, ctx: JavaParserLabeled.InterfaceMemberDeclaration0Context
    ):
        add_declaration(
            prefix_needed=(True, 1),
            ctx=ctx,
            which_declaration=2,
            kind_name="",
            save_dict=self.fields,
            second_parent_needed=False,
            stop_prefix=JavaParserLabeled.InterfaceMemberDeclaration0Context,
            is_generic=False,
            class_or_interface=False,
            needs_content=False,
            value_needed=True,
        )

    def enterFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        add_declaration(
            prefix_needed=(True, 2),
            ctx=ctx,
            which_declaration=3,
            kind_name="",
            save_dict=self.fields,
            second_parent_needed=False,
            stop_prefix=JavaParserLabeled.MemberDeclaration2Context,
            is_generic=False,
            class_or_interface=False,
            needs_content=False,
            value_needed=True,
        )

    def enterLocalVariableDeclaration(
        self, ctx: JavaParserLabeled.LocalVariableDeclarationContext
    ):
        is_final = ""
        if ctx.children[0].getText() == "final":
            is_final = "Final "
        add_declaration(
            prefix_needed=(False, 0),
            ctx=ctx,
            which_declaration=5,
            kind_name=f"Java {is_final}Variable Local",
            save_dict=self.local_variables,
            second_parent_needed=True,
            stop_prefix=False,
            is_generic=False,
            class_or_interface=False,
            needs_content=False,
            value_needed=True,
        )

    def enterInterfaceMethodDeclaration(
        self, ctx: JavaParserLabeled.InterfaceMethodDeclarationContext
    ):
        add_declaration(
            prefix_needed=(True, 2),
            ctx=ctx,
            which_declaration=1,
            kind_name="",
            save_dict=self.methods,
            second_parent_needed=False,
            stop_prefix=JavaParserLabeled.InterfaceMemberDeclaration1Context,
            is_generic=False,
            class_or_interface=False,
            needs_content=True,
            value_needed=False,
        )

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        add_declaration(
            prefix_needed=(True, 2),
            ctx=ctx,
            which_declaration=1,
            kind_name="",
            save_dict=self.methods,
            second_parent_needed=False,
            stop_prefix=JavaParserLabeled.MemberDeclaration0Context,
            is_generic=False,
            class_or_interface=False,
            needs_content=True,
            value_needed=False,
        )

    def enterConstructorDeclaration(
        self, ctx: JavaParserLabeled.ConstructorDeclarationContext
    ):
        add_declaration(
            prefix_needed=(True, 2),
            ctx=ctx,
            which_declaration=6,
            kind_name="",
            save_dict=self.methods,
            second_parent_needed=False,
            stop_prefix=JavaParserLabeled.MemberDeclaration3Context,
            is_generic=False,
            class_or_interface=False,
            needs_content=True,
            value_needed=False,
        )

    def enterInterfaceDeclaration(
        self, ctx: JavaParserLabeled.InterfaceDeclarationContext
    ):
        add_declaration(
            prefix_needed=(True, 1),
            ctx=ctx,
            which_declaration=4,
            kind_name="",
            save_dict=self.interfaces,
            second_parent_needed=False,
            stop_prefix=JavaParserLabeled.InterfaceDeclarationContext,
            is_generic=define_is_generic(ctx),
            class_or_interface=True,
            needs_content=True,
            value_needed=False,
        )

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        add_declaration(
            prefix_needed=(True, 1),
            ctx=ctx,
            which_declaration=4,
            kind_name="",
            save_dict=self.classes,
            second_parent_needed=False,
            stop_prefix=JavaParserLabeled.ClassDeclarationContext,
            is_generic=define_is_generic(ctx),
            class_or_interface=True,
            needs_content=True,
            value_needed=False,
        )


def get_parent_entity(file_path):
    return EntityModel.get_or_none(_longname=file_path)


def add_entity_package(package_name, file_path):
    file_entity = get_parent_entity(file_path)
    created_entity, _ = EntityModel.get_or_create(
        _kind_id=KindModel.get_or_none(_name="Java Package")._id,
        _parent_id=file_entity._id,
        _name=package_name["package_name"].split(".")[-1],
        _longname=f"{file_path}.{package_name['package_name']}",
        _contents="",
    )
    ReferenceModel.get_or_create(
        _kind_id=KindModel.get_or_none(_name="Java Define")._id,
        _file_id=file_entity._id,
        _line=package_name["line"],
        _column=package_name["column"],
        _ent_id=file_entity._id,
        _scope_id=created_entity._id,
    )
    ReferenceModel.get_or_create(
        _kind_id=KindModel.get_or_none(_name="Java Definein")._id,
        _file_id=file_entity._id,
        _line=package_name["line"],
        _column=package_name["column"],
        _ent_id=created_entity._id,
        _scope_id=file_entity._id,
    )


def define_parent(entity_type, entity_values, file_path, package_name):
    if entity_type == "class" or entity_type == "interface":
        return EntityModel.get_or_none(_longname=file_path)
    else:
        return EntityModel.get_or_none(
            _longname=f"{file_path}.{package_name}.{entity_values['parent_name']}"
        )


def add_defined_entities(entities, entity_type, package_name, file_path):
    for entity_key, entity_values in entities.items():
        is_constructor = False
        if entity_type == "method" and entity_values["type"] == "":
            is_constructor = True
        kind_str = (
            entity_values["kind_name"]
            if entity_type == "local variable" or entity_type == "parameter"
            else extract_all_kind(
                entity_values["prefixes"], entity_type, is_constructor
            )
        )

        kind_name = KindModel.get_or_none(_name=kind_str)
        kind_id = kind_name._id if kind_name else 1

        model_name = entity_values["name"]
        model_type = entity_values["type"]
        model_value = entity_values["value"]
        index_equal = model_value.find("=")
        if index_equal != -1:
            model_value = model_value[index_equal + 1 :]
        else:
            model_value = ""
        model_longname = (
            f"{file_path}.{package_name}.{entity_values['parent_name']}.{model_name}"
            if entity_values["parent_name"] != ""
            else f"{file_path}.{package_name}.{model_name}"
        )
        model_contents = entity_values["contents"]
        model_parent = define_parent(
            entity_type, entity_values, file_path, package_name
        )

        created_entity, _ = EntityModel.get_or_create(
            _kind_id=kind_id,
            _name=model_name,
            _type=model_type,
            _value=model_value,
            _longname=model_longname,
            _parent_id=model_parent._id,
            _contents=model_contents,
        )

        reference_line = entity_values["line"]
        reference_column = entity_values["column"]
        reference_file = EntityModel.get_or_none(_longname=file_path)

        ReferenceModel.get_or_create(
            _kind_id=KindModel.get_or_none(_name="Java Define")._id,
            _file_id=reference_file._id,
            _line=reference_line,
            _column=reference_column,
            _ent_id=model_parent._id,
            _scope_id=created_entity._id,
        )

        ReferenceModel.get_or_create(
            _kind_id=KindModel.get_or_none(_name="Java Definein")._id,
            _file_id=reference_file._id,
            _line=reference_line,
            _column=reference_column,
            _ent_id=created_entity._id,
            _scope_id=model_parent._id,
        )


# def main():
#     open("../../benchmark2_database.oudb")
#     files = []
#
#     # get files names
#     for ent_model in EntityModel.select():
#         if ent_model._kind_id == 1:
#             files.append(ent_model._longname)
#
#     for file_path in files:
#         try:
#             tree = get_parse_tree(file_path)
#             walker = ParseTreeWalker()
#             define_listener = DefineListener()
#             walker.walk(define_listener, tree)
#             package_name = define_listener.package["package_name"]
#             add_entity_package(define_listener.package, file_path)
#             add_defined_entities(
#                 define_listener.classes, "class", package_name, file_path
#             )
#             add_defined_entities(
#                 define_listener.interfaces, "interface", package_name, file_path
#             )
#             add_defined_entities(
#                 define_listener.fields, "variable", package_name, file_path
#             )
#             add_defined_entities(
#                 define_listener.methods, "method", package_name, file_path
#             )
#             add_defined_entities(
#                 define_listener.local_variables,
#                 "local variable",
#                 package_name,
#                 file_path,
#             )
#             add_defined_entities(
#                 define_listener.formal_parameters, "parameter", package_name, file_path
#             )
#         except Exception as e:
#             print(e)
#             print("some exception happened")
#             continue
#
#
# if __name__ == "__main__":
#     main()
