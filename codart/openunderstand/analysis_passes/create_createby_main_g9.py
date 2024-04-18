"""

"""

import os
from fnmatch import fnmatch

from antlr4 import *

from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaLexer import JavaLexer

from oudb.models import KindModel, EntityModel, ReferenceModel
from oudb.api import open as db_open, create_db
from oudb.fill import main

from create_createby import CreateAndCreateBy
from analysis_passes.class_properties import (
    ClassPropertiesListener,
    InterfacePropertiesListener,
)

from analysis_passes.couple_coupleby import ImplementCoupleAndImplementByCoupleBy
from analysis_passes.declare_declarein import DeclareAndDeclareinListener
from analysis_passes.import_importby import ImportListener


class Project:

    tree = None

    def Parse(self, fileAddress):
        file_stream = FileStream(fileAddress, encoding="utf-8")
        lexer = JavaLexer(file_stream)
        tokens = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokens)
        tree = parser.compilationUnit()
        self.tree = tree
        return tree

    def Walk(self, listener, tree):
        walker = ParseTreeWalker()
        walker.walk(listener=listener, t=tree)

    def getListOfFiles(self, dirName):
        listOfFile = os.listdir(dirName)
        allFiles = list()
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.getListOfFiles(fullPath)
            # checks whether the fullPath content is a .java or not
            elif fnmatch(fullPath, "*.java"):
                allFiles.append(fullPath.replace("/", "\\"))

        return allFiles

    def getFileEntity(self, path):
        # kind id: 1
        path = path.replace("/", "\\")
        name = path.split("\\")[-1]
        file = open(path, mode="r")
        file_ent = EntityModel.get_or_create(
            _kind=1, _name=name, _longname=path, _contents=file.read()
        )[0]
        file.close()
        # print("processing file:", file_ent)
        return file_ent

    def addDeclareRefs(self, ref_dicts, file_ent):
        for ref_dict in ref_dicts:
            if ref_dict["scope"] is None:  # the scope is the file
                scope = file_ent
            else:  # a normal package
                scope = self.getPackageEntity(
                    file_ent, ref_dict["scope"], ref_dict["scope_longname"]
                )

            if ref_dict["ent"] is None:  # the ent package is unnamed
                ent = self.getUnnamedPackageEntity(file_ent)
            else:  # a normal package
                ent = self.getPackageEntity(
                    file_ent, ref_dict["ent"], ref_dict["ent_longname"]
                )

            # Declare: kind id 192
            declare_ref = ReferenceModel.get_or_create(
                _kind=192,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _ent=ent,
                _scope=scope,
            )

            # Declarein: kind id 193
            declarein_ref = ReferenceModel.get_or_create(
                _kind=193,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _scope=ent,
                _ent=scope,
            )

    def addCreateRefs(self, ref_dicts, file_ent, file_address):
        for ref_dict in ref_dicts:
            scope = EntityModel.get_or_create(
                _kind=self.findKindWithKeywords(
                    ref_dict["parent_type"], ref_dict["scopemodifiers"]
                ),
                _name=ref_dict["scopename"],
                _type=ref_dict["scopereturntype"],
                _parent=ref_dict["scope_parent"]
                if ref_dict["scope_parent"] is not None
                else file_ent,
                _longname=ref_dict["scopelongname"],
                _contents=["scopecontent"],
            )[0]

            ent = self.getCreatedClassEntity(
                ref_dict["refent"], ref_dict["potential_refent"], file_address
            )

            Create = ReferenceModel.get_or_create(
                _kind=190,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _scope=scope,
                _ent=ent,
            )
            Createby = ReferenceModel.get_or_create(
                _kind=191,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _scope=ent,
                _ent=scope,
            )

    def getPackageEntity(self, file_ent, name, longname):
        # package kind id: 72
        ent = EntityModel.get_or_create(
            _kind=72, _name=name, _parent=file_ent, _longname=longname, _contents=""
        )
        return ent[0]

    def getUnnamedPackageEntity(self, file_ent):
        # unnamed package kind id: 73
        ent = EntityModel.get_or_create(
            _kind=73,
            _name="(Unnamed_Package)",
            _parent=file_ent,
            _longname="(Unnamed_Package)",
            _contents="",
        )
        return ent[0]

    def getClassProperties(self, class_longname, file_address):
        listener = ClassPropertiesListener()
        listener.class_longname = class_longname.split(".")
        listener.class_properties = None
        self.Walk(listener, self.tree)
        return listener.class_properties

    def getInterfaceProperties(self, interface_longname, file_address):
        listener = InterfacePropertiesListener()
        listener.interface_longname = interface_longname.split(".")
        listener.interface_properties = None
        self.Walk(listener, self.tree)
        return listener.interface_properties

    def getCreatedClassEntity(
        self, class_longname, class_potential_longname, file_address
    ):
        props = p.getClassProperties(class_potential_longname, file_address)
        if not props:
            return self.getClassEntity(class_longname, file_address)
        else:
            return self.getClassEntity(class_potential_longname, file_address)

    def getClassEntity(self, class_longname, file_address):
        props = p.getClassProperties(class_longname, file_address)
        if not props:  # This class is unknown, unknown class id: 84
            ent = EntityModel.get_or_create(
                _kind=84,
                _name=class_longname.split(".")[-1],
                _longname=class_longname,
                _contents="",
            )
        else:
            if len(props["modifiers"]) == 0:
                props["modifiers"].append("default")
            kind = self.findKindWithKeywords("Class", props["modifiers"])
            ent = EntityModel.get_or_create(
                _kind=kind,
                _name=props["name"],
                _longname=props["longname"],
                _parent=props["parent"] if props["parent"] is not None else file_ent,
                _contents=props["contents"],
            )
        return ent[0]

    def getInterfaceEntity(
        self, interface_longname, file_address
    ):  # can't be of unknown kind!
        props = p.getInterfaceProperties(interface_longname, file_address)
        if not props:
            return None
        else:
            kind = self.findKindWithKeywords("Interface", props["modifiers"])
            ent = EntityModel.get_or_create(
                _kind=kind,
                _name=props["name"],
                _longname=props["longname"],
                _parent=props["parent"] if props["parent"] is not None else file_ent,
                _contents=props["contents"],
            )
        return ent[0]

    def getImplementEntity(self, longname, file_address):
        ent = self.getInterfaceEntity(longname, file_address)
        if not ent:
            ent = self.getClassEntity(longname, file_address)
        return ent

    def findKindWithKeywords(self, type, modifiers):
        if len(modifiers) == 0:
            modifiers.append("default")
        leastspecific_kind_selected = None
        for kind in KindModel.select().where(KindModel._name.contains(type)):
            if self.checkModifiersInKind(modifiers, kind):
                if not leastspecific_kind_selected or len(
                    leastspecific_kind_selected._name
                ) > len(kind._name):
                    leastspecific_kind_selected = kind
        return leastspecific_kind_selected

    def checkModifiersInKind(self, modifiers, kind):
        for modifier in modifiers:
            if modifier.lower() not in kind._name.lower():
                return False
        return True


# if __name__ == "__main__":
#     project_index = 5
#     project_list = [
#         "calculator_app",  # 0
#         "JSON",  # 1
#         "testing_legacy_code",  # 2
#         "105_freemind",  # 3
#         "ganttproject",  # 4
#         "jfreechart",  # 5
#         "jhotdraw-develop",  # 6
#         "jvlt-1.3.2",  # 7
#         "xerces2j",  # 8
#     ]
#
#     p = Project()
#     create_db(
#         f"../../databases/{project_list[project_index]}.db",
#         project_dir="../../benchmark",
#     )
#     main()
#     db = db_open(f"../../databases/{project_list[project_index]}.db")
#     path = f"C:\Compiler\OpenUnderstand\\benchmark\\{project_list[project_index]}"
#     java_files = p.getListOfFiles(path)
#     n = 1
#
#     for file_address in java_files:
#         try:
#             file_ent = p.getFileEntity(file_address)
#             tree = p.Parse(file_address)
#         except Exception as e:
#             print("An Error occurred in file:" + file_address + "\n" + str(e))
#             continue
#         try:
#             # create
#             listener = CreateAndCreateBy()
#             listener.create = []
#             p.Walk(listener, tree)
#             p.addCreateRefs(listener.create, file_ent, file_address)
#             entity_file_longname = "is_built_in"
#             for files in listener.create:
#                 entity_file_name = files["potential_refent"].split(".")[-1] + ".java"
#                 for file in java_files:
#                     if entity_file_name in file:
#                         entity_file_longname = file
#                         break
#                 print(f'1. refname: "Create", inverse ref name: "Java Createby"')
#                 print(
#                     f'2. ref.scope(entity performing reference)\t: "{files["scopelongname"]}", kind: "{" ".join(files["scopemodifiers"]).title()} {files["parent_type"]}"'
#                 )
#                 print(
#                     f"3. ref.entity(entity being referenced)\t\t: {entity_file_longname}"
#                 )
#                 print(
#                     f'4. location the reference occurred: "{file_address}", line: {files["line"]}'
#                 )
#                 print(n)
#                 print(f"")
#                 n = n + 1
#         except Exception as e:
#             print(
#                 "An Error occurred for reference create in file:"
#                 + file_address
#                 + "\n"
#                 + str(e)
#             )
