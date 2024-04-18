from antlr4 import *
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from oudb.models import KindModel, EntityModel, ReferenceModel
from analysis_passes.import_importby_g10_2 import (
    Project,
    get_parse_tree,
    get_project_info,
    get_kind_name,
    get_parent,
)

PRJ_INDEX = 0
REF_NAME = "modify"


def get_prefixes(ctx, ctx_type):
    branches = ctx.parentCtx.children
    prefixes = ""
    for branch in branches:
        if type(branch).__name__ == ctx_type:
            break
        prefixes += branch.getText() + " "
    return prefixes


class ClassListener(JavaParserLabeledListener):
    def __init__(self, files, file_name):
        self.files = files
        self.file_name = file_name

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        parent_entity, parent_file_path = get_parent(self.file_name, self.files)
        prefixes = get_prefixes(ctx, "ClassDeclarationContext")
        kind_name = get_kind_name(prefixes, kind="Class")
        obj, _ = EntityModel.get_or_create(
            _kind=KindModel.get_or_none(_name=kind_name).get_id(),
            _parent=parent_entity.get_id(),
            _name=ctx.IDENTIFIER().getText(),
            _longname=parent_file_path,
            _contents=ctx.getText(),
        )


class ModifyListener(JavaParserLabeledListener):
    def __init__(self, files, file_name):
        self.files = files
        self.file_name = file_name

    @staticmethod
    def search_scope(ctx, type_names):
        # Traverse bottom up until reaching a class or method
        current = ctx.parentCtx
        while current is not None:
            type_name = type(current).__name__
            if type_name in type_names:
                return current
            current = current.parentCtx
        return None

    def make_scope_class(self, ctx, file_name):
        prefixes = get_prefixes(ctx, "ClassDeclarationContext")
        kind_name = get_kind_name(prefixes, kind="Class")
        kind_id = KindModel.get_or_none(_name=kind_name).get_id()
        name = ctx.IDENTIFIER().getText()
        parent_entity, parent_file_path = get_parent(file_name, self.files)
        content = ctx.getText()

        obj = EntityModel.get_or_none(
            _kind=KindModel.get_or_none(_name=kind_name).get_id(),
            _parent=parent_entity.get_id(),
            _name=name,
            _longname=parent_file_path,
        )
        return {
            "id": obj.get_id(),
            "kind_id": kind_id,
            "parent_id": parent_entity.get_id(),
            "name": name,
            "longname": parent_file_path,
            "content": content,
        }

    def make_scope_method(self, ctx, file_name):
        prefixes = get_prefixes(ctx, "MethodDeclarationContext")
        kind_name = get_kind_name(prefixes, kind="Method")
        kind_id = KindModel.get_or_none(_name=kind_name).get_id()
        name = ctx.IDENTIFIER().getText()
        content = ctx.getText()
        parent_ctx = self.search_scope(ctx, ["ClassDeclarationContext"])
        parent_entity = self.make_scope_class(parent_ctx, file_name)

        obj, _ = EntityModel.get_or_create(
            _kind=kind_id,
            _parent=parent_entity["id"],
            _name=name,
            _longname=f"{parent_entity['name']}.{name}",
            _contents=content,
        )
        return {
            "id": obj.get_id(),
            "kind_id": kind_id,
            "parent_id": parent_entity["id"],
            "name": name,
            "longname": f"{parent_entity['name']}.{name}",
            "content": content,
        }

    def enterExpression6(self, ctx: JavaParserLabeled.Expression6Context):
        self.modify_deref_partial(ctx)

    def enterExpression21(self, ctx: JavaParserLabeled.Expression21Context):
        self.modify_deref_partial(ctx)

    def modify_deref_partial(self, ctx):
        lhs_text = ctx.children[0].getText()
        scope = None
        if "[" in lhs_text and "]" in lhs_text:
            var_name = ctx.children[0].children[0].getText()
            var_entity = add_var_entity(var_name)

            line, col = str(ctx.start).split(",")[3][:-1].split(":")

            file_entity, _ = get_parent(self.file_name, self.files)
            file_id = file_entity.get_id()

            ref_dict = {
                "line": line,
                "column": col,
                "file_id": file_id,
                "text": ctx.getText(),
            }

            scope_ctx = self.search_scope(
                ctx, ["ClassDeclarationContext", "MethodDeclarationContext"]
            )
            if type(scope_ctx).__name__ == "ClassDeclarationContext":
                scope = self.make_scope_class(scope_ctx, self.file_name)
            elif type(scope_ctx).__name__ == "MethodDeclarationContext":
                scope = self.make_scope_method(scope_ctx, self.file_name)

            add_references(scope, var_entity, ref_dict)


def add_var_entity(var_name):
    obj, _ = EntityModel.get_or_create(
        _kind=KindModel.get_or_none(_name="Java Unresolved Variable").get_id(),
        _name=var_name,
        _longname=var_name,
    )
    return {
        "id": obj.get_id(),
        "kind_id": KindModel.get_or_none(_name="Java Unresolved Variable").get_id(),
        "name": var_name,
        "longname": var_name,
    }


def add_references(scope, ent, ref_dict):
    ref, _ = ReferenceModel.get_or_create(
        _kind=KindModel.get_or_none(_name="Java Modify Deref Partial").get_id(),
        _file=ref_dict["file_id"],
        _line=ref_dict["line"],
        _column=ref_dict["column"],
        _ent=ent["id"],
        _scope=scope["id"],
    )
    inverse_ref, _ = ReferenceModel.get_or_create(
        _kind=KindModel.get_or_none(_name="Java Modifyby Deref Partial").get_id(),
        _file=ref_dict["file_id"],
        _line=ref_dict["line"],
        _column=ref_dict["column"],
        _ent=scope["id"],
        _scope=ent["id"],
    )

    # print(ref_dict['text'])
    # print(f'1. ref name: Java Modify Deref Partial')
    # print(f'2. ref scope: {scope["longname"]} || kind: {KindModel.get_or_none(_id=scope["kind_id"])._name}')
    # print(f'3. ref ent: {ent["longname"]} || kind: Java Variable')
    # print(f'4. file location: {EntityModel.get_or_none(_id=ref_dict["file_id"])} || line: {ref_dict["line"]}')
    # print("-" * 25)


def main():
    info = get_project_info(PRJ_INDEX, REF_NAME)
    p = Project(info["DB_PATH"], info["PROJECT_PATH"], info["PROJECT_NAME"])
    p.init_db()
    p.get_java_files()

    for file_name, file_path in p.files:
        tree = get_parse_tree(file_path)
        walker = ParseTreeWalker()

        class_listener = ClassListener(p.files, file_name)
        listener = ModifyListener(p.files, file_name)

        walker.walk(class_listener, tree)
        walker.walk(listener, tree)


if __name__ == "__main__":
    main()
