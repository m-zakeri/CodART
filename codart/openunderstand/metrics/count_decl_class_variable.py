from openunderstand.oudb.models import EntityModel, KindModel, ReferenceModel


def declare_class_variables(ent_model=None) -> object:
    kinds = KindModel.select().where(KindModel._name.contains("Variable"))
    ents = EntityModel.select().where(EntityModel._kind.in_(kinds))
    return ents.select().where(EntityModel._name.contains(ent_model.name())).count()
