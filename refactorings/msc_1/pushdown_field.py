import utils_listener
import utils

def pushdown_field(source_filenames: list,
                   package_name: str,
                   superclass_name: str,
                   field_name: str,
                   filename_mapping = lambda x: (x[:-5] if x.endswith(".java") else x) + ".re.java") -> bool:

    program = utils.get_program(source_filenames)
    if package_name not in program.packages \
            or superclass_name not in program.packages[package_name].classes \
            or field_name not in program.packages[package_name].classes[superclass_name].fields:
        return False

    for pn in program.packages:
        p: utils_listener.Package = program.packages[pn]
        for cn in p.classes:
            c: utils_listener.Class = p.classes[cn]
            if superclass_name == c.superclass_name and field_name in c.fields:
                pass
