import utils_listener_fast
from refactorings import utils


def pullup_field(source_filenames: list,
                 package_name: str,
                 class_name: str,
                 field_name: str,
                 filename_mapping = lambda x: (x[:-5] if x.endswith(".java") else x) + ".re.java") -> bool:

    program = utils.get_program(source_filenames, print_status=True)

    if package_name not in program.packages \
            or class_name not in program.packages[package_name].classes \
            or field_name not in program.packages[package_name].classes[class_name].fields:
        return False

    _class: utils_listener_fast.Class = program.packages[package_name].classes[class_name]
    if _class.superclass_name is None:
        return False

    superclass_name = _class.superclass_name

    superclass: utils_listener_fast.Class = program.packages[package_name].classes[superclass_name]
    superclass_body_start = utils_listener_fast.TokensInfo(superclass.parser_context.classBody())
    superclass_body_start.stop = superclass_body_start.start # Start and stop both point to the '{'

    if field_name in superclass.fields:
        return False

    datatype = _class.fields[field_name].datatype

    fields_to_remove = []
    for pn in program.packages:
        p: utils_listener_fast.Package = program.packages[pn]
        for cn in p.classes:
            c: utils_listener_fast.Class = p.classes[cn]
            if ((c.superclass_name == superclass_name and c.file_info.has_imported_class(package_name, superclass_name)) \
                    or (package_name is not None and c.superclass_name == package_name + '.' + superclass_name)) \
                    and field_name in c.fields \
                    and c.fields[field_name].datatype == datatype:
                fields_to_remove.append(c.fields[field_name])

    if len(fields_to_remove) == 0:
        return False

    is_public = False
    is_protected = True
    for field in fields_to_remove:
        field: utils_listener_fast.Field = field
        is_public = is_public or "public" in field.modifiers
        is_protected = is_protected and ("protected" in field.modifiers or "private" in field.modifiers)

    rewriter = utils.Rewriter(program, filename_mapping)

    rewriter.insert_after(superclass_body_start, "\n    " + ("public " if is_public else ("protected " if is_protected else "")) + datatype + " " + field_name + ";")

    for field in fields_to_remove:
        if len(field.neighbor_names) == 0:
            rewriter.replace(field.get_tokens_info(), "")
            # Have to remove the modifiers too, because of the new grammar.
            for mod_ctx in field.modifiers_parser_contexts:
                rewriter.replace(utils_listener_fast.TokensInfo(mod_ctx), "")
        else:
            i = field.index_in_variable_declarators
            var_ctxs = field.all_variable_declarator_contexts
            if i == 0:
                to_remove = utils_listener_fast.TokensInfo(var_ctxs[i])
                to_remove.stop = utils_listener_fast.TokensInfo(var_ctxs[i + 1]).start - 1 # Include the ',' after it
                rewriter.replace(to_remove, "")
            else:
                to_remove = utils_listener_fast.TokensInfo(var_ctxs[i])
                to_remove.start = utils_listener_fast.TokensInfo(var_ctxs[i - 1]).stop + 1 # Include the ',' before it
                rewriter.replace(to_remove, "")

        # Add initializer to class constructor if initializer exists in field declaration
        if field.initializer is not None:
            _class: utils_listener_fast.Class = program.packages[field.package_name].classes[field.class_name]
            initializer_statement = (field.name
                                    + " = "
                                    + ("new " + field.datatype + " " if field.initializer.startswith('{') else "")
                                    + field.initializer
                                    + ";")
            has_contructor = False
            for class_body_decl in _class.parser_context.classBody().getChildren():
                if class_body_decl.getText() in ['{', '}']:
                    continue
                member_decl = class_body_decl.memberDeclaration()
                if member_decl is not None:
                    constructor = member_decl.constructorDeclaration()
                    if constructor is not None:
                        body = constructor.constructorBody # Start token = '{'
                        body_start = utils_listener_fast.TokensInfo(body)
                        body_start.stop = body_start.start # Start and stop both point to the '{'
                        rewriter.insert_after(body_start, "\n        " + initializer_statement)
                        has_contructor = True
            if not has_contructor:
                body = _class.parser_context.classBody()
                body_start = utils_listener_fast.TokensInfo(body)
                body_start.stop = body_start.start # Start and stop both point to the '{'
                rewriter.insert_after(body_start,
                    "\n    " + _class.name + "() { " + initializer_statement + " }"
                )

    rewriter.apply()
    return True

def test():
    print("Testing pullup_field...")
    filenames = [
        "tests/pullup_field/test1.java",
        "tests/pullup_field/test2.java",
        "tests/pullup_field/test3.java",
        "tests/pullup_field/test4.java"
    ]

    if pullup_field(filenames, "pullup_field_test1", "B", "a"):
        print("Success!")
    else:
        print("Cannot refactor.")

def test_ant():
    """
    target_files = [
        "tests/apache-ant/main/org/apache/tools/ant/types/ArchiveFileSet.java",
        "tests/apache-ant/main/org/apache/tools/ant/types/TarFileSet.java",
        "tests/apache-ant/main/org/apache/tools/ant/types/ZipFileSet.java"
    ]
    """
    ant_dir = "tests/apache-ant-1-7-0"
    print("Success!" if pullup_field(
        utils.get_filenames_in_dir(ant_dir),
        "org.apache.tools.ant.types",
        "TarFileSet",
        "userName",
        lambda x: "tests/pullup_field_ant/" + x[len(ant_dir):]
    ) else "Cannot refactor.")

if __name__ == "__main__":
    test()
