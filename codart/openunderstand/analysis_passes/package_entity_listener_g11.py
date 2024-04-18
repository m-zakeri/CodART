"""This module is for create, Read of entities of type package."""

__author__ = "Navid Mousavizadeh, Amir Mohammad Sohrabi, Sara Younesi, Deniz Ahmadi"
__copyright__ = "Copyright 2022, The OpenUnderstand Project, Iran University of Science and technology"
__credits__ = [
    "Dr.Parsa",
    "Dr.Zakeri",
    "Mehdi Razavi",
    "Navid Mousavizadeh",
    "Amir Mohammad Sohrabi",
    "Sara Younesi",
    "Deniz Ahmadi",
]
__license__ = "GPL"
__version__ = "1.0.0"

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class PackageListener(JavaParserLabeledListener):
    """A listener class for detecting package"""

    def __init__(self):
        self.package_data = None

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        package_parts = ctx.getText().replace(";", "").replace("package", "").split(".")
        for i in range(len(package_parts)):
            self.package_data.append(
                {
                    "package_name": package_parts[i],
                    "package_longname": ".".join(package_parts[: i + 1]),
                }
            )
