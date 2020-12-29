import utils_listener
import utils

def extract_interface(source_filenames: list,
                      package_name: str,
                      class_names: list,
                      method_names: list,
                      interface_name: str,
                      interface_filename: str,
                      filename_mapping = lambda x: (x[:-5] if x.endswith(".java") else x) + ".re.java") -> bool:

    program = utils.get_program(source_filenames)

    if package_name not in program.packages \
            or any(
                class_name not in program.packages[package_name].classes
                    for class_name in class_names
            ) \
            or any(
                method_name not in program.packages[package_name].classes[class_name].methods
                    for class_name in class_names for method_name in method_names
            ):
        return False

    method_returntypes = {}
    method_parameters = {}

    rewriter = utils.Rewriter(program, filename_mapping)

    for class_name in class_names:
        c: utils_listener.Class = program.packages[package_name].classes[class_name]
        # Add implements to the class
        has_superinterface = False
        if c.parser_context.superinterfaces() is not None:
            t = utils_listener.TokensInfo(c.parser_context.superinterfaces())
            has_superinterface = True
        elif c.parser_context.superclass() is not None:
            t = utils_listener.TokensInfo(c.parser_context.superclass())
        else:
            t = utils_listener.TokensInfo(c.parser_context.identifier())
        rewriter.insert_after(t, (", " if has_superinterface else " implements ") + interface_name)
        for method_name in method_names:
            m: utils_listener.Method = c.methods[method_name]
            # Check if the return types / parameter types are the same
            # Or add to dictionary
            if method_name in method_returntypes:
                if method_returntypes[method_name] != m.returntype:
                    return False
                if len(method_parameters[method_name]) != len(m.parameters):
                    return False
                for i in range(len(m.parameters)):
                    if method_parameters[method_name][i][0] != m.parameters[i][0]:
                        return False
            else:
                method_returntypes[method_name] = m.returntype
                method_parameters[method_name] = m.parameters
            # Manage method modifiers
            rewriter.insert_before_start(
                m.get_tokens_info(),
                ("" if "@Override" in m.modifiers else "@Override\n    ")
                + ("" if "public" in m.modifiers else "public ")
            )
            for i in range(len(m.modifiers)):
                mm = m.modifiers[i]
                if mm == "private" or mm == "protected":
                    t = utils_listener.TokensInfo(m.parser_context.methodModifier(i))
                    rewriter.replace(t, "")

    # Change variable types to the interface if only interface methods are used.
    for package_name in program.packages:
        p: utils_listener.Package = program.packages[package_name]
        for class_name in p.classes:
            c: utils_listener.Class = p.classes[class_name]
            fields_of_interest = {}
            for fn in c.fields:
                f: utils_listener.Field = c.fields[fn]
                d = False
                for cn in class_names:
                    if (f.datatype == cn and f.file_info.has_imported_class(package_name, cn)) \
                            or (package_name is not None and f.datatype == package_name + '.' + cn):
                        d = True
                        break
                if d and "private" in f.modifiers:
                    fields_of_interest[f.name] = f
            for method_name in c.methods:
                m: utils_listener.Method = c.methods[method_name]
                vars_of_interest = {}
                for item in m.body_local_vars_and_expr_names:
                    if isinstance(item, utils_listener.LocalVariable):
                        for cn in class_names:
                            if (item.datatype == cn and c.file_info.has_imported_class(package_name, cn)) \
                                    or (package_name is not None and item.datatype == package_name + '.' + cn):
                                vars_of_interest[item.identifier] = item
                                break
                    if isinstance(item, utils_listener.MethodInvocation):
                        if len(item.dot_separated_identifiers) == 2 or \
                                (len(item.dot_separated_identifiers) == 3 and item.dot_separated_identifiers[0] == "this"):
                            if item.dot_separated_identifiers[-2] in vars_of_interest:
                                if item.dot_separated_identifiers[-1] not in method_names:
                                    vars_of_interest.pop(item.dot_separated_identifiers[-2])
                            elif item.dot_separated_identifiers[-2] in fields_of_interest \
                                    and item.dot_separated_identifiers[-1] not in method_names:
                                fields_of_interest.pop(item.dot_separated_identifiers[-2])
                for var_name in vars_of_interest:
                    var = vars_of_interest[var_name]
                    if m.file_info.has_imported_package(package_name):
                        rewriter.replace(utils_listener.TokensInfo(var.parser_context.unannType()), interface_name)
                    else:
                        if package_name is None:
                            break
                        rewriter.replace(utils_listener.TokensInfo(var.parser_context.unannType()), package_name + '.' + interface_name)
            for field_name in fields_of_interest:
                f = fields_of_interest[field_name]
                if c.file_info.has_imported_package(package_name):
                    typename = interface_name
                else:
                    if package_name is None:
                        break
                    typename = package_name + '.' + interface_name
                if len(f.neighbor_names) == 0:
                    rewriter.replace(utils_listener.TokensInfo(f.parser_context.unannType()), typename)
                else:
                    rewriter.replace(utils_listener.TokensInfo(f.all_variable_declarator_contexts[f.index_in_variable_declarators]), "")
                    rewriter.insert_after(
                        f.get_tokens_info(),
                        "\n    " + typename + " " + f.name + (" = " + f.initializer + ";" if f.initializer is not None else ";")
                    )

    # Create the interface
    interface_file_content = (
        "package " + package_name +"\n\n"
        + "public interface " + interface_name + "\n"
        + "{\n"
    )
    for method_name in method_names:
        interface_file_content += "    " + method_returntypes[method_name] + " " + method_name + "("
        if len(method_parameters[method_name]) > 0:
            interface_file_content += method_parameters[method_name][0][0] + " " + method_parameters[method_name][0][1]
        for i in range(1, len(method_parameters[method_name])):
            param = method_parameters[method_name][i]
            interface_file_content += ", " + param[0] + " " + param[1]
        interface_file_content += ");\n"
    interface_file_content += "}\n"

    file = open(interface_filename, "w+")
    file.write(interface_file_content)
    file.close()

    rewriter.apply()
    return True

if __name__ == "__main__":
    filenames = [
        "tests/extract_interface/A.java",
        "tests/extract_interface/B.java",
        "tests/extract_interface/C.java",
        "tests/extract_interface/D.java",
        "tests/extract_interface/E.java",
        "tests/extract_interface/U.java",
    ]
    if extract_interface(filenames, "test", ["A", "B"], ["a", "b"], "Iab", "tests/extract_interface/Iab.re.java"):
        print("A, B: Success!")
    else:
        print("A, B: Cannot refactor.")
    for third_class in ["C", "D", "E"]:
        if extract_interface(filenames, "test", ["A", "B", third_class], ["a", "b"], "Iab", "tests/extract_interface/Iab.re.java"):
            print("A, B, " + third_class + ": Success!")
        else:
            print("A, B, " + third_class + ": Cannot refactor.")
