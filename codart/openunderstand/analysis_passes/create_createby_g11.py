"""This module is for create, Read of entities of different kinds in project,

in this module there are many classes for each individual entity as follows:
    1. File
    2. Package
    3. Parent Entities:
        Class
        Method
        Interface
"""

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

import re
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled


class CreateAndCreateBy(JavaParserLabeledListener):
    create = []

    def __init__(self, entity_manager_object):
        self.entity_manager = entity_manager_object
        self.parents = []

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.parents = self.parents + self.entity_manager.get_or_create_parent_entities(
            ctx
        )

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.parents = self.parents + self.entity_manager.get_or_create_parent_entities(
            ctx
        )

    def enterInterfaceDeclaration(
        self, ctx: JavaParserLabeled.InterfaceDeclarationContext
    ):
        self.parents = self.parents + self.entity_manager.get_or_create_parent_entities(
            ctx
        )

    def enterExpression4(self, ctx: JavaParserLabeled.Expression4Context):
        [line, col] = str(ctx.start).split(",")[3].split(":")
        parents = self.entity_manager.get_or_create_parent_entities(ctx)
        parent = parents[-1][1]
        self.create.append(
            {
                "kind": 190,
                "file": self.entity_manager.file_ent,
                "line": line,
                "column": col.replace("]", ""),
                "ent_name": re.split(r"\W+", ctx.creator().getText())[0],
                "scope": parent[0],
            }
        )
