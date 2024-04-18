from openunderstand.oudb.models import EntityModel, KindModel, ReferenceModel


def declare_method_count(ent_model=None):
    kinds = KindModel.select().where(
        KindModel._name.contains("Static") & KindModel._name.contains("Method")
    )
    ents = EntityModel.select().where(EntityModel._kind.in_(kinds))
    return (
        ents.select()
        .where(EntityModel._parent._name.contains(ent_model.name()))
        .count()
    )
