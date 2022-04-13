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
from sbse.initialize import REFACTORING_MAIN_MAP

from metrics import qmood
from metrics.modularity import main as modularity_main
from metrics.testability_prediction2 import main as testability_main


# project_dir_old = 'C:\\Users\\Administrator\\Downloads\\udbs'
# udb_path_old = 'C:/Users/Administrator/Downloads/udbs\\10_water-simulator.udb'
file_path_base_dir_old = 'C:\\Users\\Administrator\\Downloads\\prj_src'  # System server2 path (to be replaced)
# file_path_base_dir_old = 'C:\\Users\\Administrator\\Downloads\\IdeaProjects2_Cleaned'  # For JOpenChart project only


def reset_project():
    # Stage 0: Git restore
    config.logger.debug("Executing git restore.")
    # git restore .
    # git clean -f -d
    git_restore(config.PROJECT_PATH)
    config.logger.debug("Updating understand database after git restore.")
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


def print_objective_initial_values():
    reset_project()
    design_metric = qmood.DesignMetrics(config.UDB_PATH)
    design_quality_attribute = qmood.DesignQualityAttributes(config.UDB_PATH)
    metrics_dict = {
        "DSC": design_metric.DSC,
        "NOH": design_metric.NOH,
        "ANA": design_metric.ANA,
        "MOA": design_metric.MOA,
        "DAM": design_metric.DAM,
        "CAMC": design_metric.CAMC,
        "CIS": design_metric.CIS,
        "NOM": design_metric.NOM,
        "DCC": design_metric.DCC,
        "MFA": design_metric.MFA,
        "NOP": design_metric.NOP
    }

    avg_, sum_ = design_quality_attribute.average_sum
    t_ = testability_main(config.UDB_PATH, initial_value=config.CURRENT_METRICS.get("TEST", 1.0))
    m_ = modularity_main(config.UDB_PATH, initial_value=config.CURRENT_METRICS.get("MODULE", 1.0))

    objectives = {
        "reusability": design_quality_attribute.reusability,
        "understandability": design_quality_attribute.understandability,
        "flexibility": design_quality_attribute.flexibility,
        "functionality": design_quality_attribute.functionality,
        "effectiveness": design_quality_attribute.effectiveness,
        "extendability": design_quality_attribute.extendability,
        "testability": t_,
        "modularity": m_,
        #
        "average qmood": avg_,
        "sum qmood ": sum_
    }

    print('QMOOD design metrics (N):')
    print(metrics_dict)

    print('Objectives:')
    print(objectives)


if __name__ == '__main__':
    directory_name_ = os.path.dirname(__file__)
    refactoring_sequence_input_file = os.path.join(directory_name_, r'input.txt')
    # execute_from_log(input_file_path=refactoring_sequence_input_file)
    print_objective_initial_values()

