import utils_listener
import utils

def pullup_field(source_filenames: list,
                 package_name: str,
                 superclass_name: str,
                 field_name: str,
                 filename_mapping = lambda x: (x[:-5] if x.endswith(".java") else x) + ".re.java") -> bool:

    program = utils.get_program(source_filenames)
    if package_name not in program.packages \
            or superclass_name not in program.packages[package_name].classes \
            or field_name in program.packages[package_name].classes[superclass_name].fields:
        return False

    superclass: utils_listener.Class = program.packages[package_name].classes[superclass_name]
    superclass_body_start = utils_listener.TokensInfo(superclass.parser_context.classBody())
    superclass_body_start.stop = superclass_body_start.start # Start and stop both point to the '{'

    fields_to_remove = []
    for pn in program.packages:
        p: utils_listener.Package = program.packages[pn]
        for cn in p.classes:
            c: utils_listener.Class = p.classes[cn]
            if superclass_name == c.superclass_name and field_name in c.fields:
                fields_to_remove.append(c.fields[field_name])

    if len(fields_to_remove) == 0:
        return False

    is_public = False
    datatype = fields_to_remove[0].datatype
    for field in fields_to_remove:
        field: utils_listener.Field = field
        if field.datatype != datatype:
            return False
        is_public = is_public or "public" in field.modifiers

    rewriter = utils.Rewriter(program, filename_mapping)
    rewriter.insert_after(superclass_body_start, "\n\t" + ("public " if is_public else "protected ") + datatype + " " + field_name + ";")
    for field in fields_to_remove:
        rewriter.replace(field.get_tokens_info(), "")
    rewriter.apply()
    return True

if __name__ == "__main__":
    # test
    if pullup_field(["tests/pullup_field_test1.java", "tests/pullup_field_test2.java"], "pullup_field_test", "A", "a"):
        print("Success!")
    else:
        print("Cannot refactor.")
