"""
The script reads a refactoring sequence, x, from input.txt, and execute it on system, s


"""

__version__ = '0.2.0'
__author__ = 'Morteza Zakeri'

import os
import re
import json
import glob
import shutil

import pandas as pd

import codart.config as config
from codart.utility.directory_utils import reset_project, update_understand_database
from codart.sbse.initialize import REFACTORING_MAIN_MAP
from codart.sbse.search_based_refactoring2 import log_project_info


class RefactoringSequenceEvaluation:
    def __init__(self, log_directory):
        super(RefactoringSequenceEvaluation, self).__init__()
        self.log_directory = log_directory
        # self.project_dir_old = 'C:\\Users\\Administrator\\Downloads\\udbs'
        # self.udb_path_old = 'C:/Users/Administrator/Downloads/udbs\\10_water-simulator.udb'
        self.file_path_base_dir_old = 'C:\\Users\\Administrator\\Downloads\\prj_src'  # Server2 path (to be replaced)
        # self.file_path_base_dir_old = 'C:\\Users\\Zakeri\\Documents\\CodARTExp\\prj_src'  # Lab PC

    def evaluate_sequences(self):
        initial_values_path = glob.glob(os.path.join(self.log_directory, 'quality_attrs_initial_values.csv'))[0]
        df_initial = pd.read_csv(
            initial_values_path,
            sep=',',
            index_col=False
        )

        res_path = glob.glob(os.path.join(self.log_directory, 'best_refactoring_sequences_objectives_extended.csv'))[0]
        col_names = ['generation', 'reusability', 'understandability', 'flexibility', 'functionality', 'effectiveness',
                     'extendability', 'testability', 'modularity']

        # if config.PROBLEM == 0:
        #     col_names = ['generation', 'testability']
        # else:
        #     col_names = None
        #     return

        df_res = pd.read_csv(
            res_path,
            sep=',',
            # header=None,
            # names=col_names,
            index_col=False
        )
        print('df initial')
        print(df_initial)
        print('df_res')
        print(df_res)

        evaluation_results = []
        for index, row in df_res.iterrows():
            # We should use positive quality attributes
            raw_improvements = [item - df_initial[col_names[i + 1]].iloc[-1] for i, item in enumerate(row[1:])]
            relative_improvements = [
                (item - df_initial[col_names[i + 1]].iloc[-1]) / abs(df_initial[col_names[i + 1]].iloc[-1])
                for i, item in enumerate(row[1:])
            ]

            quality_gain_raw = [sum(raw_improvements)]
            quality_gain_relative = [
                (sum(row[1:]) / sum([df_initial[col].iloc[-1] for col in col_names[1:]])) - 1
            ]  # single

            evaluation_results.append(
                [*raw_improvements, *relative_improvements,
                 *quality_gain_raw, *quality_gain_relative]
            )

        evaluation_results_cols = [*[f'{name}_raw_improvement' for name in col_names[1:]],
                                   *[f'{name}_relative_improvement' for name in col_names[1:]],
                                   *['raw_quality_gain', 'relative_quality_gain']]

        df_final_result = pd.DataFrame(data=evaluation_results, columns=evaluation_results_cols)
        print(df_final_result)
        df_final_result.to_csv(f'{config.PROJECT_LOG_DIR}evaluation_results.csv', index=False)

    def execute_from_json_log(self, input_file_path=None, reset=True):
        if input_file_path is None:
            input_file_path = glob.glob(os.path.join(self.log_directory, 'best_refactoring_sequences*.json'))[0]

        # log_project_info(reset_=True, )

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
                if refactoring_params.get('class_path'):
                    refactoring_params['class_path'] = refactoring_params['class_path'].replace(
                        self.file_path_base_dir_old,
                        config.PROJECT_ROOT_DIR
                    )
                chromosome_new.append((REFACTORING_MAIN_MAP[gene_[0]], refactoring_params, gene_[0]))
            population.append(chromosome_new)

        # print(population)
        # quit()
        applicability_map = {
            'Project': [],
            'Sequence': [],
            'Applied refactorings': [],
            'Rejected refactorings': []
        }
        for k, refactoring_sequence in enumerate(population):
            true_refactorings_count = 0
            false_refactorings_count = 0
            reset_project()

            # Apply sequence X to system S
            for refactoring_operation in refactoring_sequence:
                res = refactoring_operation[0](**refactoring_operation[1])
                update_understand_database(config.UDB_PATH)
                if res:
                    true_refactorings_count += 1
                else:
                    false_refactorings_count += 1
                config.logger.info(f"Executed {refactoring_operation[2]} with status {res}")

            applicability_map['Project'].append(config.PROJECT_NAME)
            applicability_map['Sequence'].append(k)
            applicability_map['Applied refactorings'].append(true_refactorings_count)
            applicability_map['Rejected refactorings'].append(false_refactorings_count)

            continue

            # Dump refactored project
            dump_path = os.path.join(
                config.PROJECT_ROOT_DIR,
                f'{config.PROJECT_NAME}_refactored_with_algorithm{config.PROBLEM}_rand',
                f'dump{k}'
            )

            if not os.path.exists(config.PROJECT_ROOT_DIR):
                os.mkdir(dump_path)

            shutil.copytree(config.PROJECT_PATH, dump_path)

            # Compute quality metrics
            log_project_info(
                reset_=False,
                quality_attributes_path=os.path.join(
                    config.PROJECT_LOG_DIR,
                    'best_refactoring_sequences_objectives_extended.csv'
                ),
                generation='-1',  # config.MAX_ITERATIONS,
                testability_verbose=True,
                testability_log_path=os.path.join(
                    config.PROJECT_LOG_DIR,
                    f'classes_testability2_for_problem_{config.PROBLEM}_best_sequence_{k}.csv'
                )
            )

        # Log applied and rejected refactorings
        df = pd.DataFrame(data=applicability_map)
        df.to_csv(os.path.join(config.PROJECT_LOG_DIR, 'applicability_map.csv'), index=False)

        if reset:
            reset_project()

    def analysis_refactoring_sequences(self, input_file_path=None, reset=True):
        if input_file_path is None:
            input_file_path = glob.glob(os.path.join(self.log_directory, 'best_refactoring_sequences*.json'))[0]
        with open(input_file_path, 'r', encoding='utf-8') as fp:
            population_trimmed = json.load(fp)
        population = []
        position_map = {
            'Project': [],
            'Refactoring': [],
            'Position': []
        }
        for chromosome in population_trimmed:
            for i, gene_ in enumerate(chromosome):
                refactoring_name = gene_[0]
                position_map['Project'].append(config.PROJECT_NAME)
                position_map['Refactoring'].append(gene_[0])
                position_map['Position'].append(i)

        df = pd.DataFrame(data=position_map)
        df.to_csv(os.path.join(config.PROJECT_LOG_DIR, 'positions_map.csv'), index=False)

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


def measure_ad_hoc_project_quality():
    # create_understand_database(project_dir=config.PROJECT_PATH, db_dir=config.UDB_ROOT_DIR)
    log_project_info()


if __name__ == '__main__':
    # measure_ad_hoc_project_quality()
    # quit()
    reset_project()
    # quit()
    # execute_refactoring_sequence()
    eval_ = RefactoringSequenceEvaluation(log_directory=config.PROJECT_LOG_DIR)
    eval_.execute_from_json_log(reset=False)
    # eval_.evaluate_sequences()

    # eval_.analysis_refactoring_sequences()