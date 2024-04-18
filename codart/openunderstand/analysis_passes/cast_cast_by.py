from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import openunderstand.analysis_passes.class_properties as class_properties


class ClassEntities:
    def __init__(self, name, parent, kind, content, longname, modifiers):
        self.modifiers = modifiers
        self.name = name
        self.parent = parent
        self.kind = kind
        self.content = content
        self.longname = longname
        self.type = None
        self.value = None


class implementListener(JavaParserLabeledListener):
    def __init__(
        self,
    ):
        self.classes = []

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        name = ctx.IDENTIFIER().getText()
        scope_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        if len(scope_parents) == 1:
            scope_longname = scope_parents[0]
        else:
            scope_longname = ".".join(scope_parents)

        EntityClass = ClassEntities(
            name,
            scope_parents[-2] if len(scope_parents) > 2 else None,
            "Class",
            ctx.getText(),
            scope_longname,
            class_properties.ClassPropertiesListener.findClassOrInterfaceModifiers(ctx),
        )
        self.classes.append(EntityClass)


class CastAndCastBy(JavaParserLabeledListener):
    classes = []
    cast = []

    def __init__(self, classes):
        self.classes = classes
        self.cast = []
        self.c_name = ""
        self.c_longname = ""
        self.c_parent = ""
        self.c_kind = ""
        self.c_content = ""
        self.c_modifiers = ""

    def enterExpression5(self, ctx: JavaParserLabeled.Expression5Context):
        self.c_name = ""
        self.c_longname = ""
        self.c_parent = ""
        self.c_kind = ""
        self.c_content = ""
        self.c_modifiers = ""

        name = ctx.typeType().getText()
        scope_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        [line, col] = str(ctx.start).split(",")[3].split(":")  # line, column
        col = col[:-1]

        if len(scope_parents) >= 2:
            parent = scope_parents[-2]
        else:
            parent = None
        for ent in self.classes:
            if ent.name == name:
                self.c_name = name
                self.c_longname = ent.longname
                self.c_parent = ent.parent
                self.c_kind = ent.kind
                self.c_content = ent.content
                self.c_modifiers = ent.modifiers

        for ent in self.classes:
            if self.c_name != "":
                if ent.name == parent:
                    self.cast.append(
                        {
                            "name": self.c_name,
                            "longname": self.c_longname,
                            "parent": self.c_parent,
                            "kind": self.c_kind,
                            "content": self.c_content,
                            "modifier": self.c_modifiers,
                            "p_name": ent.name,
                            "p_longname": ent.longname,
                            "p_parent": ent.parent,
                            "p_kind": ent.kind,
                            "p_content": ent.content,
                            "p_modifier": ent.modifiers,
                            "line": line,
                            "col": col,
                            "ent": ent,
                        }
                    )
