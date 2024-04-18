import peewee
import os
import sys
import unittest

from openunderstand.oudb.models import KindModel, EntityModel, ReferenceModel
from openunderstand.oudb.utils import get_entity_object_from_understand
import pkg_resources


def append_java_ent_kinds(path_dir: str = ""):
    current_directory = os.path.abspath(os.path.dirname(__file__))
    path_dir = os.path.join(current_directory, "java_ent_kinds.txt")
    with open(path_dir, "r") as f:
        for line in f.readlines():
            if line.startswith("Java"):
                query = line.strip()
                kind, _ = KindModel.get_or_create(_name=query)
                print(f"Created ({_}): {kind}")


def append_java_ref_kind(kind: str, inverse: str, ref: str) -> int:
    ref_kind, _ = KindModel.get_or_create(_name=ref, is_ent_kind=False)
    inv = ref.replace(kind, inverse)
    inv_kind, _ = KindModel.get_or_create(_name=inv, is_ent_kind=False, _inv=ref_kind)
    ref_kind.inverse = inv_kind
    return ref_kind.save()


def append_java_ref_kinds(path_dir: str = ""):
    kind, inv_kind = "", ""
    current_directory = os.path.abspath(os.path.dirname(__file__))
    path_dir = os.path.join(current_directory, "java_ref_kinds.txt")
    with open(path_dir, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith("Java"):
                try:
                    if append_java_ref_kind(kind, inv_kind, line):
                        print(f"Created: {line}")
                        continue
                    else:
                        raise ConnectionError(
                            "Database disconnected, please try again!"
                        )
                except peewee.IntegrityError:
                    print(f"KindModel exists: {line}")
            else:
                if line:
                    kind, inv_kind = line.split()
                    inv_kind = inv_kind[1:-1]


def append_entities_with_understand(udb_path: str):
    try:
        from oudb import api as und
    except ImportError:
        print("Understand Python API is not installed correctly.")

    db = und.open(udb_path)
    for ent in db.ents():
        if ent.language() == "Java":
            # Create parents first
            parent_obj = None
            parents = []
            parent = ent.parent()
            while parent is not None:
                parents.append(parent)
                parent = parent.parent()
            parents.reverse()
            for index, parent in enumerate(parents):
                kind, _ = KindModel.get_or_create(_name=parent.kind().longname())
                parent_obj, _ = EntityModel.get_or_create(
                    _kind=kind,
                    _parent=parent_obj,
                    _name=parent.name(),
                    _longname=parent.longname(),
                    _value=parent.value(),
                    _type=parent.type(),
                    _contents=parent.contents(),
                )

            # Create entity it-self!
            kind, _ = KindModel.get_or_create(_name=ent.kind().longname())
            ent, _ = EntityModel.get_or_create(
                _kind=kind,
                _parent=parent_obj,
                _name=ent.name(),
                _longname=ent.longname(),
                _value=ent.value(),
                _type=ent.type(),
                _contents=ent.contents(),
            )
            print(ent)


def append_references_with_understand(udb_path: str):
    # TODO: Implement this method!
    try:
        from openunderstand import ounderstand as und
    except ImportError:
        print("Understand Python API is not installed correctly.")

    db = und.open(udb_path)
    for ent in db.ents():
        for ref in ent.refs():
            ent = get_entity_object_from_understand(ref.ent())
            scope = get_entity_object_from_understand(ref.scope())
            file = get_entity_object_from_understand(ref.file())
            assert ent is not None
            assert scope is not None
            assert file is not None
            kind, _ = KindModel.get_or_create(_name=ref.kind().longname())
            ref, has_created = ReferenceModel.get_or_create(
                _kind=kind,
                _file=file,
                _line=ref.line(),
                _column=ref.column(),
                _ent=ent,
                _scope=scope,
            )
            print(f"Reference created [{has_created}]: {ref}")
        print("===============")


class TestFill(unittest.TestCase):
    def setUp(self) -> None:
        self.ent_kind = KindModel.get(_name="Java Method Constructor Member Default")
        self.ref_kind = KindModel.get(_name="Java Open")

    def test_valid_inverse(self):
        inv = self.ref_kind.inv()
        self.assertEqual(inv._name, "Java Openby")
        self.assertTrue(inv.is_ref_kind)
        self.assertEqual(inv.inv(), self.ref_kind)

    def test_invalid_inverse(self):
        inv = self.ent_kind.inverse
        self.assertIsNone(inv)
        self.assertRaises(peewee.OperationalError, lambda: self.ent_kind.inv())


def fill(udb_path: str = ""):

    # udb_path = "D:\Dev\JavaSample\JavaSample1.udb"
    append_java_ent_kinds()
    append_java_ref_kinds()
    # print("=" * 50)
    # append_entities_with_understand(udb_path)
    # append_references_with_understand(udb_path)
