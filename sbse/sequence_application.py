"""
The script reads a refactoring sequence, x, from input.txt, and execute it on system, s


"""

__version__ = '0.2.0'
__author__ = 'Morteza Zakeri'

import os
import re
import json
import glob

import pandas as pd

import sbse.config as config
from codart.utility.directory_utils import reset_project, update_understand_database
from sbse.initialize import REFACTORING_MAIN_MAP
from sbse.search_based_refactoring2 import log_project_info

from metrics import qmood
from metrics.modularity import main as modularity_main
from metrics.testability_prediction2 import main as testability_main


class RefactoringSequenceEvaluation:
    def __init__(self, log_directory):
        super(RefactoringSequenceEvaluation, self).__init__()
        self.log_directory = log_directory
        # self.project_dir_old = 'C:\\Users\\Administrator\\Downloads\\udbs'
        # self.udb_path_old = 'C:/Users/Administrator/Downloads/udbs\\10_water-simulator.udb'
        self.file_path_base_dir_old = 'C:\\Users\\Administrator\\Downloads\\prj_src'  # Server2 path (to be replaced)

    def evaluate_sequences(self):
        initial_values_path = glob.glob(f'{self.log_directory}quality_attrs_initial_values.csv')[0]
        df_initial = pd.read_csv(
            initial_values_path,
            sep=',',
            index_col=False
        )

        res_path = glob.glob(f'{self.log_directory}best_refactoring_sequences_objectives*.csv')[0]
        if config.PROBLEM == 2:
            col_names = ['generation',
                         'reusability', 'understandability', 'flexibility', 'functionality', 'effectiveness',
                         'extendability',
                         'testability', 'modularity']
        elif config.PROBLEM == 0:
            col_names = ['generation', 'testability']
        else:
            col_names = None
            return

        df_res = pd.read_csv(
            res_path,
            sep=',',
            header=None,
            names=col_names,
            index_col=False
        )
        # print(df)

        evaluation_results = []
        for index, row in df_res.iterrows():
            raw_improvements = [(-item)-df_initial[col_names[i+1]][0] for i, item in enumerate(row[1:])]
            relative_improvements = [((-item)-df_initial[col_names[i+1]][0])/abs(df_initial[col_names[i+1]][0])
                                     for i, item in enumerate(row[1:])]

            quality_gain_raw = [sum(raw_improvements)]
            quality_gain_relative = [(sum(-row[1:])/sum([df_initial[col][0] for col in col_names[1:]])) - 1]  # single

            evaluation_results.append([*raw_improvements, *relative_improvements,
                                       *quality_gain_raw, *quality_gain_relative])

        evaluation_results_cols = [*[f'{name}_raw_improvement' for name in col_names[1:]],
                                   *[f'{name}_relative_improvement' for name in col_names[1:]],
                                   *['raw_quality_gain', 'relative_quality_gain']]

        df_final_result = pd.DataFrame(data=evaluation_results, columns=evaluation_results_cols)
        print(df_final_result)
        df_final_result.to_csv(f'{config.PROJECT_LOG_DIR}evaluation_results.csv', index=False)

    def execute_from_json_log(self, input_file_path=None):
        if input_file_path is None:
            input_file_path = glob.glob(f'{self.log_directory}best_refactoring_sequences*.json')[0]

        population = []
        with open(input_file_path, 'r', encoding='utf-8') as fp:
            population_trimmed = json.load(fp)

        for chromosome in population_trimmed:
            chromosome_new = []
            for gene_ in chromosome:
                refactoring_params = gene_[1]
                if refactoring_params.get('udb_path'):
                    refactoring_params['udb_path'] = config.UDB_PATH
                if refactoring_params.get('project_dir'):
                    refactoring_params['project_dir'] = config.PROJECT_PATH
                if refactoring_params.get('file_path'):
                    refactoring_params['file_path'] = refactoring_params['file_path'].replace(
                        self.file_path_base_dir_old,
                        config.PROJECT_ROOT_DIR
                    )
                chromosome_new.append((REFACTORING_MAIN_MAP[gene_[0]], refactoring_params, gene_[0]))
            population.append(chromosome_new)

        print(population)
        # quit()
        for refactoring_sequence in population:
            reset_project()
            # Apply sequence X to system S
            for refactoring_operation in refactoring_sequence:
                res = refactoring_operation[0](**refactoring_operation[1])
                update_understand_database(config.UDB_PATH)
                print(f"Executed {refactoring_operation[2]} with status {res}")

            # Compute quality metrics
            log_project_info(
                reset_=False,
                quality_attributes_path=f'{config.PROJECT_LOG_DIR}best_refactoring_sequences_objectives_extended.csv',
                generation=config.MAX_ITERATIONS
            )

        reset_project()

    def execute_from_txt_log(self, input_file_path):
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

            if params.get('udb_path'):
                params['udb_path'] = config.UDB_PATH
            if params.get('project_dir'):
                params['project_dir'] = config.PROJECT_PATH
            if params.get('file_path'):
                params['file_path'] = params['file_path'].replace(self.file_path_base_dir_old, config.PROJECT_ROOT_DIR)
            print(refactoring_name, params)

            res = REFACTORING_MAIN_MAP[refactoring_name](**params)
            print(f"Executed {refactoring_name} with status {res}")
            update_understand_database(config.UDB_PATH)
            print('-' * 100)


def execute_refactoring_sequence():
    directory_name_ = os.path.dirname(__file__)
    refactoring_sequence_input_file = os.path.join(directory_name_, r'utils/input.txt')
    # reset_project()
    # execute_from_txt_log(input_file_path=refactoring_sequence_input_file)


if __name__ == '__main__':
    # execute_refactoring_sequence()
    eval_ = RefactoringSequenceEvaluation(log_directory=config.PROJECT_LOG_DIR)
    eval_.evaluate_sequences()
    eval_.execute_from_json_log()
