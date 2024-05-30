from openunderstand.ounderstand.project import Project
from collections import Counter
from antlr4 import *
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from openunderstand.metrics.utils_g10 import get_method_prefixes
from gen.javaLabeled.JavaLexer import JavaLexer




def make_enum_scope():
    return [
        {
            "kind": "Java Method Public Member",
            "name": "values",
            "longname": "",
            "cyclomatic": 1,
        },
        {
            "kind": "Java Method Public Member",
            "name": "valueOf",
            "longname": "",
            "cyclomatic": 1,
        },
    ]


def make_method_scope(ctx):
    prefixes = get_method_prefixes(ctx)
    name = ""
    kind = ""
    if type(ctx).__name__ == "MethodDeclarationContext":
        name = ctx.IDENTIFIER().getText()
        if name == "main":
            is_main = True
        else:
            is_main = False
        kind = get_kind_name(prefixes, is_main=is_main)
    elif type(ctx).__name__ == "GenericMethodDeclarationContext":
        name = ctx.children[1].IDENTIFIER().getText()
        kind = get_kind_name(prefixes, is_generic=True)
    elif type(ctx).__name__ == "ConstructorDeclarationContext":
        name = ctx.IDENTIFIER().getText()
        kind = get_kind_name(prefixes, is_constructor=True)
    elif type(ctx).__name__ == "GenericConstructorDeclarationContext":
        name = ctx.children[1].IDENTIFIER().getText()
        kind = get_kind_name(prefixes, is_constructor=True, is_generic=True)
    elif type(ctx).__name__ == "LambdaExpressionContext":
        name = "(lambda_expr)"
        kind = get_kind_name(prefixes, is_lambda=True)

    return {"kind": kind, "name": name, "longname": ""}


def get_kind_name(
    prefixes, is_constructor=False, is_lambda=False, is_generic=False, is_main=False
):
    p_static = ""
    p_final = ""
    p_generic = ""
    p_main = ""

    if "static" in prefixes:
        p_static = "Static"

    if "final" in prefixes:
        p_final = "Final"

    if is_generic:
        p_generic = "Generic"

    if "private" in prefixes:
        p_visibility = "Private"
    elif "public" in prefixes:
        p_visibility = "Public"
    elif "protected" in prefixes:
        p_visibility = "Protected"
    else:
        p_visibility = "Default"

    if is_main:
        p_main = "Main"

    if is_constructor:
        s = f"Java Method Constructor Member {p_visibility}"
        s = " ".join(s.split())
        return s

    elif is_lambda:
        s = f"Java Method Lambda"
        s = " ".join(s.split())
        return s

    else:
        s = f"Java {p_static} {p_final} {p_generic} Method {p_visibility} {p_main} Member"
        s = " ".join(s.split())
        return s


def get_method_ctx(ctx):
    # Traverse bottom up until reaching a method
    current = ctx.parentCtx
    while current is not None:
        type_name = type(current).__name__
        if type_name in [
            "MethodDeclarationContext",
            "GenericMethodDeclarationContext",
            "ConstructorDeclarationContext",
            "GenericConstructorDeclarationContext",
        ]:
            return current
        current = current.parentCtx
    return None


class CyclomaticListener(JavaParserLabeledListener):
    def __init__(self):
        # repository of ctx
        self.repository = []
        self.project_cyclomatic = 0

    def update_repository(self, ctx, kind=None):
        if kind:
            scope_ctx = ctx

        else:
            scope_ctx = get_method_ctx(ctx)
            if scope_ctx is None:
                return

            parent_scope_ctx = scope_ctx.parentCtx
            if type(parent_scope_ctx).__name__ in [
                "GenericMethodDeclarationContext",
                "GenericConstructorDeclarationContext",
            ]:
                scope_ctx = parent_scope_ctx

        prefixes = get_method_prefixes(scope_ctx)
        if "abstract" not in prefixes:
            self.repository.append(scope_ctx)
            self.project_cyclomatic += 1

    def enterGenericMethodDeclaration(
        self, ctx: JavaParserLabeled.GenericMethodDeclarationContext
    ):
        self.update_repository(ctx, kind="GenericMethodDeclarationContext")

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        # Parent can be genericMethodDeclaration
        if type(ctx.parentCtx).__name__ == "GenericMethodDeclarationContext":
            return
        self.update_repository(ctx, kind="MethodDeclarationContext")

    def enterGenericConstructorDeclaration(
        self, ctx: JavaParserLabeled.GenericConstructorDeclarationContext
    ):
        self.update_repository(ctx, kind="GenericConstructorDeclarationContext")

    def enterConstructorDeclaration(
        self, ctx: JavaParserLabeled.ConstructorDeclarationContext
    ):
        # Parent can be genericConstructorDeclaration
        if type(ctx.parentCtx).__name__ == "GenericConstructorDeclarationContext":
            return
        self.update_repository(ctx, kind="ConstructorDeclarationContext")

    def enterEnumDeclaration(self, ctx: JavaParserLabeled.EnumDeclarationContext):
        # valueOf and values for Enums
        self.repository.append(ctx)
        self.project_cyclomatic += 2

    def enterLambdaExpression(self, ctx: JavaParserLabeled.LambdaExpressionContext):
        self.repository.append(ctx)
        self.project_cyclomatic += 1

    # while
    def enterStatement4(self, ctx: JavaParserLabeled.Statement4Context):
        self.update_repository(ctx)

    # ternary
    def enterExpression20(self, ctx: JavaParserLabeled.Expression20Context):
        self.update_repository(ctx)

    # if
    def enterStatement2(self, ctx: JavaParserLabeled.Statement2Context):
        self.update_repository(ctx)

    # for
    def enterStatement3(self, ctx: JavaParserLabeled.Statement3Context):
        self.update_repository(ctx)

    # do
    def enterStatement5(self, ctx: JavaParserLabeled.Statement5Context):
        self.update_repository(ctx)

    # catch
    def enterCatchClause(self, ctx: JavaParserLabeled.CatchClauseContext):
        self.update_repository(ctx)

    # case
    def enterSwitchLabel(self, ctx: JavaParserLabeled.SwitchLabelContext):
        if ctx.children[0].getText() == "case":
            self.update_repository(ctx)


def cyclomatic(ent_model):
    p = Project()
    listener = CyclomaticListener()
    lexer = JavaLexer(InputStream(ent_model.contents()))
    tokens = CommonTokenStream(lexer)
    parser = JavaParserLabeled(tokens)
    return_tree = parser.compilationUnit()
    p.Walk(reference_listener=listener, parse_tree=return_tree)
    cyclomatic_listener = listener
    cyclomatic_list = []
    ent_kind_set = set()
    cyclomatic_counter = Counter(cyclomatic_listener.repository)
    for ctx in cyclomatic_counter:
        cyclomatic = cyclomatic_counter[ctx]
        if type(ctx).__name__ == "EnumDeclarationContext":
            cyclomatic_list.extend(make_enum_scope())
        else:
            cyclomatic_obj = make_method_scope(ctx)
            cyclomatic_obj["val"] = cyclomatic
            cyclomatic_list.append(cyclomatic_obj)
            ent_kind_set.add(cyclomatic_obj["kind"])
    return cyclomatic_listener.project_cyclomatic
