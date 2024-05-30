"""


"""

import os
from pathlib import Path

from antlr4 import *

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener

from ..oudb.models import *
from ..oudb.api import open as db_open, create_db, Kind
from ..oudb.fill import main


class ClassEntityListener(JavaParserLabeledListener):
    def __init__(self):
        self.class_body = None

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        # print("inside class declaration", ctx.getText())
        self.class_body = ctx.getText()


class ImportListener(JavaParserLabeledListener):
    def __init__(self):
        self.names = []
        self.longnames = []
        self.is_unknown_class = []
        self.parents = []
        self.line = 0
        self.col = 0

    def enterImportDeclaration(self, ctx: JavaParserLabeled.CompilationUnitContext):
        longname = ctx.qualifiedName().getText()
        self.longnames.append(longname)
        # print("longname", longname)
        name = longname.split(".")[-1]
        # print("name", name)
        self.names.append(name)

        if longname.split(".")[0] == "java":
            self.is_unknown_class.append(True)
            parent = None
        else:
            self.is_unknown_class.append(False)
            parent = name + ".java"

        self.parents.append(parent)
        # print("parent", parent)

        self.line = ctx.children[0].symbol.line
        self.col = ctx.children[0].symbol.column


def create_Entity(name, longname, parent, contents, kind, value, entity_type):
    obj, has_created = EntityModel.get_or_create(
        _kind=kind,
        _parent=parent,
        _name=name,
        _longname=longname,
        _value=value,
        _type=entity_type,
        _contents=contents,
    )
    return obj


def create_Ref(kind, file, line, column, ent, scope):
    obj, has_created = ReferenceModel.get_or_create(
        _kind=kind, _file=file, _line=line, _column=column, _ent=ent, _scope=scope
    )
    return obj


def get_class_body(path):
    file = FileStream(path)
    lexer = JavaLexer(file)
    tokens = CommonTokenStream(lexer)

    parser = JavaParserLabeled(tokens)

    tree = parser.compilationUnit()

    listener = ClassEntityListener()

    walker = ParseTreeWalker()
    walker.walk(listener=listener, t=tree)
    return listener.class_body


def readFile():
    listOfFiles = list()
    filename = []
    for dirpath, dirnames, filenames in os.walk(
        r"E:\uni\compiler\OpenUnderstand\benchmark\calculator_app"
    ):
        for file in filenames:
            if ".java" in str(file):
                filename.append(file)
                listOfFiles.append(os.path.join(dirpath, file))

    db = db_open(r"E:\uni\compiler\OpenUnderstand\database.oudb")

    for path, name in zip(listOfFiles, filename):
        # lexer and parser for the current file
        file = FileStream(path)
        lexer = JavaLexer(file)
        tokens = CommonTokenStream(lexer)

        parser = JavaParserLabeled(tokens)

        tree = parser.compilationUnit()

        listener = ImportListener()

        walker = ParseTreeWalker()
        walker.walk(listener=listener, t=tree)

        file_kind = KindModel.get_or_none(_name="Java File")._id

        # break
        # find enitity
        entities = []
        for ent_name, longname, is_unk, parent in zip(
            listener.names,
            listener.longnames,
            listener.is_unknown_class,
            listener.parents,
        ):
            if is_unk:
                ent_kind = KindModel.get_or_none(
                    _name="Java Unknown Class Type Member"
                )._id
                contents = ""
                obj = create_Entity(
                    ent_name, longname, None, contents, ent_kind, None, None
                )

            else:
                ent_kind = KindModel.get_or_none(
                    _name="Java Class Type Public Member"
                )._id
                idx = filename.index(parent)
                new_path = listOfFiles[idx]
                contents = get_class_body(new_path)

                # create parent of entity of ref
                parent_contents = FileStream(new_path)
                parent_obj = create_Entity(
                    parent, longname, None, parent_contents, file_kind, None, None
                )
                obj = create_Entity(
                    ent_name, longname, parent_obj._id, contents, ent_kind, None, None
                )

            entities.append(obj._id)

        # find scope
        obj2 = create_Entity(name, path, None, file, file_kind, None, None)

        # make reference
        ref_kind = KindModel.get_or_none(_name="Java Import")._id
        for ent in entities:
            obj3 = create_Ref(
                ref_kind, name, listener.line, listener.col, ent, obj2._id
            )


readFile()
