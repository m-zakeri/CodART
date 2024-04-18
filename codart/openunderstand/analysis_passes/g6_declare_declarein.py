__author__ = (
    "Parmida Majmasanaye , Zahra Momeninezhad , Bayan divaaniazar , Bavan Divaaniazar"
)
__version__ = "0.2.0"

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class DeclareAndDeclareinListener(JavaParserLabeledListener):
    def __init__(self) -> None:
        """define an array for saving entity and reference information"""

        self.declare_dicts = []

    def setDeclareDicts(self, data: dict) -> None:
        """setter to append a data to declaration array"""

        self.declare_dicts.append(data)

    def enterCompilationUnit(
        self, ctx: JavaParserLabeled.CompilationUnitContext
    ) -> None:
        """override enterCompilationUnit function to check if a file declare any package or not"""

        if not ctx.packageDeclaration():
            data = {
                "scope": None,
                "entity": None,
                "line": 1,
                "column": 0,
            }  # unnamed package
            self.setDeclareDicts(data)

    def enterPackageDeclaration(
        self, ctx: JavaParserLabeled.PackageDeclarationContext
    ) -> None:
        """override enterPackageDeclaration function to set reference information"""

        full_package_name_array = ctx.qualifiedName().IDENTIFIER()
        longname = ""

        for i in range(len(full_package_name_array)):
            entity_name = full_package_name_array[i].getText()
            entity_longname = f"{longname}{'.' if longname else ''}{entity_name}"
            [line, column] = str(ctx.start).split(",")[3].split(":")

            data = {
                "scope": None if i == 0 else full_package_name_array[i - 1].getText(),
                "entity": entity_name,
                "scope_longname": longname,
                "entity_longname": entity_longname,
                "line": line,
                "column": column.strip("]"),
            }

            self.setDeclareDicts(data)
            longname = entity_longname
