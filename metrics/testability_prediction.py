"""

This module contains testability prediction script
to be used in refactoring process in addition to qmood metrics

## Reference
[1] ADAFEST2 paper
[2] TsDD paper


"""

__version__ = '0.1.0'
__author__ = 'Morteza Zakeri'

import math
import os
import warnings

import joblib
import numpy as np
import pandas as pd

try:
    import understand as und
except ImportError as e:
    print(e)

from sklearn.experimental import enable_hist_gradient_boosting  # noqa
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import QuantileTransformer

import metrics
from metrics import metrics_names
from metrics.metrics_jcode_odor import JCodeOdorMetric
from metrics.naming import UnderstandUtility


# patch_sklearn()


class TestabilityMetrics:
    """
    Compute all required metrics for computing Coverageability and testability.
    This includes typical source code metrics, lexical metrics, and sub-metrics.
    Metrics can be computed in project-level, package-level, class-level, and method-level.
    For computing testability and Coverageability we use package-level and class-level metrics.
    All methods are class methods.

    """

    @classmethod
    def get_class_ordinary_metrics_names(cls) -> list:
        return metrics.metrics_names.class_ordinary_metrics_names

    @classmethod
    def get_class_lexicon_metrics_names(cls) -> list:
        return metrics.metrics_names.class_lexicon_metrics_names

    @classmethod
    def get_package_metrics_names(cls) -> list:
        return metrics.metrics_names.package_metrics_names

    @classmethod
    def get_project_metrics_names(cls) -> list:
        return metrics.metrics_names.project_metrics_names

    @classmethod
    def get_all_metrics_names(cls) -> list:
        metrics = list()
        # print('project_metrics number: ', len(TestabilityMetrics.get_project_metrics_names()))
        # for metric_name in TestabilityMetrics.get_project_metrics_names():
        #     metrics.append('PJ_' + metric_name)

        # print('package_metrics number: ', len(TestabilityMetrics.get_package_metrics_names()))
        for metric_name in TestabilityMetrics.get_package_metrics_names():
            metrics.append('PK_' + metric_name)

        # SOOTI is now corrected.
        # print('class_lexicon_metrics number: ', len(TestabilityMetrics.get_class_lexicon_metrics_names()))
        for metric_name in TestabilityMetrics.get_class_lexicon_metrics_names():
            metrics.append('CSLEX_' + metric_name)

        # print('class_ordinary_metrics number: ', len(TestabilityMetrics.get_class_ordinary_metrics_names()))
        for metric_name in TestabilityMetrics.get_class_ordinary_metrics_names():
            metrics.append('CSORD_' + metric_name)

        # print('All available metrics: {0}'.format(len(metrics)))
        return metrics

    @classmethod
    def get_all_primary_metrics_names(cls) -> list:
        primary_metrics_names = list()
        for metric_name in metrics.metrics_names.project_metrics_names_primary:
            primary_metrics_names.append('PJ_' + metric_name)
        for metric_name in metrics.metrics_names.package_metrics_names_primary:
            primary_metrics_names.append('PK_' + metric_name)
        for metric_name in metrics.metrics_names.class_ordinary_metrics_names_primary:
            primary_metrics_names.append('CSORD_' + metric_name)
        for metric_name in metrics.metrics_names.class_lexicon_metrics_names:
            primary_metrics_names.append('CSLEX_' + metric_name)
        return primary_metrics_names

    @classmethod
    def compute_java_class_metrics2(cls, db=None, entity=None):
        """
        Strategy #2: Take a list of all classes and search for target class
        Which strategy is used for our final setting? I do not know!

        :param db:
        :param entity:
        :return:
        """

        # 1. Understand built-in class metrics
        class_metrics = entity.metric(entity.metrics())
        # print('number of metrics for class "{0}": {1}, and metrics: {2}'.format(entity.longname(),
        #                                                                         len(class_metrics), class_metrics), )

        # for i, metric in enumerate(class_metrics.keys()):
        #     print(i + 1, ': ', metric, class_metrics[metric])
        # print(class_metrics['AvgCyclomatic'])

        # 2. Systematically created metrics
        j_code_odor_metric = JCodeOdorMetric()
        method_list = UnderstandUtility.get_method_of_class_java2(db=db, class_name=entity.longname())

        if method_list is None:
            raise TypeError('method_list is none for class "{}"'.format(entity.longname()))

        # 2.1 CSCC
        class_cyclomatic_list = list()
        class_cyclomatic_namm_list = list()

        class_cyclomatic_strict_list = list()
        class_cyclomatic_strict_namm_list = list()

        class_cyclomatic_modified_list = list()
        class_cyclomatic_modified_namm_list = list()

        class_essential_list = list()
        class_essential_namm_list = list()

        for method in method_list:
            class_cyclomatic_list.append(method.metric(['Cyclomatic'])['Cyclomatic'])
            class_cyclomatic_strict_list.append(method.metric(['CyclomaticStrict'])['CyclomaticStrict'])
            class_cyclomatic_modified_list.append(method.metric(['CyclomaticModified'])['CyclomaticModified'])
            class_essential_list.append(method.metric(['Essential'])['Essential'])
            if not j_code_odor_metric.is_accesor_or_mutator(method_entity=method):
                class_cyclomatic_namm_list.append(method.metric(['Cyclomatic'])['Cyclomatic'])
                class_cyclomatic_strict_namm_list.append(method.metric(['CyclomaticStrict'])['CyclomaticStrict'])
                class_cyclomatic_modified_namm_list.append(method.metric(['CyclomaticModified'])['CyclomaticModified'])
                class_essential_namm_list.append(method.metric(['Essential'])['Essential'])

        cls.remove_none_from_lists([class_cyclomatic_list, class_cyclomatic_namm_list,
                                    class_cyclomatic_strict_list, class_cyclomatic_strict_namm_list,
                                    class_cyclomatic_modified_list, class_cyclomatic_modified_namm_list,
                                    class_essential_list, class_essential_namm_list])

        # CSCC
        # 2.1.13
        class_metrics.update({'MinCyclomatic': min(class_cyclomatic_list)})
        # 2.1.14
        class_metrics.update({'MinCyclomaticStrict': min(class_cyclomatic_strict_list)})
        # 2.1.15
        class_metrics.update({'MinCyclomaticModified': min(class_cyclomatic_modified_list)})
        # 2.1.16
        class_metrics.update({'MinEssential': min(class_essential_list)})

        # 2.1.17
        class_metrics.update({'SDCyclomatic': np.std(class_cyclomatic_list)})
        # 2.1.18
        class_metrics.update({'SDCyclomaticStrict': np.std(class_cyclomatic_strict_list)})
        # 2.1.19
        class_metrics.update({'SDCyclomaticModified': np.std(class_cyclomatic_modified_list)})
        # 2.1.20
        class_metrics.update({'SDEssential': np.std(class_essential_list)})

        class_metrics.update({'LogCyclomatic': math.log10(sum(class_cyclomatic_list) + 1)})
        class_metrics.update({'LogCyclomaticStrict': math.log10(sum(class_cyclomatic_strict_list) + 1)})
        class_metrics.update({'LogCyclomaticModified': math.log10(sum(class_cyclomatic_modified_list) + 1)})
        class_metrics.update({'LogEssential': math.log10(sum(class_essential_list) + 1)})

        # CSCCNAMM
        # 2.1.21
        class_metrics.update({'SumCyclomaticNAMM': sum(class_cyclomatic_namm_list)})
        # 2.1.22
        class_metrics.update({'SumCyclomaticStrictNAMM': sum(class_cyclomatic_strict_namm_list)})
        # 2.1.23
        class_metrics.update({'SumCyclomaticModifiedNAMM': sum(class_cyclomatic_modified_namm_list)})
        # 2.1.24
        class_metrics.update({'SumEssentialNAMM': sum(class_essential_namm_list)})

        # 2.1.25
        class_metrics.update({'MaxCyclomaticNAMM': max(class_cyclomatic_namm_list)})
        # 2.1.26
        class_metrics.update({'MaxCyclomaticStrictNAMM': max(class_cyclomatic_strict_namm_list)})
        # 2.1.27
        class_metrics.update({'MaxCyclomaticModifiedNAMM': max(class_cyclomatic_modified_namm_list)})
        # 2.1.28
        class_metrics.update({'MaxEssentialNAMM': max(class_essential_namm_list)})

        # 2.1.29
        class_metrics.update({'AvgCyclomaticNAMM': sum(class_cyclomatic_namm_list) / len(class_cyclomatic_namm_list)})
        # 2.1.30
        class_metrics.update({'AvgCyclomaticStrictNAMM': sum(class_cyclomatic_strict_namm_list) / len(
            class_cyclomatic_strict_namm_list)})
        # 2.1.31
        class_metrics.update({'AvgCyclomaticModifiedNAMM': sum(class_cyclomatic_modified_namm_list) / len(
            class_cyclomatic_modified_namm_list)})
        # 2.1.32
        class_metrics.update({'AvgEssentialNAMM': sum(class_essential_namm_list) / len(class_essential_namm_list)})

        # 2.1.33
        class_metrics.update({'MinCyclomaticNAMM': min(class_cyclomatic_namm_list)})
        # 2.1.34
        class_metrics.update({'MinCyclomaticStrictNAMM': min(class_cyclomatic_strict_namm_list)})
        # 2.1.35
        class_metrics.update({'MinCyclomaticModifiedNAMM': min(class_cyclomatic_modified_namm_list)})
        # 2.1.36
        class_metrics.update({'MinEssentialNAMM': min(class_essential_namm_list)})

        # 2.1.37
        class_metrics.update({'SDCyclomaticNAMM': np.std(class_cyclomatic_namm_list)})
        # 2.1.38
        class_metrics.update({'SDCyclomaticStrictNAMM': np.std(class_cyclomatic_strict_namm_list)})
        # 2.1.39
        class_metrics.update({'SDCyclomaticModifiedNAMM': np.std(class_cyclomatic_modified_namm_list)})
        # 2.1.40
        class_metrics.update({'SDEssentialNAMM': np.std(class_essential_namm_list)})

        # 2.2 CSNOP (10)
        #
        parameters_length_list = list()
        parameters_length_namm_list = list()
        # number_of_parameters = 0
        # print('method list', len(method_list))
        for method in method_list:
            # if method.library() != "Standard":
            # print('method params', method.longname(), '-->', method.parameters())
            params = method.parameters().split(',')
            if len(params) == 1:
                if params[0] == ' ' or params[0] == '' or params[0] is None:
                    parameters_length_list.append(0)
                else:
                    parameters_length_list.append(1)
            else:
                parameters_length_list.append(len(params))

            if not j_code_odor_metric.is_accesor_or_mutator(method_entity=method):
                if len(params) == 1:
                    if params[0] == ' ' or params[0] == '' or params[0] is None:
                        parameters_length_namm_list.append(0)
                    else:
                        parameters_length_namm_list.append(1)
                else:
                    parameters_length_namm_list.append(len(params))

        cls.remove_none_from_lists([parameters_length_list, parameters_length_namm_list])

        # print('number of parameters', number_of_parameters)
        # CSNOP
        # 2.2.1
        class_metrics.update({'SumCSNOP': sum(parameters_length_list)})
        # 2.2.2
        class_metrics.update({'MaxCSNOP': max(parameters_length_list)})
        # 2.2.3
        class_metrics.update({'MinCSNOP': min(parameters_length_list)})
        # 2.2.4
        class_metrics.update({'AvgCSNOP': sum(parameters_length_list) / len(parameters_length_list)})
        # 2.2.5
        class_metrics.update({'SDCSNOP': np.std(parameters_length_list)})

        # CSNOP_NAMM
        # 2.2.6
        class_metrics.update({'SumCSNOPNAMM': sum(parameters_length_namm_list)})
        # 2.2.7
        class_metrics.update({'MaxCSNOPNAMM': max(parameters_length_namm_list)})
        # 2.2.8
        class_metrics.update({'MinCSNOPNAMM': min(parameters_length_namm_list)})
        # 2.2.9
        class_metrics.update({'AvgCSNOPNAMM': sum(parameters_length_namm_list) / len(parameters_length_namm_list)})
        # 2.2.10
        class_metrics.update({'SDCSNOPNAMM': np.std(parameters_length_namm_list)})

        # 2.3 SCLOC (30)
        #
        line_of_code_list = list()
        line_of_code_namm_list = list()

        line_of_code_decl_list = list()
        line_of_code_decl_namm_list = list()

        line_of_code_exe_list = list()
        line_of_code_exe_namm_list = list()
        for method in method_list:
            line_of_code_list.append(method.metric(['CountLineCode'])['CountLineCode'])
            line_of_code_decl_list.append(method.metric(['CountLineCodeDecl'])['CountLineCodeDecl'])
            line_of_code_exe_list.append(method.metric(['CountLineCodeExe'])['CountLineCodeExe'])
            if not j_code_odor_metric.is_accesor_or_mutator(method_entity=method):
                line_of_code_namm_list.append(method.metric(['CountLineCode'])['CountLineCode'])
                line_of_code_decl_namm_list.append(method.metric(['CountLineCodeDecl'])['CountLineCodeDecl'])
                line_of_code_exe_namm_list.append(method.metric(['CountLineCodeExe'])['CountLineCodeExe'])

        cls.remove_none_from_lists([line_of_code_list, line_of_code_namm_list,
                                    line_of_code_decl_list, line_of_code_decl_namm_list,
                                    line_of_code_exe_list, line_of_code_exe_namm_list])
        # CSLOC_All
        # 2.3.5
        class_metrics.update({'AvgLineCodeDecl': sum(line_of_code_decl_list) / len(line_of_code_decl_list)})
        # 2.3.6
        class_metrics.update({'AvgLineCodeExe': sum(line_of_code_exe_list) / len(line_of_code_exe_list)})

        # 2.3.7
        class_metrics.update({'MaxLineCode': max(line_of_code_list)})
        # 2.3.8
        class_metrics.update({'MaxLineCodeDecl': max(line_of_code_decl_list)})
        # 2.3.9
        class_metrics.update({'MaxLineCodeExe': max(line_of_code_exe_list)})

        # 2.3.10
        class_metrics.update({'MinLineCode': min(line_of_code_list)})
        # 2.3.11
        class_metrics.update({'MinLineCodeDecl': min(line_of_code_decl_list)})
        # 2.3.12
        class_metrics.update({'MinLineCodeExe': min(line_of_code_exe_list)})

        # 2.3.13
        class_metrics.update({'SDLineCode': np.std(line_of_code_list)})
        # 2.3.14
        class_metrics.update({'SDLineCodeDecl': np.std(line_of_code_decl_list)})
        # 2.3.15
        class_metrics.update({'SDLineCodeExe': np.std(line_of_code_exe_list)})

        class_metrics.update({'LogLineCode': math.log10(sum(line_of_code_list) + 1)})
        class_metrics.update({'LogLineCodeDecl': math.log10(sum(line_of_code_decl_list) + 1)})
        class_metrics.update({'LogLineCodeExe': math.log10(sum(line_of_code_exe_list) + 1)})

        # CSLOC_NAMM
        # 2.3.16
        class_metrics.update({'CountLineCodeNAMM': sum(line_of_code_namm_list)})
        # 2.3.17
        class_metrics.update({'CountLineCodeDeclNAMM': sum(line_of_code_decl_namm_list)})

        # print('!@#', sum(line_of_code_decl_namm_list))
        # quit()

        # 2.3.18
        class_metrics.update({'CountLineCodeExeNAMM': sum(line_of_code_exe_namm_list)})

        # 2.3.19
        class_metrics.update({'AvgLineCodeNAMM': sum(line_of_code_namm_list) / len(line_of_code_namm_list)})
        # 2.3.20
        class_metrics.update(
            {'AvgLineCodeDeclNAMM': sum(line_of_code_decl_namm_list) / len(line_of_code_decl_namm_list)})
        # 2.3.21
        class_metrics.update({'AvgLineCodeExeNAMM': sum(line_of_code_exe_namm_list) / len(line_of_code_exe_namm_list)})

        # 2.3.22
        class_metrics.update({'MaxLineCodeNAMM': max(line_of_code_namm_list)})
        # 2.3.23
        class_metrics.update({'MaxLineCodeDeclNAMM': max(line_of_code_decl_namm_list)})
        # 2.3.24
        class_metrics.update({'MaxLineCodeExeNAMM': max(line_of_code_exe_namm_list)})

        # 2.3.25
        class_metrics.update({'MinLineCodeNAMM': min(line_of_code_namm_list)})
        # 2.3.26
        class_metrics.update({'MinLineCodeDeclNAMM': min(line_of_code_decl_namm_list)})
        # 2.3.27
        class_metrics.update({'MinLineCodeExeNAMM': min(line_of_code_exe_namm_list)})

        # 2.3.28
        class_metrics.update({'SDLineCodeNAMM': np.std(line_of_code_namm_list)})
        # 2.3.29
        class_metrics.update({'SDLineCodeDeclNAMM': np.std(line_of_code_decl_namm_list)})
        # print('!@#', np.std(line_of_code_decl_namm_list))
        # quit()
        # 2.3.30
        class_metrics.update({'SDLineCodeExeNAMM': np.std(line_of_code_exe_namm_list)})

        # ----------------------------------------------------------------
        # 2.4 CSNOST (3-->30)
        # To be completed in future work
        number_of_stmt_list = list()
        number_of_stmt_namm_list = list()

        number_of_stmt_decl_list = list()
        number_of_stmt_decl_namm_list = list()

        number_of_stmt_exe_list = list()
        number_of_stmt_exe_namm_list = list()

        for method in method_list:
            number_of_stmt_list.append(method.metric(['CountStmt'])['CountStmt'])
            number_of_stmt_decl_list.append(method.metric(['CountStmtDecl'])['CountStmtDecl'])
            number_of_stmt_exe_list.append(method.metric(['CountStmtExe'])['CountStmtExe'])
            if not j_code_odor_metric.is_accesor_or_mutator(method_entity=method):
                number_of_stmt_namm_list.append(method.metric(['CountStmt'])['CountStmt'])
                number_of_stmt_decl_namm_list.append(method.metric(['CountStmtDecl'])['CountStmtDecl'])
                number_of_stmt_exe_namm_list.append(method.metric(['CountStmtExe'])['CountStmtExe'])

        cls.remove_none_from_lists([number_of_stmt_list, number_of_stmt_namm_list,
                                    number_of_stmt_decl_list, number_of_stmt_decl_namm_list,
                                    number_of_stmt_exe_list, number_of_stmt_exe_namm_list])

        # CSNOST_All
        # 2.4.4
        class_metrics.update({'AvgStmt': sum(number_of_stmt_list) / len(number_of_stmt_list)})
        # 2.4.5
        class_metrics.update({'AvgStmtDecl': sum(number_of_stmt_decl_list) / len(number_of_stmt_decl_list)})
        # 2.4.6
        class_metrics.update({'AvgStmtExe': sum(number_of_stmt_exe_list) / len(number_of_stmt_exe_list)})

        # 2.4.7
        class_metrics.update({'MaxStmt': max(number_of_stmt_list)})
        # 2.4.8
        class_metrics.update({'MaxStmtDecl': max(number_of_stmt_decl_list)})
        # 2.4.9
        class_metrics.update({'MaxStmtExe': max(number_of_stmt_exe_list)})

        # 2.4.10
        class_metrics.update({'MinStmt': min(number_of_stmt_list)})
        # 2.4.11
        class_metrics.update({'MinStmtDecl': min(number_of_stmt_decl_list)})
        # 2.4.12
        class_metrics.update({'MinStmtExe': min(number_of_stmt_exe_list)})

        # 2.4.13
        class_metrics.update({'SDStmt': np.std(number_of_stmt_list)})
        # 2.4.14
        class_metrics.update({'SDStmtDecl': np.std(number_of_stmt_decl_list)})
        # 2.4.15
        class_metrics.update({'SDStmtExe': np.std(number_of_stmt_exe_list)})

        class_metrics.update({'LogStmt': math.log10(sum(number_of_stmt_list) + 1)})
        class_metrics.update({'LogStmtDecl': math.log10(sum(number_of_stmt_decl_list) + 1)})
        class_metrics.update({'LogStmtExe': math.log10(sum(number_of_stmt_exe_list) + 1)})

        # CSNOST_NAMM
        # 2.4.16
        class_metrics.update({'CountStmtNAMM': sum(number_of_stmt_namm_list)})
        # 2.4.17
        class_metrics.update({'CountStmtDeclNAMM': sum(number_of_stmt_decl_namm_list)})
        # 2.4.18
        class_metrics.update({'CountStmtExeNAMM': sum(number_of_stmt_exe_namm_list)})

        # 2.4.19
        class_metrics.update({'AvgStmtNAMM': sum(number_of_stmt_namm_list) / len(number_of_stmt_namm_list)})
        # 2.4.20
        class_metrics.update(
            {'AvgStmtDeclNAMM': sum(number_of_stmt_decl_namm_list) / len(number_of_stmt_decl_namm_list)})
        # 2.4.21
        class_metrics.update({'AvgStmtExeNAMM': sum(number_of_stmt_exe_namm_list) / len(number_of_stmt_exe_namm_list)})

        # 2.4.22
        class_metrics.update({'MaxStmtNAMM': max(number_of_stmt_namm_list)})
        # 2.4.23
        class_metrics.update({'MaxStmtDeclNAMM': max(number_of_stmt_decl_namm_list)})
        # 2.4.24
        class_metrics.update({'MaxStmtExeNAMM': max(number_of_stmt_exe_namm_list)})

        # 2.4.25
        class_metrics.update({'MinStmtNAMM': min(number_of_stmt_namm_list)})
        # 2.4.26
        class_metrics.update({'MinStmtDeclNAMM': min(number_of_stmt_decl_namm_list)})
        # 2.4.27
        class_metrics.update({'MinStmtExeNAMM': min(number_of_stmt_exe_namm_list)})

        # 2.4.28
        class_metrics.update({'SDStmtNAMM': np.std(number_of_stmt_namm_list)})
        # 2.4.29
        class_metrics.update({'SDStmtDeclNAMM': np.std(number_of_stmt_decl_namm_list)})
        # 2.4.30
        class_metrics.update({'SDStmtExeNAMM': np.std(number_of_stmt_exe_namm_list)})

        # Class number of not accessor or mutator methods
        # Class max_nesting (4)
        CSNOMNAMM = 0
        max_nesting_list = list()
        for method in method_list:
            max_nesting_list.append(method.metric(['MaxNesting'])['MaxNesting'])
            if not j_code_odor_metric.is_accesor_or_mutator(method_entity=method):
                CSNOMNAMM += 1

        cls.remove_none_from_lists([max_nesting_list])

        class_metrics.update({'CSNOMNAMM': CSNOMNAMM})

        class_metrics.update({'MinNesting': min(max_nesting_list)})
        class_metrics.update({'AvgNesting': sum(max_nesting_list) / len(max_nesting_list)})
        class_metrics.update({'SDNesting': np.std(max_nesting_list)})

        # Custom (JCodeOdor) coupling metrics
        class_metrics.update({'RFC': j_code_odor_metric.RFC(class_name=entity)})
        class_metrics.update({'FANIN': j_code_odor_metric.FANIN(db=db, class_entity=entity)})
        class_metrics.update({'FANOUT': j_code_odor_metric.FANOUT(db=db, class_entity=entity)})

        class_metrics.update({'ATFD': UnderstandUtility.ATFD(db=db, class_entity=entity)})  ### not implement

        class_metrics.update({'CFNAMM': j_code_odor_metric.CFNAMM_Class(class_name=entity)})
        class_metrics.update({'DAC': UnderstandUtility.get_data_abstraction_coupling(db=db, class_entity=entity)})
        class_metrics.update({'NumberOfMethodCalls': UnderstandUtility.number_of_method_call(class_entity=entity)})

        # Visibility metrics
        # Understand built-in metrics plus one custom metric.
        class_metrics.update({'CSNOAMM': j_code_odor_metric.NOMAMM(class_entity=entity)})

        # Inheritance metrics
        class_metrics.update({'NIM': j_code_odor_metric.NIM(class_name=entity)})
        class_metrics.update({'NMO': j_code_odor_metric.NMO(class_name=entity)})

        class_metrics.update({'NOII': UnderstandUtility.NOII(db=db)})  # Not implemented

        # ---------------------------------------
        # New added metric (version 0.3.0, dataset 0.5.0)
        class_count_path_list = list()
        class_count_path_log_list = list()
        class_knots_list = list()
        for method in method_list:
            class_count_path_list.append(method.metric(['CountPath'])['CountPath'])
            class_count_path_log_list.append(method.metric(['CountPathLog'])['CountPathLog'])
            class_knots_list.append(method.metric(['Knots'])['Knots'])

        cls.remove_none_from_lists([class_count_path_list, class_count_path_log_list, class_knots_list])

        class_metrics.update({'SumCountPath': sum(class_count_path_list)})
        class_metrics.update({'MinCountPath': min(class_count_path_list)})
        class_metrics.update({'MaxCountPath': max(class_count_path_list)})
        class_metrics.update({'AvgCountPath': sum(class_count_path_list) / len(class_count_path_list)})
        class_metrics.update({'SDCountPath': np.std(class_count_path_list)})

        class_metrics.update({'SumCountPathLog': sum(class_count_path_log_list)})
        class_metrics.update({'MinCountPathLog': min(class_count_path_log_list)})
        class_metrics.update({'MaxCountPathLog': max(class_count_path_log_list)})
        class_metrics.update({'AvgCountPathLog': sum(class_count_path_log_list) / len(class_count_path_log_list)})
        class_metrics.update({'SDCountPathLog': np.std(class_count_path_log_list)})

        class_metrics.update({'SumKnots': sum(class_knots_list)})
        class_metrics.update({'MinKnots': min(class_knots_list)})
        class_metrics.update({'MaxKnots': max(class_knots_list)})
        class_metrics.update({'AvgKnots': sum(class_knots_list) / len(class_knots_list)})
        class_metrics.update({'SDKnots': np.std(class_knots_list)})

        constructor = UnderstandUtility.get_constructor_of_class_java(db=db, class_name=entity.longname())
        class_metrics.update({'NumberOfClassConstructors': len(constructor)})

        class_metrics.update({'NumberOfDepends': len(entity.depends())})
        class_metrics.update({'NumberOfDependsBy': len(entity.dependsby())})

        class_metrics.update({'NumberOfClassInItsFile': len(
            UnderstandUtility.get_number_of_class_in_file_java(db=db, class_entity=entity))})

        return class_metrics

    @classmethod
    def compute_java_class_metrics_lexicon(cls, db=None, entity=None):
        """

        :param db:
        :param entity:
        :return:
        """
        class_lexicon_metrics_dict = dict()

        # for ib in entity.ib():
        #     print('entity ib', ib)

        # Compute lexicons
        tokens_list = list()
        identifiers_list = list()
        keywords_list = list()
        operators_list = list()

        return_and_print_count = 0
        return_and_print_kw_list = ['return', 'print', 'printf', 'println', 'write', 'writeln']

        condition_count = 0
        condition_kw_list = ['if', 'for', 'while', 'switch', '?', 'assert', ]

        uncondition_count = 0
        uncondition_kw_list = ['break', 'continue', ]

        exception_count = 0
        exception_kw_list = ['try', 'catch', 'throw', 'throws', 'finally', ]

        new_count = 0
        new_count_kw_list = ['new']

        super_count = 0
        super_count_kw_list = ['super']

        dots_count = 0

        try:
            # print('ec', entity.parent().id())
            # source_file_entity = db.ent_from_id(entity.parent().id())

            # print('file', type(source_file_entity), source_file_entity.longname())
            for lexeme in entity.lexer(show_inactive=False):
                # print(lexeme.text(), ': ', lexeme.token())
                tokens_list.append(lexeme.text())
                if lexeme.token() == 'Identifier':
                    identifiers_list.append(lexeme.text())
                if lexeme.token() == 'Keyword':
                    keywords_list.append(lexeme.text())
                if lexeme.token() == 'Operator':
                    operators_list.append(lexeme.text())
                if lexeme.text() in return_and_print_kw_list:
                    return_and_print_count += 1
                if lexeme.text() in condition_kw_list:
                    condition_count += 1
                if lexeme.text() in uncondition_kw_list:
                    uncondition_count += 1
                if lexeme.text() in exception_kw_list:
                    exception_count += 1
                if lexeme.text() in new_count_kw_list:
                    new_count += 1
                if lexeme.text() in super_count_kw_list:
                    super_count += 1
                if lexeme.text() == '.':
                    dots_count += 1
        except:
            raise RuntimeError('Error in computing class lexical metrics for class "{0}"'.format(entity.longname()))

        number_of_assignments = operators_list.count('=')
        number_of_operators_without_assignments = len(operators_list) - number_of_assignments
        number_of_unique_operators = len(set(list(filter('='.__ne__, operators_list))))

        class_lexicon_metrics_dict.update({'NumberOfTokens': len(tokens_list)})
        class_lexicon_metrics_dict.update({'NumberOfUniqueTokens': len(set(tokens_list))})

        class_lexicon_metrics_dict.update({'NumberOfIdentifies': len(identifiers_list)})
        class_lexicon_metrics_dict.update({'NumberOfUniqueIdentifiers': len(set(identifiers_list))})

        class_lexicon_metrics_dict.update({'NumberOfKeywords': len(keywords_list)})
        class_lexicon_metrics_dict.update({'NumberOfUniqueKeywords': len(set(keywords_list))})

        class_lexicon_metrics_dict.update(
            {'NumberOfOperatorsWithoutAssignments': number_of_operators_without_assignments})
        class_lexicon_metrics_dict.update({'NumberOfAssignments': number_of_assignments})
        class_lexicon_metrics_dict.update({'NumberOfUniqueOperators': number_of_unique_operators})

        class_lexicon_metrics_dict.update({'NumberOfDots': dots_count})
        class_lexicon_metrics_dict.update({'NumberOfSemicolons': entity.metric(['CountSemicolon'])['CountSemicolon']})

        class_lexicon_metrics_dict.update({'NumberOfReturnAndPrintStatements': return_and_print_count})
        class_lexicon_metrics_dict.update({'NumberOfConditionalJumpStatements': condition_count})
        class_lexicon_metrics_dict.update({'NumberOfUnConditionalJumpStatements': uncondition_count})
        class_lexicon_metrics_dict.update({'NumberOfExceptionStatements': exception_count})
        class_lexicon_metrics_dict.update({'NumberOfNewStatements': new_count})
        class_lexicon_metrics_dict.update({'NumberOfSuperStatements': super_count})

        # print('Class lexicon metrics:', class_lexicon_metrics_dict)
        return class_lexicon_metrics_dict

    @classmethod
    def compute_java_package_metrics(cls, db=None, class_name: str = None):

        # print('ib', entity.ib())
        # package_name = ''
        # Find package: strategy 1
        # for ib in entity.ib():
        #     if ib.find('Package:') != -1:
        #         sp = ib.split(':')
        # print('entity ib', sp[1][1:-1])
        # package_name = sp[1][1:-1]

        # Find package: strategy 2: Dominated strategy
        class_name_list = class_name.split('.')[:-1]
        package_name = '.'.join(class_name_list)
        # print('package_name string', package_name)
        package_list = db.lookup(package_name + '$', 'Package')
        if package_list is None:
            return None
        if len(package_list) == 0:  # if len != 1 return None!
            return None
        package = package_list[0]
        # print('kind:', package.kind())
        # print('Computing package metrics for class: "{0}" in package: "{1}"'.format(class_name, package.longname()))

        # Print info
        # print('package metrics')
        package_metrics = package.metric(package.metrics())
        # print('number of metrics:', len(metrics), metrics)
        # for i, metric in enumerate(metrics.keys()):
        #     print(i + 1, ': ', metric, metrics[metric])

        # print('class metrics')
        # metrics2 = entity.metric(entity.metrics())
        # print('number of metrics:', len(metrics), metrics2)
        # for i, metric2 in enumerate(metrics.keys()):
        #     print(i + 1, ': ', metric2, metrics[metric2])

        #
        # print(package.refs('Definein'))
        # for defin in package.refs('Definein'):
        #     print('kind', defin.ent().kind())
        # print(defin, '-->', defin.ent().ents('Java Define', 'Class'))
        # metrics = entity.metric(defin.ent().metrics())
        # print('number of metrics in file:', len(metrics), metrics)
        # for i, metric in enumerate(metrics.keys()):
        #     print(i + 1, ': ', metric, metrics[metric])

        classes_and_interfaces_list = UnderstandUtility.get_package_clasess_java(package_entity=package)
        # print(classes_and_interfaces_list)
        # quit()

        # 2. Custom package metrics
        # 2.1. PKLOC (15)
        pk_loc_list = list()
        pk_loc_decl_list = list()
        pk_loc_exe_list = list()
        for type_entity in classes_and_interfaces_list:
            pk_loc_list.append(type_entity.metric(['CountLineCode'])['CountLineCode'])
            pk_loc_decl_list.append(type_entity.metric(['CountLineCodeDecl'])['CountLineCodeDecl'])
            pk_loc_exe_list.append(type_entity.metric(['CountLineCodeExe'])['CountLineCodeExe'])

        cls.remove_none_from_lists([pk_loc_list, pk_loc_decl_list, pk_loc_exe_list])

        try:
            package_metrics.update({'AvgLineCodeDecl': sum(pk_loc_decl_list) / len(pk_loc_decl_list)})
            package_metrics.update({'AvgLineCodeExe': sum(pk_loc_exe_list) / len(pk_loc_exe_list)})

            package_metrics.update({'MaxLineCode': max(pk_loc_list)})
            package_metrics.update({'MaxLineCodeDecl': max(pk_loc_decl_list)})
            package_metrics.update({'MaxLineCodeExe': max(pk_loc_exe_list)})

            package_metrics.update({'MinLineCode': min(pk_loc_list)})
            package_metrics.update({'MinLineCodeDecl': min(pk_loc_decl_list)})
            package_metrics.update({'MinLineCodeExe': min(pk_loc_exe_list)})

            package_metrics.update({'SDLineCode': np.std(pk_loc_list)})
            package_metrics.update({'SDLineCodeDecl': np.std(pk_loc_decl_list)})
            package_metrics.update({'SDLineCodeExe': np.std(pk_loc_exe_list)})
        except:
            raise TypeError('Error happen when compute packege metric for class "{0}" and list "{1}"'.format(class_name,
                                                                                                             pk_loc_decl_list))

        # 2.2 PKNOS (15)
        pk_stmt_list = list()
        pk_stmt_decl_list = list()
        pk_stmt_exe_list = list()
        for type_entity in classes_and_interfaces_list:
            pk_stmt_list.append(type_entity.metric(['CountStmt'])['CountStmt'])
            pk_stmt_decl_list.append(type_entity.metric(['CountStmtDecl'])['CountStmtDecl'])
            pk_stmt_exe_list.append(type_entity.metric(['CountStmtExe'])['CountStmtExe'])

        cls.remove_none_from_lists([pk_stmt_list, pk_stmt_decl_list, pk_stmt_exe_list])

        package_metrics.update({'AvgStmt': sum(pk_stmt_decl_list) / len(pk_stmt_decl_list)})
        package_metrics.update({'AvgStmtDecl': sum(pk_stmt_decl_list) / len(pk_stmt_decl_list)})
        package_metrics.update({'AvgStmtExe': sum(pk_stmt_exe_list) / len(pk_stmt_exe_list)})

        package_metrics.update({'MaxStmt': max(pk_stmt_list)})
        package_metrics.update({'MaxStmtDecl': max(pk_stmt_decl_list)})
        package_metrics.update({'MaxStmtExe': max(pk_stmt_exe_list)})

        package_metrics.update({'MinStmt': min(pk_stmt_list)})
        package_metrics.update({'MinStmtDecl': min(pk_stmt_decl_list)})
        package_metrics.update({'MinStmtExe': min(pk_stmt_exe_list)})

        package_metrics.update({'SDStmt': np.std(pk_stmt_list)})
        package_metrics.update({'SDStmtDecl': np.std(pk_stmt_decl_list)})
        package_metrics.update({'SDStmtExe': np.std(pk_stmt_exe_list)})

        # 2.3 PKCC (20)
        pk_cyclomatic_list = list()
        pk_cyclomatic_namm_list = list()

        pk_cyclomatic_strict_list = list()
        pk_cyclomatic_strict_namm_list = list()

        pk_cyclomatic_modified_list = list()
        pk_cyclomatic_modified_namm_list = list()

        pk_essential_list = list()
        pk_essential_namm_list = list()

        for type_entity in classes_and_interfaces_list:
            pk_cyclomatic_list.append(type_entity.metric(['SumCyclomatic'])['SumCyclomatic'])
            pk_cyclomatic_modified_list.append(type_entity.metric(['SumCyclomaticModified'])['SumCyclomaticModified'])
            pk_cyclomatic_strict_list.append(type_entity.metric(['SumCyclomaticStrict'])['SumCyclomaticStrict'])
            pk_essential_list.append(type_entity.metric(['SumEssential'])['SumEssential'])

        cls.remove_none_from_lists(
            [pk_cyclomatic_list, pk_cyclomatic_strict_list, pk_cyclomatic_modified_list, pk_essential_list])

        package_metrics.update({'MinCyclomatic': min(pk_cyclomatic_list)})
        package_metrics.update({'MinCyclomaticModified': min(pk_cyclomatic_modified_list)})
        package_metrics.update({'MinCyclomaticStrict': min(pk_cyclomatic_strict_list)})
        package_metrics.update({'MinEssential': min(pk_essential_list)})

        package_metrics.update({'SDCyclomatic': np.std(pk_cyclomatic_list)})
        package_metrics.update({'SDCyclomaticModified': np.std(pk_cyclomatic_modified_list)})
        package_metrics.update({'SDCyclomaticStrict': np.std(pk_cyclomatic_strict_list)})
        package_metrics.update({'SDEssential': np.std(pk_essential_list)})

        # 2.4 PKNESTING (4)
        pk_nesting_list = list()
        for type_entity in classes_and_interfaces_list:
            pk_nesting_list.append(type_entity.metric(['MaxNesting'])['MaxNesting'])

        cls.remove_none_from_lists([pk_nesting_list])

        package_metrics.update({'MinNesting': min(pk_nesting_list)})
        package_metrics.update({'AvgNesting': sum(pk_nesting_list) / len(pk_nesting_list)})
        package_metrics.update({'SDNesting': np.std(pk_nesting_list)})

        # 2.5
        # Other Size/Count metrics (understand built-in metrics)

        # PKNOMNAMM: Package number of not accessor or mutator methods
        j_code_odor = JCodeOdorMetric()
        pk_not_accessor_and_mutator_methods_list = list()
        pk_accessor_and_mutator_methods_list = list()
        for type_entity in classes_and_interfaces_list:
            pk_not_accessor_and_mutator_methods_list.append(j_code_odor.NOMNAMM(type_entity))
            pk_accessor_and_mutator_methods_list.append(j_code_odor.NOMAMM(type_entity))

        cls.remove_none_from_lists([pk_not_accessor_and_mutator_methods_list, pk_accessor_and_mutator_methods_list])

        package_metrics.update({'PKNOMNAMM': sum(pk_not_accessor_and_mutator_methods_list)})

        # 2.6 Visibility metrics
        # Other Visibility metrics metrics (understand built-in metrics)
        package_metrics.update({'PKNOAMM': sum(pk_accessor_and_mutator_methods_list)})
        # To add other visibility metrics

        # 2.7 Inheritance metrics
        package_metrics.update({'PKNOI': len(UnderstandUtility.get_package_interfaces_java(package_entity=package))})
        package_metrics.update(
            {'PKNOAC': len(UnderstandUtility.get_package_abstract_class_java(package_entity=package))})

        # print(len(package_metrics))
        # print(package_metrics)
        return package_metrics

    @classmethod
    def compute_java_project_metrics(cls, db):
        project_metrics = db.metric(db.metrics())
        # print('number of metrics:', len(project_metrics),  project_metrics)
        # for i, metric in enumerate( project_metrics.keys()):
        #     print(i + 1, ': ',  metric,  project_metrics[metric])

        # print(project_metrics)  # Print Understand built-in metrics

        # 2 Custom project metrics
        files = UnderstandUtility.get_project_files_java(db=db)
        # 2.1 PJLOC (30)
        pj_loc_list = list()
        pj_loc_decl_list = list()
        pj_loc_exe_list = list()

        pj_stmt_list = list()
        pj_stmt_decl_list = list()
        pj_stmt_exe_list = list()

        for file_entity in files:
            pj_loc_list.append(file_entity.metric(['CountLineCode'])['CountLineCode'])
            pj_loc_decl_list.append(file_entity.metric(['CountLineCodeDecl'])['CountLineCodeDecl'])
            pj_loc_exe_list.append(file_entity.metric(['CountLineCodeExe'])['CountLineCodeExe'])

            pj_stmt_list.append(file_entity.metric(['CountStmt'])['CountStmt'])
            pj_stmt_decl_list.append(file_entity.metric(['CountStmtDecl'])['CountStmtDecl'])
            pj_stmt_exe_list.append(file_entity.metric(['CountStmtExe'])['CountStmtExe'])

        cls.remove_none_from_lists([pj_loc_list, pj_loc_decl_list, pj_loc_exe_list,
                                    pj_stmt_list, pj_stmt_decl_list, pj_stmt_exe_list])

        project_metrics.update({'AvgLineCodeDecl': sum(pj_loc_decl_list) / len(pj_loc_decl_list)})
        project_metrics.update({'AvgLineCodeExe': sum(pj_loc_exe_list) / len(pj_loc_exe_list)})

        project_metrics.update({'MaxLineCode': max(pj_loc_list)})
        project_metrics.update({'MaxLineCodeDecl': max(pj_loc_decl_list)})
        project_metrics.update({'MaxLineCodeExe': max(pj_loc_exe_list)})

        project_metrics.update({'MinLineCode': min(pj_loc_list)})
        project_metrics.update({'MinLineCodeDecl': min(pj_loc_decl_list)})
        project_metrics.update({'MinLineCodeExe': min(pj_loc_exe_list)})

        project_metrics.update({'SDLineCode': np.std(pj_loc_list)})
        project_metrics.update({'SDLineCodeDecl': np.std(pj_loc_decl_list)})
        project_metrics.update({'SDLineCodeExe': np.std(pj_loc_exe_list)})

        # 2.2. PJNOST (15)
        project_metrics.update({'AvgStmt': sum(pj_stmt_list) / len(pj_stmt_list)})
        project_metrics.update({'AvgStmtDecl': sum(pj_stmt_decl_list) / len(pj_stmt_decl_list)})
        project_metrics.update({'AvgStmtExe': sum(pj_stmt_exe_list) / len(pj_stmt_exe_list)})

        project_metrics.update({'MaxStmt': max(pj_stmt_list)})
        project_metrics.update({'MaxStmtDecl': max(pj_stmt_decl_list)})
        project_metrics.update({'MaxStmtExe': max(pj_stmt_exe_list)})

        project_metrics.update({'MinStmt': min(pj_stmt_list)})
        project_metrics.update({'MinStmtDecl': min(pj_stmt_decl_list)})
        project_metrics.update({'MinStmtExe': min(pj_stmt_exe_list)})

        project_metrics.update({'SDStmt': np.std(pj_stmt_list)})
        project_metrics.update({'SDStmtDecl': np.std(pj_stmt_decl_list)})
        project_metrics.update({'SDStmtExe': np.std(pj_stmt_exe_list)})

        # 2.3 Other Count/Size metrics
        packages = db.ents('Java Package')
        # print('number of packages', len(packages))
        project_metrics.update({'NumberOfPackages': len(packages)})

        j_code_odor = JCodeOdorMetric()
        pj_number_of_method_namm = 0
        for class_ in UnderstandUtility.get_project_classes_java(db=db):
            pj_number_of_method_namm += j_code_odor.NOMNAMM(class_)
        project_metrics.update({'PJNOMNAMM': pj_number_of_method_namm})

        # 2.4 PJCC (20): Project cyclomatic complexity
        pj_cyclomatic_list = list()
        pj_cyclomatic_namm_list = list()

        pj_cyclomatic_strict_list = list()
        pj_cyclomatic_strict_namm_list = list()

        pj_cyclomatic_modified_list = list()
        pj_cyclomatic_modified_namm_list = list()

        pj_essential_list = list()
        pj_essential_namm_list = list()

        for type_entity in files:
            pj_cyclomatic_list.append(type_entity.metric(['SumCyclomatic'])['SumCyclomatic'])
            pj_cyclomatic_modified_list.append(type_entity.metric(['SumCyclomaticModified'])['SumCyclomaticModified'])
            pj_cyclomatic_strict_list.append(type_entity.metric(['SumCyclomaticStrict'])['SumCyclomaticStrict'])
            pj_essential_list.append(type_entity.metric(['SumEssential'])['SumEssential'])

        cls.remove_none_from_lists([pj_cyclomatic_list, pj_cyclomatic_strict_list,
                                    pj_cyclomatic_modified_list, pj_essential_list])

        project_metrics.update({'SumCyclomatic': sum(pj_cyclomatic_list)})
        project_metrics.update({'SumCyclomaticModified': sum(pj_cyclomatic_modified_list)})
        project_metrics.update({'SumCyclomaticStrict': sum(pj_cyclomatic_strict_list)})
        project_metrics.update({'SumEssential': sum(pj_essential_list)})

        project_metrics.update({'MaxCyclomatic': max(pj_cyclomatic_list)})
        project_metrics.update({'MaxCyclomaticModified': max(pj_cyclomatic_modified_list)})
        project_metrics.update({'MaxCyclomaticStrict': max(pj_cyclomatic_strict_list)})
        project_metrics.update({'MaxEssential': max(pj_essential_list)})

        project_metrics.update({'AvgCyclomatic': sum(pj_cyclomatic_list) / len(pj_cyclomatic_list)})
        project_metrics.update(
            {'AvgCyclomaticModified': sum(pj_cyclomatic_modified_list) / len(pj_cyclomatic_modified_list)})
        project_metrics.update({'AvgCyclomaticStrict': sum(pj_cyclomatic_strict_list) / len(pj_cyclomatic_strict_list)})
        project_metrics.update({'AvgEssential': sum(pj_essential_list) / len(pj_essential_list)})

        project_metrics.update({'MinCyclomatic': min(pj_cyclomatic_list)})
        project_metrics.update({'MinCyclomaticModified': min(pj_cyclomatic_modified_list)})
        project_metrics.update({'MinCyclomaticStrict': min(pj_cyclomatic_strict_list)})
        project_metrics.update({'MinEssential': min(pj_essential_list)})

        project_metrics.update({'SDCyclomatic': np.std(pj_cyclomatic_list)})
        project_metrics.update({'SDCyclomaticModified': np.std(pj_cyclomatic_modified_list)})
        project_metrics.update({'SDCyclomaticStrict': np.std(pj_cyclomatic_strict_list)})
        project_metrics.update({'SDEssential': np.std(pj_essential_list)})

        # 2.4 PKNESTING (4)
        pj_nesting_list = list()
        for type_entity in files:
            pj_nesting_list.append(type_entity.metric(['MaxNesting'])['MaxNesting'])

        cls.remove_none_from_lists([pj_nesting_list])

        project_metrics.update({'MinNesting': min(pj_nesting_list)})
        project_metrics.update({'AvgNesting': sum(pj_nesting_list) / len(pj_nesting_list)})
        project_metrics.update({'SDNesting': np.std(pj_nesting_list)})

        # 3 Inheritance metrics
        project_metrics.update({'PJNOI': len(UnderstandUtility.get_project_interfaces_java(db=db))})
        project_metrics.update({'PJNAC': len(UnderstandUtility.get_project_abstract_classes_java(db=db))})

        return project_metrics

    @classmethod
    def remove_none_from_lists(cls, lists: list = None):
        for i, list_ in enumerate(lists):
            if len(list_) == 0:
                list_.append(0)
                warnings.warn('Empty list passed!')
            # else:
            #     list_ = [i for i in list_ if i is not None]
            #     if len(list_) == 0:
            #         list_.append(0)
            #         raise ValueError('Required data for systematic metric computation is not enough!')


# ------------------------------------------------------------------------
class PreProcess:
    """
    Writes all metrics in a csv file and performs preprocessing
    """

    # Dataset creation API
    @classmethod
    def create_understand_database_from_project(cls, root_path='sf110_without_test/'):
        # {0}: understand_db_directory, {1}: understand_db_name, {2}: project_root_directory
        cmd = 'und create -db {0}{1}.udb -languages java add {2} analyze -all'
        # projects = [x[0] for x in os.walk(root_path)]
        projects = [name for name in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, name))]
        for project_ in projects:
            command_ = cmd.format(root_path, project_, root_path + project_)
            # print('executing command {0}'.format(command_))
            # returned_value_in_byte = subprocess.check_output(command_, shell=True)
            os.system('cmd /c "{0}"'.format(command_))
            # os.system('cmd / k "{0}"'.format(command_))

    @classmethod
    def extract_project_classes_all(cls, udbs_path, class_list_csv_path_root=r'class_list_csvs/'):
        files = [f for f in os.listdir(udbs_path) if os.path.isfile(os.path.join(udbs_path, f))]
        for f in files:
            # print('processing understand db file {0}:'.format(f))
            db = und.open(os.path.join(udbs_path, f))
            cls.write_project_classes(project_name=f[:-4], db=db, csv_path=class_list_csv_path_root + f[:-4] + '.csv')
            db.close()
            # print('processing understand db file {0} was finished'.format(f))

    @classmethod
    def extract_project_classes(cls, db):
        classes_list = UnderstandUtility.get_project_classes_longnames_java(db=db)
        # print('@understand', len(set(classes_list)), set(classes_list))
        return classes_list

    @classmethod
    def write_project_classes(cls, project_name: str = None, db=None, csv_path: str = None):
        classes = cls.extract_project_classes(db=db)
        df = pd.DataFrame(columns=['Project', 'Class', 'Line', 'Branch', 'Mutation', 'Output', 'Exceptions', 'Tests'])
        df['Project'] = [project_name for i in range(0, len(classes))]
        df['Class'] = classes
        df.to_csv(csv_path, index=False)

    @classmethod
    def read_project_classes(cls, db=None, classes_names_list: list = None):
        class_entities = list()
        for class_name_ in classes_names_list:
            # Find relevant class entity
            class_entity_ = UnderstandUtility.get_class_entity_by_name(db=db, class_name=class_name_)
            if class_entity_ is not None:
                method_list = UnderstandUtility.get_method_of_class_java2(db=db, class_entity=class_entity_)
                if method_list is not None:
                    class_entities.append(class_entity_)
                else:
                    # We do not need a class without any method!
                    warnings.warn(
                        'Requested class entity with name "{0}" does not have any method!'.format(class_name_))
            else:
                # if class not found it may be an enum, or interface so we simply ignore it for metric computation
                warnings.warn(
                    'Requested class entity with name "{0}" was not found int the project!'.format(class_name_))
        return class_entities

    @classmethod
    def extract_metrics_and_coverage_all(cls, udbs_path: str = r'sf110_without_test',
                                         class_list_csv_path: str = r'runtime_result/evosuit160_sf110_result_html_with_project.csv',
                                         csvs_path: str = r'sf110_csvs_without_test_e3/',
                                         ):
        df = pd.read_csv(class_list_csv_path, delimiter=',', index_col=False)
        files = [f for f in os.listdir(udbs_path) if os.path.isfile(os.path.join(udbs_path, f))]

        t = list()
        p = list()
        for i, f in enumerate(files):
            # print('processing understand db file {0}:'.format(f))
            db = und.open(os.path.join(udbs_path, f))

            # cls.check_compute_metrics_by_class_list(project_name=f[:-4], database=db, class_list=df, csv_path=csvs_path)
            # t.append(threading.Thread(target=cls.check_compute_metrics_by_class_list, args=(f[:-4], db, df, csvs_path, )))
            # t[i].start()

            # p.append(multiprocessing.Process(target=cls.check_compute_metrics_by_class_list, args=(f[:-4], db, df, csvs_path, )))
            # p[i].start()

            cls.compute_metrics_by_class_list(project_name=f[:-4], database=db, class_list=df, csv_path=csvs_path)
            db.close()
            # print('processing understand db file {0} was finished'.format(f))

    @classmethod
    def check_compute_metrics_by_class_list(cls, db=None, class_list=None, csv_path=None):
        class_entities = cls.read_project_classes(db=db, classes_names_list=class_list)
        # print('Number of classes is: {1}'.format(len(class_entities)))

        columns = ['Project', 'NumberOfClass']
        columns.extend(TestabilityMetrics.get_all_metrics_names())

        dummy_data = [0 for i in range(0, len(columns) - 2)]
        dummy_data.insert(0, 'project_name')
        dummy_data.insert(1, len(class_entities))

        df = pd.DataFrame(data=[dummy_data], columns=columns)
        # print(df)
        # print(columns)
        df.to_csv(csv_path + '.csv', index=False, )

    @classmethod
    def compute_metrics_by_class_list(cls, db=None, class_list=None):
        all_class_metrics_value = list()

        # print('Calculating project metrics')
        # project_metrics_dict = TestabilityMetrics.compute_java_project_metrics(db=database)
        # if project_metrics_dict is None:
        #     raise TypeError('No project metrics for project {} was found!'.format(project_name))

        class_entities = cls.read_project_classes(db=db, classes_names_list=class_list, )
        for class_entity in class_entities:
            one_class_metrics_value = [class_entity.longname()]
            # print('Calculating package metrics')
            package_metrics_dict = TestabilityMetrics.compute_java_package_metrics(db=db,
                                                                                   class_name=class_entity.longname())
            if package_metrics_dict is None:
                # raise TypeError('No package metric for item {} was found'.format(class_entity.longname()))
                continue
            # print('Calculating class lexicon metrics')
            class_lexicon_metrics_dict = TestabilityMetrics.compute_java_class_metrics_lexicon(db=db,
                                                                                               entity=class_entity)
            if class_lexicon_metrics_dict is None:
                # raise TypeError('No class lexicon metric for item {} was found'.format(class_entity.longname()))
                continue
            # print('Calculating class ordinary metrics')
            class_ordinary_metrics_dict = TestabilityMetrics.compute_java_class_metrics2(db=db,
                                                                                         entity=class_entity)
            if class_ordinary_metrics_dict is None:
                # raise TypeError('No class ordinary metric for item {} was found'.format(class_entity.longname()))
                continue

            # Write project_metrics_dict
            # for metric_name in TestabilityMetrics.get_project_metrics_names():
            #     one_class_metrics_value.append(project_metrics_dict[metric_name])

            # Write package_metrics_dict
            for metric_name in TestabilityMetrics.get_package_metrics_names():
                one_class_metrics_value.append(package_metrics_dict[metric_name])

            # Write class_lexicon_metrics_dict
            for metric_name in TestabilityMetrics.get_class_lexicon_metrics_names():
                one_class_metrics_value.append(class_lexicon_metrics_dict[metric_name])

            # Write class_ordinary_metrics_dict
            for metric_name in TestabilityMetrics.get_class_ordinary_metrics_names():
                one_class_metrics_value.append(class_ordinary_metrics_dict[metric_name])

            all_class_metrics_value.append(one_class_metrics_value)

        columns = ['Class']
        columns.extend(TestabilityMetrics.get_all_metrics_names())
        df = pd.DataFrame(data=all_class_metrics_value, columns=columns)
        # print('df for class {0} with shape {1}'.format(project_name, df.shape))
        # df.to_csv(csv_path + project_name + '.csv', index=False)
        return df

    @classmethod
    def compute_metrics_for_single_class(cls, class_name, und_path, result_csv):
        all_class_metrics_value = list()
        database_ = und.open(und_path)
        class_entity = UnderstandUtility.get_class_entity_by_name(db=database_, class_name=class_name)

        one_class_metrics_value = [class_entity.longname()]
        # print('Calculating package metrics')
        package_metrics_dict = TestabilityMetrics.compute_java_package_metrics(db=database_,
                                                                               class_name=class_entity.longname())
        if package_metrics_dict is None:
            raise TypeError('No package metric for item {} was found'.format(class_entity.longname()))

        # print('Calculating class lexicon metrics')
        class_lexicon_metrics_dict = TestabilityMetrics.compute_java_class_metrics_lexicon(db=database_,
                                                                                           entity=class_entity)
        if class_lexicon_metrics_dict is None:
            raise TypeError('No class lexicon metric for item {} was found'.format(class_entity.longname()))
        # print('Calculating class ordinary metrics')
        class_ordinary_metrics_dict = TestabilityMetrics.compute_java_class_metrics2(db=database_,
                                                                                     entity=class_entity)
        if class_ordinary_metrics_dict is None:
            raise TypeError('No class ordinary metric for item {} was found'.format(class_entity.longname()))
        # Write package_metrics_dict
        for metric_name in TestabilityMetrics.get_package_metrics_names():
            one_class_metrics_value.append(package_metrics_dict[metric_name])
        # Write class_lexicon_metrics_dict
        for metric_name in TestabilityMetrics.get_class_lexicon_metrics_names():
            one_class_metrics_value.append(class_lexicon_metrics_dict[metric_name])
        # Write class_ordinary_metrics_dict
        for metric_name in TestabilityMetrics.get_class_ordinary_metrics_names():
            one_class_metrics_value.append(class_ordinary_metrics_dict[metric_name])

        all_class_metrics_value.append(one_class_metrics_value)
        columns = ['Class']
        columns.extend(TestabilityMetrics.get_all_metrics_names())
        columns2 = [metrics.metrics_names.metric_map[c_] for c_ in columns[:-1]]
        columns2.append('NOCLINFILE')
        df = pd.DataFrame(data=all_class_metrics_value, columns=columns2)
        df.drop(columns=['NOCLINFILE'], inplace=True)
        df['CSNOM'] = df['CSNOIM'] + df['CSNOSM']
        # df.to_csv(result_csv, index=False)
        database_.close()
        return df


class TestabilityModel(object):
    def __init__(self, df_path: str = None):
        self.df = pd.read_csv(df_path, delimiter=',', index_col=False)
        self.X_train1, self.X_test1, self.y_train, self.y_test = train_test_split(self.df.iloc[:, 1:-1],
                                                                                  self.df.iloc[:, -1],
                                                                                  test_size=0.25,
                                                                                  random_state=117,
                                                                                  )
        """
        # ---------------------------------------
        # -- Feature selection (For DS2)
        selector = feature_selection.SelectKBest(feature_selection.f_regression, k=15)
        # clf = linear_model.LassoCV(eps=1e-3, n_alphas=100, normalize=True, max_iter=5000, tol=1e-4)
        # clf.fit(self.X_train1, self.y_train)
        # importance = np.abs(clf.coef_)
        # print('importance', importance)
        # clf = RandomForestRegressor()
        # selector = feature_selection.SelectFromModel(clf, prefit=False, norm_order=2, max_features=20, threshold=None)
        selector.fit(self.X_train1, self.y_train)

        # Get columns to keep and create new dataframe with only selected features
        cols = selector.get_support(indices=True)
        self.X_train1 = self.X_train1.iloc[:, cols]
        self.X_test1 = self.X_test1.iloc[:, cols]
        print('Selected columns by feature selection:', self.X_train1.columns)
        # quit()
        # -- End of feature selection
        """

        # ---------------------------------------
        # Standardization
        # self.scaler = preprocessing.RobustScaler(with_centering=True, with_scaling=True, unit_variance=True)
        # self.scaler = preprocessing.StandardScaler()
        self.scaler = QuantileTransformer(n_quantiles=1000, random_state=11)
        self.scaler.fit(self.X_train1)
        self.X_train = self.scaler.transform(self.X_train1)
        self.X_test = self.scaler.transform(self.X_test1)
        # quit()

    def inference(self, model=None, model_path=None, df_predict_data=None):
        if model is None:
            model = joblib.load(model_path)

        # df_predict_data = pd.read_csv(predict_data_path, delimiter=',', index_col=False)
        X_test1 = df_predict_data.iloc[:, 1:]
        X_test = self.scaler.transform(X_test1)
        y_pred = model.predict(X_test)

        df_new = pd.DataFrame(df_predict_data.iloc[:, 0], columns=['Class'])
        df_new['PredictedTestability'] = list(y_pred)

        # print(df_new)
        # df_new.to_csv(r'dataset06/refactored01010_predicted_testability.csv', index=True, index_label='Row')
        return df_new['PredictedTestability'].mean()


# Test driver
def main(project_path):
    """
    A demo of using testability_prediction module to measure testability quality attribute with machine learning
    """
    db = und.open(project_path)
    p = PreProcess()
    classes_longnames_list = p.extract_project_classes(db=db)
    df = p.compute_metrics_by_class_list(db=db, class_list=classes_longnames_list)
    db.close()
    model = TestabilityModel(df_path=r'../metrics/data_model/DS07012.csv')
    testability_ = model.inference(model_path='../metrics/data_model/VR1_DS1.joblib', df_predict_data=df)
    # print('testability=', testability_)
    return testability_


# Test module
if __name__ == '__main__':
    # project_path_ = r'../benchmark_projects/ganttproject/biz.ganttproject.core/biz.ganttproject.core.und'  # T=0.5253
    # project_path_ = r'../benchmark_projects/JSON/JSON.und'  # T=0.4531
    project_path_ = r'D:/IdeaProjects/JSON20201115/JSON.und'  # T=0.4749
    # project_path_ = r'D:/IdeaProjects/jvlt-1.3.2/src.und'  # T=0.4212
    main(project_path_)
