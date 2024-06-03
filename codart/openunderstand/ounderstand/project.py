"""This module is the main part for creating all entities and references in database. our task was the javaModify and
javaCreate and their reverse references. """

import logging
import os
from fnmatch import fnmatch
from antlr4 import *
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaLexer import JavaLexer
from openunderstand.oudb.models import KindModel, EntityModel, ReferenceModel
from openunderstand.analysis_passes.modify_modifyby import ModifyListener
from openunderstand.analysis_passes.g6_class_properties import (
    ClassPropertiesListener,
    InterfacePropertiesListener,
)

from openunderstand.utils.utilities import ClassTypeData

# from utils.antler_parser import _cpp_parse


class Project:
    def __init__(self):
        self.tree = None

    @staticmethod
    def listToString(s):
        """a method to find projects path dynamically"""
        str1 = ""
        for ele in s[0 : len(s) - 1]:
            str1 += ele + "\\"
        return str1

    def Parse(self, fileAddress):
        file_stream = FileStream(fileAddress, encoding="utf8")
        lexer = JavaLexer(file_stream)
        tokens = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokens)
        return_tree = parser.compilationUnit()
        # return_tree = _cpp_parse(
        #     stream=file_stream, java_parser_labeld=JavaParserLabeled
        # )
        self.tree = return_tree
        return return_tree

    @staticmethod
    def Walk(reference_listener, parse_tree):
        walker = ParseTreeWalker()
        walker.walk(listener=reference_listener, t=parse_tree)

    def getListOfFiles(self, dirName):
        listOfFile = os.listdir(dirName)
        allFiles = list()
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.getListOfFiles(fullPath)
            elif fnmatch(fullPath, "*.java"):
                allFiles.append(fullPath)
        return allFiles

    def getFileEntity(self, path: str = "", name: str = ""):
        # kind id: 1
        file = open(path, mode="r")
        file_ent = EntityModel.get_or_create(
            _kind=1, _name=name, _longname=path, _contents=file.read()
        )[0]
        file.close()
        print("processing file:", file_ent)
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

    def addTypeRefs(self, d_type, file_ent, stream: str = ""):
        for type_tuple in d_type["typedBy"]:
            ent, h_c1 = EntityModel.get_or_create(
                _kind=224,
                _parent=None,
                _name=type_tuple[1],
                _longname=type_tuple[6] + "." + type_tuple[1],
                _value=None,
                _type=None,
                _contents=stream,
            )

            scope, h_c2 = EntityModel.get_or_create(
                _kind=225,
                _parent=None,
                _name=type_tuple[0],
                _longname=type_tuple[6] + "." + type_tuple[0],
                _value=None,
                _type=None,
                _contents=stream,
            )

            # 224		Java Typed
            typed_ref = ReferenceModel.get_or_create(
                _kind=224,
                _file=scope,
                _line=type_tuple[4],
                _column=type_tuple[5],
                _ent=ent,
                _scope=scope,
            )
            # 225    	Java Typedby
            typedby_ref = ReferenceModel.get_or_create(
                _kind=225,
                _file=ent,
                _line=type_tuple[2],
                _column=type_tuple[3],
                _ent=scope,
                _scope=ent,
            )

    def addSetRefs(self, d, file_ent, stream: str = ""):

        for type_tuple in d:
            par = EntityModel.get(_name=type_tuple[7])
            ss = str(type_tuple[1]).rfind(".")
            ent, h_c1 = EntityModel.get_or_create(
                _kind=222,
                _parent=par._id,
                _name=type_tuple[0],
                _longname=type_tuple[1],
                _value=type_tuple[3],
                _type=type_tuple[9],
                _contents="",
            )

            scope, h_c2 = EntityModel.get_or_create(
                _kind=223,
                _parent=None,
                _name=type_tuple[10],  # PROBLEM
                _longname=str(type_tuple[1])[:ss],
                _value=None,
                _type=type_tuple[3],
                _contents=type_tuple[8],
            )
            # 222: Java Set
            set_ref = ReferenceModel.get_or_create(
                _kind=222,
                _file=scope,
                _line=type_tuple[4],
                _column=type_tuple[5],
                _ent=ent,
                _scope=scope,
            )
            # 223: Java Setby
            setby_ref = ReferenceModel.get_or_create(
                _kind=223,
                _file=ent,
                _line=type_tuple[4],
                _column=type_tuple[5],
                _ent=scope,
                _scope=ent,
            )

    def addSetInitRefs(self, d, file_ent, stream: str = ""):
        for type_tuple in d:
            ss = str(type_tuple[1]).rfind(".")
            par = EntityModel.get(_name=type_tuple[7])
            ent, h_c1 = EntityModel.get_or_create(
                _kind=218,
                _parent=par._id,
                _name=type_tuple[0],
                _longname=type_tuple[1],
                _value=type_tuple[3],
                _type=type_tuple[8],
                _contents="",
            )

            scope, h_c2 = EntityModel.get_or_create(
                _kind=219,
                _parent=None,
                _name=type_tuple[10],  # PROBLEM
                _longname=str(type_tuple[1])[:ss],
                _value=None,
                _type=type_tuple[3],
                _contents=type_tuple[9],
            )
            # 222: Java SetInit
            set_init_ref = ReferenceModel.get_or_create(
                _kind=218,
                _file=scope,
                _line=type_tuple[5],
                _column=type_tuple[6],
                _ent=ent,
                _scope=scope,
            )
            # 223: Java SetInitby
            setby_init_ref = ReferenceModel.get_or_create(
                _kind=219,
                _file=ent,
                _line=type_tuple[5],
                _column=type_tuple[6],
                _ent=scope,
                _scope=ent,
            )

    def addSetPartialRefs(self, d, file_ent, stream: str = ""):

        for type_tuple in d:
            ss = str(type_tuple[1]).rfind(".")
            par = EntityModel.get(_name=type_tuple[7])
            ent, h_c1 = EntityModel.get_or_create(
                _kind=220,
                _parent=par._id,
                _name=type_tuple[0],
                _longname=type_tuple[1],
                _value=type_tuple[3],
                _type=type_tuple[8],
                _contents="",
            )

            scope, h_c2 = EntityModel.get_or_create(
                _kind=221,
                _parent=None,
                _name=type_tuple[7],  # PROBLEM
                _longname=str(type_tuple[1])[:ss],
                _value=None,
                _type=type_tuple[3],
                _contents=type_tuple[9],
            )
            # 222: Java Set Partial
            set_partial_ref = ReferenceModel.get_or_create(
                _kind=220,
                _file=scope,
                _line=type_tuple[4],
                _column=type_tuple[5],
                _ent=ent,
                _scope=scope,
            )
            # 223: Java Setby Partial
            setby_partial_ref = ReferenceModel.get_or_create(
                _kind=221,
                _file=ent,
                _line=type_tuple[4],
                _column=type_tuple[5],
                _ent=scope,
                _scope=ent,
            )

    def addUseRefs(self, d_use, file_ent, stream: str = ""):
        for use_tuple in d_use:
            ent, h_c1 = EntityModel.get_or_create(
                _kind=226,
                _parent=None,
                _name=use_tuple[1],
                _longname=use_tuple[6] + "." + use_tuple[1],
                _value=None,
                _type=None,
                _contents=stream,
            )

            scope, h_c2 = EntityModel.get_or_create(
                _kind=227,
                _parent=None,
                _name=use_tuple[0],
                _longname=use_tuple[6] + "." + use_tuple[0],
                _value=None,
                _type=None,
                _contents=stream,
            )

            # 226		Java Use
            use_ref = ReferenceModel.get_or_create(
                _kind=226,
                _file=file_ent,
                _line=use_tuple[4],
                _column=use_tuple[5],
                _ent=ent,
                _scope=scope,
            )
            # 227	 	Java Useby
            useby_ref = ReferenceModel.get_or_create(
                _kind=227,
                _file=file_ent,
                _line=use_tuple[2],
                _column=use_tuple[3],
                _ent=scope,
                _scope=ent,
            )

    def addDefineRefs(self, ref_dicts, file_ent):

        for ref_dict in ref_dicts:
            if ref_dict["scope"] is None:  # the scope is the file
                scope = file_ent
            else:  # a normal package
                scope = self.getPackageEntity(
                    file_ent, ref_dict["scope"], ref_dict["scope_longname"]
                )

            ent = self.getPackageEntity(
                file_ent, ref_dict["ent"], ref_dict["ent_longname"]
            )
            # print("ref_dict[parent] : ", ref_dict["parent"])
            # print("ref_dict[parent] : ", type(ref_dict["parent"]))
            par = EntityModel.get(_longname=ref_dict["parent"])
            ent, h_c1 = EntityModel.get_or_create(
                _kind=194,
                _parent=par._id,
                _name=ref_dict["ent"],
                _longname=ref_dict["ent_longname"],
                _value=None,
                _type=ref_dict["type"],
                _contents=ref_dict["contents"],
            )

            # scope, h_c2 = EntityModel.get_or_create(
            #     _kind=195,
            #     _parent=None,
            #     _name=type_tuple[10],  # PROBLEM
            #     _longname=str(type_tuple[1])[:ss],
            #     _value=None,
            #     _type=type_tuple[3],
            #     _contents=type_tuple[8],
            # )
            if file_ent._name == "JSONML.java":
                print("file_ent : ", file_ent._name)
                print("scope : ", scope._name)
            # Define: kind id 194
            define_ref = ReferenceModel.get_or_create(
                _kind=194,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _ent=ent,
                _scope=scope,
            )

            # Definein: kind id 195
            definein_ref = ReferenceModel.get_or_create(
                _kind=195,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _scope=ent,
                _ent=scope,
            )

    def addImplementOrImplementByRefs(self, ref_dicts, file_ent, file_address):
        pass

    def add_create_and_createby_reference(self, ref_dicts, file_address, file_ent):
        for ref_dict in ref_dicts:
            scope = EntityModel.get_or_create(
                _kind=self.findKindWithKeywords(
                    ref_dict["scope_kind"], ref_dict["scope_modifiers"]
                ),
                _name=ref_dict["scope_name"],
                _parent=(
                    ref_dict["scope_parent"]
                    if ref_dict["scope_parent"] is not None
                    else file_ent
                ),
                _longname=ref_dict["scope_longname"],
                _contents=ref_dict["scope_contents"],
            )[0]
            ent = self.getImplementEntity(
                ref_dict["type_ent_longname"], file_address, file_ent
            )
            implement_ref = ReferenceModel.get_or_create(
                _kind=188,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _ent=ent,
                _scope=scope,
            )
            implementBy_ref = ReferenceModel.get_or_create(
                _kind=189,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _ent=scope,
                _scope=ent,
            )

    def add_references_extend_implicit_couple(
        self, importing_ent, imported_ent, cls_data
    ):
        ref, _ = ReferenceModel.get_or_create(
            _kind=KindModel.get_or_none(_name="Java Extend Couple Implicit")._id,
            _file_id=importing_ent._id,
            _line=cls_data.line,
            _column=cls_data.column,
            _ent_id=imported_ent._id,
            _scope_id=importing_ent._id,
        )
        inverse_ref, _ = ReferenceModel.get_or_create(
            _kind=KindModel.get_or_none(_name="Java Extend Coupleby Implicit")._id,
            _file_id=importing_ent._id,
            _line=cls_data.line,
            _column=cls_data.column,
            _ent_id=importing_ent._id,
            _scope_id=imported_ent._id,
        )

    def addExtendCoupleOrExtendCoupleByRefs(self, ref_dicts, file_ent, file_address):
        for ref_dict in ref_dicts:
            scope = EntityModel.get_or_create(
                _kind=self.findKindWithKeywords(
                    ref_dict["scope_kind"], ref_dict["scope_modifiers"]
                ),
                _name=ref_dict["scope_name"],
                _parent=(
                    ref_dict["scope_parent"]
                    if ref_dict["scope_parent"] is not None
                    else file_ent
                ),
                _longname=ref_dict["scope_longname"],
                _contents=ref_dict["scope_contents"],
            )[0]
            ent = self.getImplementEntity(
                ref_dict["type_ent_longname"], file_address, file_ent
            )
            extend_ref = ReferenceModel.get_or_create(
                _kind=178,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _ent=ent,
                _scope=scope,
            )
            extendBy_ref = ReferenceModel.get_or_create(
                _kind=179,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _ent=scope,
                _scope=ent,
            )

    def addCallOrCallByRefs(self, ref_dicts, file_ent, file_address):
        for ref_dict in ref_dicts:
            scope = EntityModel.get_or_create(
                _kind=self.findKindWithKeywords(
                    ref_dict["scope_kind"], ref_dict["scope_modifiers"]
                ),
                _name=ref_dict["scope_name"],
                _parent=(
                    ref_dict["scope_parent"]
                    if ref_dict["scope_parent"] is not None
                    else file_ent
                ),
                _longname=ref_dict["scope_longname"],
                _contents=ref_dict["scope_contents"],
            )[0]
            ent = self.getImplementEntity(
                ref_dict["type_ent_longname"], file_address, file_ent
            )
            call_ref = ReferenceModel.get_or_create(
                _kind=172,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _ent=ent,
                _scope=scope,
            )
            callBy_ref = ReferenceModel.get_or_create(
                _kind=173,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _ent=scope,
                _scope=ent,
            )

    @staticmethod
    def add_modify_and_modifyby_reference(ref_dicts):
        for ref_dict in ref_dicts:
            longname = ref_dict["ent"]
            ent = ModifyListener.get_different_combinations(longname)
            scope = ref_dict["scope"]
            _, _ = ReferenceModel.get_or_create(
                _kind=208,
                _file=ref_dict["file"],
                _line=ref_dict["line"],
                _column=ref_dict["column"],
                _ent=ent if ent is not None else "NOT FOUND",
                _scope=scope,
            )
            _, _ = ReferenceModel.get_or_create(
                _kind=209,
                _file=ref_dict["file"],
                _line=ref_dict["line"],
                _column=ref_dict["column"],
                _ent=scope,
                _scope=ent if ent is not None else "NOT FOUND",
            )

    def addCallNonDynamicOrCallNonDynamicByRefs(
        self, ref_dicts, file_ent, file_address
    ):
        for ref_dict in ref_dicts:
            scope = EntityModel.get_or_create(
                _kind=self.findKindWithKeywords(
                    ref_dict["scope_kind"], ref_dict["scope_modifiers"]
                ),
                _name=ref_dict["scope_name"],
                _parent=(
                    ref_dict["scope_parent"]
                    if ref_dict["scope_parent"] is not None
                    else file_ent
                ),
                _longname=ref_dict["scope_longname"],
                _contents=ref_dict["scope_contents"],
            )[0]
            ent = self.getImplementEntity(
                ref_dict["type_ent_longname"], file_address, file_ent
            )
            call_ref = ReferenceModel.get_or_create(
                _kind=170,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _ent=ent,
                _scope=scope,
            )
            callBy_ref = ReferenceModel.get_or_create(
                _kind=171,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _ent=scope,
                _scope=ent,
            )

    def add_cast_by(self, ref_dicts_all, file_ent, file_address):
        for ref_dicts in ref_dicts_all:
            scope = EntityModel.get_or_create(
                _kind=self.findKindWithKeywords(
                    ref_dicts["p_kind"], ref_dicts["p_modifier"]
                ),
                _name=ref_dicts["p_name"],
                _parent=(
                    ref_dicts["p_parent"]
                    if ref_dicts["p_parent"] is not None
                    else file_ent
                ),
                _longname=ref_dicts["p_longname"],
                _contents=ref_dicts["p_content"],
            )[0]
            ent = self.getImplementEntity(ref_dicts["longname"], file_address, file_ent)

            cast = ReferenceModel.get_or_create(
                _kind=174,
                _file=file_ent,
                _line=ref_dicts["line"],
                _column=ref_dicts["col"],
                _scope=scope,
                _ent=ent,
            )
            castby = ReferenceModel.get_or_create(
                _kind=175,
                _file=file_ent,
                _line=ref_dicts["line"],
                _column=ref_dicts["col"],
                _scope=ent,
                _ent=scope,
            )

    def add_contain_in(self, ref_dicts, file_ent, file_address):
        for ref_dict in ref_dicts:
            scope = EntityModel.get_or_create(
                _kind=self.findKindWithKeywords(
                    ref_dict["kind"], ref_dict["modifiers"]
                ),
                _name=ref_dict["name"],
                _parent=(
                    ref_dict["parent"] if ref_dict["parent"] is not None else file_ent
                ),
                _longname=ref_dict["longname"],
                _contents=ref_dict["content"],
            )[0]
            ent = self.getImplementEntity(
                ref_dict["package_type"], file_address, file_ent
            )
            contain = ReferenceModel.get_or_create(
                _kind=176,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _scope=ent,
                _ent=scope,
            )

            containin = ReferenceModel.get_or_create(
                _kind=177,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _scope=scope,
                _ent=ent,
            )

    def get_parent(self, parent_file_path) -> EntityModel:
        return EntityModel.get_or_none(_longname=parent_file_path)

    def getNameEntity(self, prefixes) -> str:
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

        result_str = "Java{0}{1}{2} Class Type{3} Member".format(
            pattern_static, pattern_abstract, pattern_generic, pattern_visibility
        )
        return result_str

    def get_imported_entity(self, import_entity_listener):
        prefixes = ""
        kind = ""
        for branch in import_entity_listener.branches:
            if type(branch) == JavaParserLabeled.ClassDeclarationContext:
                kind = "Class"
                break
            elif type(branch) == JavaParserLabeled.InterfaceDeclarationContext:
                kind = "Interface"
                break
            elif type(branch) == JavaParserLabeled.EnumDeclarationContext:
                kind = "Enum Class"
                break
            prefixes += branch.getText() + " "
        return prefixes, import_entity_listener.body, kind

    def get_parent_import(self, parent_file_name, file):
        parent_entity, _ = EntityModel.get_or_create(
            _kind=1,  # Java File
            _name=parent_file_name,
            _longname=file,
        )
        return parent_entity, file

    def get_kind_name(self, prefixes, kind):
        p_static = ""
        p_abstract = ""
        p_generic = ""
        p_type = "Type"
        p_visibility = "Default"
        p_member = "Member"

        if "static" in prefixes:
            p_static = "Static"

        if "generic" in prefixes:
            p_generic = "Generic"

        if "abstract" in prefixes:
            p_abstract = "Abstract"
        elif "final" in prefixes:
            p_abstract = "Final"

        if "private" in prefixes:
            p_visibility = "Private"
        elif "public" in prefixes:
            p_visibility = "Public"
        elif "protected" in prefixes:
            p_visibility = "Protected"

        if kind == "Interface":
            p_member = ""

        if kind == "Method":
            p_type = ""

        s = f"Java {p_static} {p_abstract} {p_generic} {kind} {p_type} {p_visibility} {p_member}"
        s = " ".join(s.split())
        return s

    def get_kind_name_opened(self, prefixes, kind):
        p_static = ""
        p_abstract = ""
        p_generic = ""
        p_type = "Type"
        p_visibility = "Default"
        p_member = "Member"

        if "static" in prefixes:
            p_static = "Static"

        if "generic" in prefixes:
            p_generic = "Generic"

        if "abstract" in prefixes:
            p_abstract = "Abstract"
        elif "final" in prefixes:
            p_abstract = "Final"

        if "private" in prefixes:
            p_visibility = "Private"
        elif "public" in prefixes:
            p_visibility = "Public"
        elif "protected" in prefixes:
            p_visibility = "Protected"

        if kind == "Interface":
            p_member = ""
            p_static = ""

        if kind == "Method":
            p_type = ""

        s = f"Java {p_static} {p_abstract} {p_generic} {kind} {p_type} {p_visibility} {p_member}"
        s = " ".join(s.split())
        return s

    def add_opened_entity(self, entity):
        entity_kind = self.get_kind_name_opened(entity["longname"], entity["kind"])
        imported_entity, _ = EntityModel.get_or_create(
            _kind=KindModel.get_or_none(_name=entity_kind).get_id(),
            # _parent=parent_entity.get_id(),
            _parent=None,
            _name=entity["name"],
            _longname=entity["longname"],
            _contents=entity["body"],
        )
        return imported_entity

    def add_references_opend(self, importing_ent, imported_ent, ref_dict):
        ref, _ = ReferenceModel.get_or_create(
            _kind=234,  # Java Open
            _file=importing_ent.get_id(),
            _line=ref_dict["line"],
            _column=ref_dict["column"],
            _ent=imported_ent.get_id(),
            _scope=importing_ent.get_id(),
        )
        inverse_ref, _ = ReferenceModel.get_or_create(
            _kind=235,  # Java OpenBy
            _file=importing_ent.get_id(),
            _line=ref_dict["line"],
            _column=ref_dict["column"],
            _ent=importing_ent.get_id(),
            _scope=imported_ent.get_id(),
        )

    def add_references_import(self, importing_ent, imported_ent, ref_dict):
        ref, _ = ReferenceModel.get_or_create(
            _kind=206,  # Java Import
            _file=importing_ent.get_id(),
            _line=ref_dict["line"],
            _column=ref_dict["column"],
            _ent=imported_ent.get_id(),
            _scope=importing_ent.get_id(),
        )
        inverse_ref, _ = ReferenceModel.get_or_create(
            _kind=207,  # Java Importby
            _file=importing_ent.get_id(),
            _line=ref_dict["line"],
            _column=ref_dict["column"],
            _ent=importing_ent.get_id(),
            _scope=imported_ent.get_id(),
        )

    def add_imported_entity(self, i, files, import_entity_listener):
        if i["is_built_in"]:
            imported_entity, _ = EntityModel.get_or_create(
                _kind=84,  # Java Unknown Class Type Member
                _parent=None,
                _name=i["imported_class_name"],
                _longname=i["imported_class_longname"],
            )
        else:
            parent_entity, parent_file_path = self.get_parent_import(
                i["imported_class_file_name"], files
            )
            imported_entity, _ = EntityModel.get_or_create(
                _kind=KindModel.get_or_none(_name="Java Import").get_id(),
                _parent=parent_entity.get_id(),
                _name=i["imported_class_name"],
                _longname=i["imported_class_longname"],
                _contents="",
            )
        return imported_entity

    def add_import_demand(self, ents, file_path):
        for i in ents:
            ent, _ = EntityModel.get_or_create(
                _kind=1,
                _parent="None",
                _name=i["name"],
                _longname=i["longname"],
                _contents=FileStream(file_path, encoding="utf-8"),
            )

            ReferenceModel.get_or_create(
                _kind=204,
                _file=file_path,
                _line=i["line"],
                _column=i["col"],
                _ent=ent.get_id(),
                _scope=file_path,
            )

    def add_references(self, importing_ent, imported_ent, cls_data: ClassTypeData):
        ref, _ = ReferenceModel.get_or_create(
            _kind=KindModel.get_or_none(_name="Java Extend Couple Implicit")._id,
            _file_id=importing_ent._id,
            _line=cls_data.line,
            _column=cls_data.column,
            _ent_id=imported_ent._id,
            _scope_id=importing_ent._id,
        )
        inverse_ref, _ = ReferenceModel.get_or_create(
            _kind=KindModel.get_or_none(_name="Java Extend Coupleby Implicit")._id,
            _file_id=importing_ent._id,
            _line=cls_data.line,
            _column=cls_data.column,
            _ent_id=importing_ent._id,
            _scope_id=imported_ent._id,
        )

    def add_imported_entity_factory(self, cls_data: ClassTypeData):
        parent_entity: EntityModel = self.get_parent(cls_data.file_path)
        kindModel = KindModel.get_or_none(
            _name=self.getNameEntity(cls_data.get_prefixes())
        )
        extend_implicit_entity = None
        if kindModel is not None:
            extend_implicit_entity, _ = EntityModel.get_or_create(
                _kind=kindModel._id,
                _parent=parent_entity._id,
                _name=cls_data.get_name(),
                _type=cls_data.get_type(),
                _longname=cls_data.get_long_name(),
                _contents=cls_data.get_contents(),
            )
        entity_kind_object = 84
        java_lang_entity, _ = EntityModel.get_or_create(
            _kind=entity_kind_object,
            _parent=None,
            _name="Object",
            _type=None,
            _longname=cls_data.parentClass,
            _contents="",
        )
        return extend_implicit_entity, java_lang_entity

    def addCreateRefs(self, ref_dicts, file_ent, file_address):

        for ref_dict in ref_dicts:
            try:
                scope = EntityModel.get_or_create(
                    _kind=self.findKindWithKeywords(
                        "Method", ref_dict["scopemodifiers"]
                    ),
                    _name=ref_dict["scopename"],
                    _type=ref_dict["scopereturntype"],
                    _parent=(
                        ref_dict["scope_parent"]
                        if ref_dict["scope_parent"] is not None
                        else file_ent
                    ),
                    _longname=ref_dict["scopelongname"],
                    _contents=["scopecontent"],
                )[0]

                ent = self.getCreatedClassEntity(
                    ref_dict["refent"],
                    ref_dict["potential_refent"],
                    file_address,
                    file_ent,
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
            except Exception as e:
                print("ERROR in project.py function addCreateRefs ")
                print("error message : ", e)

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
        self, class_longname, class_potential_longname, file_address, file_ent
    ):
        props = self.getClassProperties(class_potential_longname, file_address)
        if not props:
            return self.getClassEntity(class_longname, file_address, file_ent)
        else:
            return self.getClassEntity(class_potential_longname, file_address, file_ent)

    def getClassEntity(self, class_longname, file_address, file_ent):
        props = self.getClassProperties(class_longname, file_address)
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
        self, interface_longname, file_address, file_ent
    ):  # can't be of unknown kind!
        props = self.getInterfaceProperties(interface_longname, file_address)
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

    def getImplementEntity(self, longname, file_address, file_ent):
        ent = self.getInterfaceEntity(longname, file_address, file_ent)
        if not ent:
            ent = self.getClassEntity(longname, file_address, file_ent)
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

    def addoverridereference(self, classes, extendedfiles, file_ent):
        try:
            for tuples in extendedfiles:
                try:
                    main = tuples[0]
                    fromx = tuples[1]
                    methodsmain = classes[main]
                except Exception as e:
                    print("ERROR 0 in addoverridereference : ", e)
                for x in methodsmain:
                    try:
                        file = x["File"]
                        kindx = self.findKindWithKeywords(
                            x["scope_kind"], x["scope_modifiers"]
                        )
                        if kindx is None:
                            kindx = x["modifiersx"]
                        scope = EntityModel.get_or_create(
                            _kind=kindx,
                            _name=x["scope_name"],
                            _parent=(
                                x["scope_parent"]
                                if x["scope_parent"] is not None
                                else file_ent
                            ),
                            _longname=x["scope_longname"],
                            _contents=x["scope_contents"],
                            _type=x["Methodkind"],
                        )
                        methodname1 = x["MethodIs"]
                    except Exception as e:
                        print("ERROR 1 in addoverridereference : ", e)
                    if fromx in classes:
                        try:
                            mathodsfrom = classes[fromx]
                        except Exception as e:
                            print("ERROR 2 in addoverridereference : ", e)
                        for y in mathodsfrom:
                            try:
                                if y["MethodIs"] == methodname1:
                                    fe = file_ent
                                    kind = self.findKindWithKeywords(
                                        y["scope_kind"], y["scope_modifiers"]
                                    )
                                    if kind is None:
                                        kind = y["modifiersx"]
                                    ent = EntityModel.get_or_create(
                                        _kind=kind,
                                        _name=y["scope_name"],
                                        _parent=(
                                            y["scope_parent"]
                                            if y["scope_parent"] is not None
                                            else fe
                                        ),
                                        _longname=y["scope_longname"],
                                        _contents=y["scope_contents"],
                                        _type=y["Methodkind"],
                                    )

                                    override_ref = ReferenceModel.get_or_create(
                                        _kind=211,
                                        _file=file_ent,
                                        _line=x["line"],
                                        _column=x["col"],
                                        _ent=ent[0],
                                        _scope=scope[0],
                                    )
                                    overrideBy_ref = ReferenceModel.get_or_create(
                                        _kind=212,
                                        _file=fe,
                                        _line=y["line"],
                                        _column=y["col"],
                                        _ent=scope[0],
                                        _scope=ent[0],
                                    )
                            except Exception as e:
                                print("ERROR 3 in addoverridereference : ", e)
                    elif x["is_overrided"]:
                        overrideword = list(x.values())
                        classes = [
                            list(i[0].values())[0]
                            for i in [item for item in list(classes.values())]
                        ]
                        if overrideword[0] not in classes:

                            ent = EntityModel.get_or_create(
                                _kind=32,
                                _name=overrideword[1],
                                _parent=file_ent,
                                _longname=overrideword,
                                _contents="",
                            )
                            override_ref = ReferenceModel.get_or_create(
                                _kind=211,
                                _file=file_ent,
                                _line=x["line"],
                                _column=x["col"],
                                _ent=ent[0],
                                _scope=scope[0],
                            )
        except Exception as e:
            print("ERROR 6 in addoverridereference : ", e)

    def get_parent_entity(self, file_path):
        return EntityModel.get_or_none(_longname=file_path)

    def add_entity_package(self, package_name, file_path):
        file_entity = self.get_parent_entity(file_path)
        created_entity, _ = EntityModel.get_or_create(
            _kind_id=KindModel.get_or_none(_name="Java Package")._id,
            _parent_id=file_entity._id,
            _name=package_name["package_name"].split(".")[-1],
            _longname=package_name["package_name"],
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

    def define_parent(self, entity_type, entity_values, file_path, package_name):
        if entity_type == "class" or entity_type == "interface":
            return EntityModel.get_or_none(_longname=file_path)
        else:
            return EntityModel.get_or_none(
                _longname=f"{package_name}.{entity_values['parent_name']}"
            )

    def extract_is_constructor(self, prefixes):
        pattern_visibility = " Default"
        if "private" in prefixes:
            pattern_visibility = " Private"
        elif "public" in prefixes:
            pattern_visibility = " Public"
        elif "protected" in prefixes:
            pattern_visibility = " Protected"
        return f"Java Method Constructor Member{pattern_visibility}"

    def config_entity_type(self, type_entity):
        if type_entity == "class":
            return "Class Type"
        if type_entity == "interface":
            return "Interface Type"
        if type_entity == "variable":
            return "Variable"
        if type_entity == "method":
            return "Method"

    def extract_all_kind(self, prefixes, type_entity, is_constructor) -> str:
        if is_constructor:
            return self.extract_is_constructor(prefixes)
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
            self.config_entity_type(type_entity),
            pattern_visibility,
        )
        if type_entity == "interface":
            result_str = result_str.replace("Member", "").strip()
        return result_str

    def add_use_module_reference(
        self,
        use_module: list = None,
        unknown_module: list = None,
        unresolved_module: list = None,
        file_address: str = "",
    ) -> None:
        file_entity = self.get_parent_entity(file_address)
        for item in unknown_module:
            created_entity, _ = EntityModel.get_or_create(
                _kind_id=KindModel.get_or_none(_name="Java Module")._id,
                _parent_id=file_entity._id,
                _name=item["name"].split(".")[-1],
                _longname=item["package"],
                _contents="",
            )

            ReferenceModel.get_or_create(
                _kind_id=KindModel.get_or_none(_name="Java Unknown Module")._id,
                _file_id=file_entity._id,
                _line=item["line"],
                _column=item["col"],
                _ent_id=item["ent"],
                _scope_id=item["scope"],
            )
        for item in unresolved_module:
            created_entity, _ = EntityModel.get_or_create(
                _kind_id=KindModel.get_or_none(_name="Java Module")._id,
                _parent_id=file_entity._id,
                _name=item["name"].split(".")[-1],
                _longname=item["package"],
                _contents="",
            )
            ReferenceModel.get_or_create(
                _kind_id=KindModel.get_or_none(_name="Java Unresolved Module")._id,
                _file_id=file_entity._id,
                _line=item["line"],
                _column=item["col"],
                _ent_id=item["ent"],
                _scope_id=item["scope"],
            )
        for item in use_module:
            created_entity, _ = EntityModel.get_or_create(
                _kind_id=KindModel.get_or_none(_name="Java Module")._id,
                _parent_id=file_entity._id,
                _name=item["name"].split(".")[-1],
                _longname=item["package"],
                _contents="",
            )
            ReferenceModel.get_or_create(
                _kind_id=KindModel.get_or_none(_name="Java ModuleUse")._id,
                _file_id=file_entity._id,
                _line=item["line"],
                _column=item["col"],
                _ent_id=item["ent"],
                _scope_id=item["scope"],
            )
            ReferenceModel.get_or_create(
                _kind_id=KindModel.get_or_none(_name="Java ModuleUseby")._id,
                _file_id=file_entity._id,
                _line=item["line"],
                _column=item["col"],
                _ent_id=item["scope"],
                _scope_id=item["ent"],
            )

    def check_and_create_record(self, name, kind):
        existing_record = EntityModel.select().where(EntityModel._name == name).first()
        return not (existing_record and existing_record._kind == kind)

    def add_defined_entities(self, entities, entity_type, package_name, file_path):
        for entity_key, entity_values in entities.items():
            is_constructor = False
            if entity_type == "method" and entity_values["type"] == "":
                is_constructor = True
            kind_str = (
                entity_values["kind_name"]
                if entity_type == "local variable" or entity_type == "parameter"
                else self.extract_all_kind(
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
                f"{package_name}.{entity_values['parent_name']}.{model_name}"
                if entity_values["parent_name"] != ""
                else f"{package_name}.{model_name}"
            )
            model_contents = entity_values["contents"]
            model_parent = self.define_parent(
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

    def getThrowEntity(self, longname, file_address, file_ent):
        ent = self.getInterfaceEntity(longname, file_address, file_ent)
        if not ent:
            ent = self.getClassEntity(longname, file_address, file_ent)
        return ent

    def addThrows_TrowsByRefs(self, ref_dicts, file_ent, file_address, id1, id2, Throw):
        for ref_dict in ref_dicts:

            scope = EntityModel.get_or_create(
                _kind=self.findKindWithKeywords("Method", ref_dict["scopemodifiers"]),
                _name=ref_dict["scopename"],
                _parent=(
                    ref_dict["scope_parent"]
                    if ref_dict["scope_parent"] is not None
                    else file_ent
                ),
                _longname=ref_dict["scopelongname"],
                _contents=ref_dict["scopecontent"],
            )[0]

            if not Throw:
                if ref_dict["refent"] is None:
                    ent = self.getUnnamedPackageEntity(file_ent)
                else:
                    ent = self.getPackageEntity(
                        file_ent, ref_dict["refent"], ref_dict["refent"]
                    )
            else:
                ent = self.getThrowEntity(ref_dict["refent"], file_address, file_ent)

            implement_ref = ReferenceModel.get_or_create(
                _kind=id1,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _ent=ent,
                _scope=scope,
            )
            implementBy_ref = ReferenceModel.get_or_create(
                _kind=id2,
                _file=file_ent,
                _line=ref_dict["line"],
                _column=ref_dict["col"],
                _ent=scope,
                _scope=ent,
            )

    def add_couple_and_couple_by_refs(self, classes, couples):
        keykind = ''
        for c in couples:
            file_ent = self.getFileEntity(c['File'])
            scope = EntityModel.get_or_create(_kind=self.findKindWithKeywords(c["scope_kind"], c["scope_modifiers"]),
                                              _name=c["scope_name"],
                                              _parent=c["scope_parent"] if c["scope_parent"] is not None else file_ent,
                                              _longname=c["scope_longname"],
                                              _contents=c["scope_contents"])
            if 'type_ent_longname' in c:
                keylist = c['type_ent_longname']
                if (len(keylist) != 0):
                    for key in keylist:
                        if key in classes:
                            c1 = classes[key]
                            file_ent2 = self.getFileEntity(c1['File'])
                            keykind = self.findKindWithKeywords(c1["scope_kind"], c1["scope_modifiers"])
                            ent = EntityModel.get_or_create(
                                _kind=self.findKindWithKeywords(c1["scope_kind"], c1["scope_modifiers"]),
                                _name=c1["scope_name"],
                                _parent=c1["scope_parent"] if c1["scope_parent"] is not None else file_ent2,
                                _longname=c1["scope_longname"],
                                _contents=c1["scope_contents"])
                            CoupleBy_ref = ReferenceModel.get_or_create(_kind=180, _file=file_ent2, _line=c["line"],
                                                                        _column=c["col"], _ent=scope[0], _scope=ent[0])

                        else:
                            kw = key.split('.')
                            keykind = "Unknown Class"
                            ent = EntityModel.get_or_create(_kind="Unknown Class", _name=kw[-1],
                                                            _parent=file_ent,
                                                            _longname=key,
                                                            )
                        Couple_ref = ReferenceModel.get_or_create(_kind=179, _file=file_ent, _line=c["line"],
                                                                  _column=c["col"], _ent=ent[0], _scope=scope[0])

    # for c in couples:
        #     ent = self.getImplementEntity(
        #         c["type_ent_longname"], file_address, file_ent
        #     )
        #     scope = EntityModel.get_or_create(
        #         _kind=self.findKindWithKeywords(c["scope_kind"], c["scope_modifiers"]),
        #         _name=c["scope_name"],
        #         _parent=(
        #             c["scope_parent"] if c["scope_parent"] is not None else file_ent
        #         ),
        #         _longname=c["scope_longname"],
        #         _contents=c["scope_contents"],
        #     )[0]
        #     Couple_ref = ReferenceModel.get_or_create(
        #         _kind=180,
        #         _file=file_ent,
        #         _line=c["line"],
        #         _column=c["col"],
        #         _ent=ent,
        #         _scope=scope,
        #     )
        #     CoupleBy_ref = ReferenceModel.get_or_create(
        #         _kind=181,
        #         _file=file_ent,
        #         _line=c["line"],
        #         _column=c["col"],
        #         _ent=scope,
        #         _scope=ent,
        #     )

    def addcouplereference(self, classes, couples, file_ent):
        keykind = ""
        for c in couples:
            try:
                scope = EntityModel.get_or_create(
                    _kind=self.findKindWithKeywords(
                        c["scope_kind"], c["scope_modifiers"]
                    ),
                    _name=c["scope_name"],
                    _parent=(
                        c["scope_parent"] if c["scope_parent"] is not None else file_ent
                    ),
                    _longname=c["scope_longname"],
                    _contents=c["scope_contents"],
                )
                if "type_ent_longname" in c:
                    keylist = c["type_ent_longname"]
                    if len(keylist) != 0:
                        for key in keylist:
                            if key in classes:
                                c1 = classes[key]
                                file_ent2 = file_ent
                                keykind = self.findKindWithKeywords(
                                    c1["scope_kind"], c1["scope_modifiers"]
                                )
                                ent = EntityModel.get_or_create(
                                    _kind=self.findKindWithKeywords(
                                        c1["scope_kind"], c1["scope_modifiers"]
                                    ),
                                    _name=c1["scope_name"],
                                    _parent=(
                                        c1["scope_parent"]
                                        if c1["scope_parent"] is not None
                                        else file_ent2
                                    ),
                                    _longname=c1["scope_longname"],
                                    _contents=c1["scope_contents"],
                                )
                                CoupleBy_ref = ReferenceModel.get_or_create(
                                    _kind=180,
                                    _file=file_ent2,
                                    _line=c["line"],
                                    _column=c["col"],
                                    _ent=scope[0],
                                    _scope=ent[0],
                                )

                            else:
                                kw = key.split(".")
                                keykind = 84
                                ent = EntityModel.get_or_create(
                                    _kind=keykind,
                                    _name=kw[-1],
                                    _parent=file_ent,
                                    _longname=key,
                                )
                            Couple_ref = ReferenceModel.get_or_create(
                                _kind=179,
                                _file=file_ent,
                                _line=c["line"],
                                _column=c["col"],
                                _ent=ent[0],
                                _scope=scope[0],
                            )

            except Exception as e:
                print(e)

