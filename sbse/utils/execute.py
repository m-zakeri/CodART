import json
import re

from refactorings import make_field_non_static, make_field_static, make_method_static_2, \
    make_method_non_static_2, pullup_field, move_field, move_method, move_class, pushdown_field2, \
    extract_class, pullup_method, pushdown_method, extract_method, pullup_constructor, decrease_method_visibility, \
    increase_method_visibility, decrease_field_visibility, increase_field_visibility

REFACTORING_MAIN_MAP = {
    'Make Field Non-Static': make_field_non_static.main,
    'Make Field Static': make_field_static.main,
    'Make Method Static': make_method_static_2.main,
    'Make Method Non-Static': make_method_non_static_2.main,
    'Pull Up Field': pullup_field.main,
    'Push Down Field': pushdown_field2.main,
    'Pull Up Method': pullup_method.main,
    'Pull Up Constructor': pullup_constructor.main,
    'Push Down Method': pushdown_method.main,
    'Move Field': move_field.main,
    'Move Method': move_method.main,
    'Move Class': move_class.main,
    'Extract Class': extract_class.main,
    'Extract Method': extract_method.main,
    'Increase Field Visibility': increase_field_visibility.main,
    'Increase Method Visibility': increase_method_visibility.main,
    'Decrease Field Visibility': decrease_field_visibility.main,
    'Decrease Method Visibility': decrease_method_visibility.main,
}


def execute_from_log(input_file_path):
    """
    input_file_path: The path of input data from log.

    Example: Take a look at ./input.txt
    """
    with open(input_file_path, 'r') as f:
        data = f.read().split('\n')
        for row in data:
            refactoring_name = re.search(', (.+?)(\w+)*\(', row).group()[1:-1].strip()
            params = re.search('{(.+?)}', row).group().strip()
            params = params.replace("'", '"')
            params = params.replace("False", "false")
            params = params.replace("True", "true")
            params = json.loads(params)

            main_function = REFACTORING_MAIN_MAP[refactoring_name](**params)
            print(f"Executed {refactoring_name}...")


if __name__ == '__main__':
    execute_from_log('/home/ali/Documents/IUST/CodART/sbse/utils/input.txt')
