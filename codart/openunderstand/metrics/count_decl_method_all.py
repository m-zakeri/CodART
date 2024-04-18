from openunderstand.oudb.models import EntityModel, KindModel, ReferenceModel


def count_decl_method_all(ent_model=None) -> int:
    number_of_methods = 0
    class_methods = {}
    files = []
    extends_class_names = {}
    kinds = KindModel.select().where(KindModel._name.contains("Extend"))
    refs = ReferenceModel.select().where(ReferenceModel._kind_id.in_(kinds))
    for e in EntityModel.select().where(EntityModel._id.in_(refs)):
        extends_class_names.update({e._longname: e._name})
    if ent_model.kind() == 1:
        files.append(ent_model._longname)
    if "Class" in ent_model.kind().name():
        class_methods[ent_model._name] = 0
    for ent_model in EntityModel.select():
        try:
            if "Method" in ent_model._kind._name:
                exists = class_methods.get(ent_model._parent._name, -1)
                if exists == -1:
                    class_methods[ent_model._parent._name] = 1
                else:
                    class_methods[ent_model._parent._name] += 1
        except Exception as e:
            print(
                f"error to calculate count_decl_method_all metric in {ent_model._kind._name} kind"
            )

    for cm in class_methods:
        visited = []
        temp = cm
        while extends_class_names.__contains__(temp):
            t = extends_class_names[temp]
            if not visited.__contains__(t):
                visited.append(t)
                temp = "-9999"

        for v in visited:
            number_of_methods += class_methods[v]
    return number_of_methods
