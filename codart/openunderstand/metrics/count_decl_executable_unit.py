from openunderstand.oudb.models import EntityModel, KindModel, ReferenceModel


def reach_file(ent_model):
    tmp = ent_model
    while "Java File" not in tmp._kind._name:
        tmp = tmp._parent
    return tmp._longname


def declare_executable_unit(ent_model=None):
    kinds = KindModel.select().where(KindModel._name.contains("Method"))
    ents = EntityModel.select().where(EntityModel._kind.in_(kinds))
    file_name = reach_file(ent_model)
    return ents.select().where(EntityModel._name.contains(file_name)).count()
