"""
The script reads a refactoring sequence, x, from input.txt, and execute it on system, s


"""

__version__ = '0.2.0'
__author__ = 'Morteza Zakeri'


import os
import re
import json

import sbse.config as config
from codart.utility.directory_utils import reset_project, update_understand_database
from sbse.initialize import REFACTORING_MAIN_MAP

from metrics import qmood
from metrics.modularity import main as modularity_main
from metrics.testability_prediction2 import main as testability_main


# project_dir_old = 'C:\\Users\\Administrator\\Downloads\\udbs'
# udb_path_old = 'C:/Users/Administrator/Downloads/udbs\\10_water-simulator.udb'
file_path_base_dir_old = 'C:\\Users\\Administrator\\Downloads\\prj_src'  # System server2 path (to be replaced)
# file_path_base_dir_old = 'C:\\Users\\Administrator\\Downloads\\IdeaProjects2_Cleaned'  # For JOpenChart project only


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
    directory_name_ = os.path.dirname(__file__)
    refactoring_sequence_input_file = os.path.join(directory_name_, r'input.txt')
    # execute_from_log(input_file_path=refactoring_sequence_input_file)

