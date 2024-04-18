from openunderstand.oudb.models import EntityModel, KindModel, ReferenceModel


def declare_file(ent_model=None):
    kinds = KindModel.select().where(KindModel._name.contains("Java Package"))
    ents = EntityModel.select().where(EntityModel._kind.in_(kinds))
    return (
        ents.select()
        .where(EntityModel._parent._name.contains(ent_model.name()))
        .count()
    )
