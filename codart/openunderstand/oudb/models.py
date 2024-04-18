from peewee import *


class KindModel(Model):
    """
    This table will fill automatically.
    """

    _id = AutoField()
    _inv = ForeignKeyField("self", null=True)
    _name = CharField(max_length=256, unique=True)

    is_ent_kind = BooleanField(default=True)

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        return str(self._name)

    @property
    def is_ref_kind(self):
        return not self.is_ent_kind


class EntityModel(Model):
    _id = AutoField()
    _kind = ForeignKeyField(KindModel, backref="entities")
    _parent = ForeignKeyField("self", backref="children", null=True)
    _name = CharField(max_length=512)
    _longname = CharField(max_length=512)
    _value = CharField(max_length=512, null=True)
    _type = CharField(max_length=512, null=True)
    _contents = TextField(null=True)

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        return str(self._longname)

    # TODO: Implement other methods


class ReferenceModel(Model):
    _id = AutoField()
    _kind = ForeignKeyField(KindModel, backref="references")
    _file = ForeignKeyField(EntityModel)
    _line = IntegerField()
    _column = IntegerField()
    _ent = ForeignKeyField(EntityModel, backref="refs")
    _scope = ForeignKeyField(EntityModel, backref="inv_refs")

    def __str__(self):
        return f"{self._kind} {self._ent} {self._file}({self._line}, {self._column})"


class ProjectModel(Model):
    name = CharField(max_length=128)
    language = CharField(max_length=128, default="Java")
    root = CharField(max_length=1024)
    db_path = CharField(max_length=1024, unique=True)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)
