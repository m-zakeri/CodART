"""
The script reads a refactoring sequence, x, from input.txt, and execute it on system, s


"""

__version__ = '0.2.0'
__author__ = 'Morteza Zakeri'


import os
import re
import json

import sbse.config as config
from codart.utility.directory_utils import git_restore, update_understand_database
from sbse.config import logger

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

# project_dir_old = 'C:\\Users\\Administrator\\Downloads\\udbs'
# udb_path_old = 'C:/Users/Administrator/Downloads/udbs\\10_water-simulator.udb'
file_path_base_dir_old = 'C:\\Users\\Administrator\\Downloads\\prj_src'  # System server2 path (to be replaced)
# file_path_base_dir_old = 'C:\\Users\\Administrator\\Downloads\\IdeaProjects2_Cleaned'  # For JOpenChart project only


def reset_project():
    # Stage 0: Git restore
    logger.debug("Executing git restore.")
    # git restore .
    # git clean -f -d
    git_restore(config.PROJECT_PATH)
    logger.debug("Updating understand database after git restore.")
    update_understand_database(config.UDB_PATH)
    # quit()


def execute_from_log(input_file_path):
    """
    input_file_path: The path of input data from log.

    Example: Take a look at ./input.txt
    """

    reset_project()
    with open(input_file_path, 'r') as f:
        data = f.read().split('\n')
        for row in data:
            refactoring_name = re.search(', (.+?)(\w+)*\(', row).group()[1:-1].strip()
            params = re.search('{(.+?)}', row).group().strip()
            params = params.replace("'", '"')
            params = params.replace("False", "false")
            params = params.replace("True", "true")
            params = json.loads(params)

            if params.get('udb_path'):
                params['udb_path'] = config.UDB_PATH
            if params.get('project_dir'):
                params['project_dir'] = config.PROJECT_PATH
            if params.get('file_path'):
                params['file_path'] = params['file_path'].replace(file_path_base_dir_old, config.PROJECT_ROOT_DIR)
            print(refactoring_name, params)

            main_function = REFACTORING_MAIN_MAP[refactoring_name](**params)
            print(f"Executed {refactoring_name} with status {main_function}")
            update_understand_database(config.UDB_PATH)
            print('-' * 100)


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    refactoring_sequence_input_file = os.path.join(dirname, r'input.txt')
    execute_from_log(input_file_path=refactoring_sequence_input_file)
