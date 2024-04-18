from openunderstand.oudb.models import EntityModel, KindModel


def get_entity_object_from_understand(understand_ent):
    kind = KindModel.get_or_none(_name=understand_ent.kind().longname())
    ent = EntityModel.get_or_none(
        _name=understand_ent.name(), _longname=understand_ent.longname(), _kind=kind
    )
    return ent
