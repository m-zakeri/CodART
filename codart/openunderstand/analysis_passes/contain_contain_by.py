from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import openunderstand.analysis_passes.class_properties as class_properties


class ContainAndContainBy(JavaParserLabeledListener):
    def __init__(self):
        self.contain = []
        self.packageInfo = []

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.packageInfo = []
        longname = ""
        for x in range(len(ctx.qualifiedName().IDENTIFIER())):
            if x == 0:
                longname = str(ctx.qualifiedName().IDENTIFIER()[x])
            else:
                longname = longname + "." + str(ctx.qualifiedName().IDENTIFIER()[x])

        self.packageInfo.append(
            {
                "name": ctx.qualifiedName().IDENTIFIER()[-1],
                "longname": longname,
                "kind": "Package",
                "contents": "",
                "parent": None,
                "type": "Package",
                "value": None,
            }
        )

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        name = ctx.IDENTIFIER().getText()
        [line, col] = str(ctx.start).split(",")[3].split(":")  # line, column
        col = col[:-1]
        scope_parents = class_properties.ClassPropertiesListener.findParents(ctx)

        if len(scope_parents) == 1:
            scope_longname = scope_parents[0]
        else:
            scope_longname = ".".join(scope_parents)

        scope_longname = "." + scope_longname
        packageName = self.packageInfo[0]["name"]
        packageLongName = self.packageInfo[0]["longname"]
        scope_longname = packageLongName + scope_longname
        packageKind = self.packageInfo[0]["kind"]
        packageContent = self.packageInfo[0]["contents"]
        packageParent = self.packageInfo[0]["parent"]
        packageType = self.packageInfo[0]["type"]
        packageValue = self.packageInfo[0]["value"]

        parent = scope_parents[-2] if len(scope_parents) > 2 else None
        kind = "Class"
        modifiers = (
            class_properties.ClassPropertiesListener.findClassOrInterfaceModifiers(ctx)
        )
        content = ctx.getText()

        self.contain.append(
            {
                "package_name": packageName.getText(),
                "package_longname": packageLongName,
                "package_kind": packageKind,
                "package_content": packageContent,
                "package_parent": packageParent,
                "package_type": packageType,
                "package_value": packageValue,
                "name": name,
                "longname": scope_longname,
                "parent": parent,
                "kind": kind,
                "line": line,
                "col": col,
                "modifiers": modifiers,
                "content": content,
                "type": "Class",
                "value": None,
            }
        )
