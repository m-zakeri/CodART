import utils

def pullup_field(source_filenames: list, package_name: str, class_name: str, field_name: str, filename_mapping = lambda x: x + ".rewritten.java"):
    program = utils.get_program(source_filenames)
    print(program)
    rewriter = utils.Rewriter(program, filename_mapping) # TODO: Fix Rewriter
    # TODO
    return False

# test
pullup_field(["tests/utils_test.java"], "dummy", "dummy", "dummy")
