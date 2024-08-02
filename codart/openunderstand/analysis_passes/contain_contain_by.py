from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import openunderstand.analysis_passes.class_properties as class_properties


class ContainAndContainBy(JavaParserLabeledListener):
    def __init__(self, file_address):
        self.contain = []
        self.packageInfo = []
        self.file_address = file_address

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.packageInfo = []
        longname = ""
        for x in range(len(ctx.qualifiedName().IDENTIFIER())):
            if x == 0:
                longname = str(ctx.qualifiedName().IDENTIFIER()[x])
            else:
                longname = longname + "." + str(ctx.qualifiedName().IDENTIFIER()[x])
        addr = self.file_address
        addr = addr.replace("/", ".").replace("\\", ".").split(".")
        addr.pop()
        par = addr[len(addr) - 1] + ".java"
        self.packageInfo.append(
            {
                "name": ctx.qualifiedName().IDENTIFIER()[-1],
                "longname": longname,
                "kind": "Package",
                "contents": ctx.getText(),
                "parent": par,
                "type": "Package",
                "value": None,
            }
        )

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        name = ctx.IDENTIFIER().getText()
        [line, col] = str(ctx.start).split(",")[3].split(":")  # line, column
        col = col[:-1]
        # scope_parents = class_properties.ClassPropertiesListener.findParents(ctx)
        b = ctx.parentCtx
        base = b.parentCtx.getChild(0)
        pack_seq = base.getChild(1).getText()
        scope_parents = pack_seq
        scope_longname = scope_parents+"."+b.getChild(1).getChild(1).getText()

        # scope_longname = "." + scope_longname
        packageName = self.packageInfo[0]["name"]
        packageLongName = self.packageInfo[0]["longname"]
        # scope_longname = packageLongName + scope_longname
        packageKind = self.packageInfo[0]["kind"]
        packageContent = self.packageInfo[0]["contents"]
        packageParent = self.packageInfo[0]["parent"]
        packageType = self.packageInfo[0]["type"]
        packageValue = self.packageInfo[0]["value"]

        addr = self.file_address
        addr = addr.replace("/", ".").replace("\\", ".").split(".")
        addr.pop()
        par = addr[len(addr) - 1] + ".java"

        parent = par
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
