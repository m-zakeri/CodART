"""

## Introduction

This module contains light-weight version of testability prediction script (with 68 metrics)
to be used in refactoring process in addition to QMOOD metrics.

## Changelog
### v0.2.3
- Remove dependency to metrics_jcode_odor
### v0.2.2
- Add scikit-learn 1 compatibility


## Reference
[1] ADAFEST paper
[2] TsDD paper


"""

__version__ = '0.2.3'
__author__ = 'Morteza Zakeri'

import os
import pandas as pd
import joblib
from joblib import Parallel, delayed

import understand as und

from codart import config
from codart.metrics import metrics_names
from codart.metrics.metrics_coverability import UnderstandUtility

# scaler1 = joblib.load(os.path.join(os.path.dirname(__file__), 'data_model/DS07510.joblib'))
# model5 = joblib.load(os.path.join(os.path.dirname(__file__), 'data_model/VR1_DS5.joblib'))
# model_branch = joblib.load(os.path.join(os.path.dirname(__file__), 'sklearn_models6/VR6_DS5_branch.joblib'))
# model_line = joblib.load(os.path.join(os.path.dirname(__file__), 'sklearn_models6/VR6_DS5_line.joblib'))


class TestabilityMetrics:
    """

    Compute all required metrics for computing Coverageability and testability.

    """

    @classmethod
    def get_package_metrics_names(cls) -> list:
        return metrics_names.package_metrics_names_primary

    @classmethod
    def get_class_lexicon_metrics_names(cls) -> list:
        return metrics_names.class_lexicon_metrics_names

    @classmethod
    def get_class_ordinary_metrics_names(cls) -> list:
        return metrics_names.class_ordinary_metrics_names_primary

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
        # for metric_name in metrics.metrics_names.project_metrics_names_primary:
        #     primary_metrics_names.append('PJ_' + metric_name)
        for metric_name in metrics_names.package_metrics_names_primary:
            primary_metrics_names.append('PK_' + metric_name)
        for metric_name in metrics_names.class_lexicon_metrics_names:
            primary_metrics_names.append('CSLEX_' + metric_name)
        for metric_name in metrics_names.class_ordinary_metrics_names_primary:
            primary_metrics_names.append('CSORD_' + metric_name)
        return primary_metrics_names

    @classmethod
    def compute_java_package_metrics(cls, db=None, entity=None):
        """
        Find package: strategy 2: Dominated strategy

        """
        #
        class_name = entity.longname()
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

        metric_list = ['CountLineCode', 'CountStmt', 'CountDeclClassMethod', 'CountDeclClassVariable',
                       'CountDeclInstanceMethod', 'CountDeclInstanceVariable', 'CountDeclClass', 'CountDeclFile',
                       'SumCyclomatic', 'MaxNesting', 'CountDeclMethodDefault', 'CountDeclMethodPrivate',
                       'CountDeclMethodProtected', 'CountDeclMethodPublic', ]
        package_metrics = package.metric(metric_list)
        classes_and_interfaces_list = package.ents('Contain', 'Java Type ~Unknown ~Unresolved ~Jar ~Library')

        # PKNOMNAMM: Package number of not accessor or mutator methods
        pk_accessor_and_mutator_methods_list = list()
        for type_entity in classes_and_interfaces_list:
            pk_accessor_and_mutator_methods_list.append(UnderstandUtility.NOMAMM(type_entity))
        pk_accessor_and_mutator_methods_list = list(filter(None, pk_accessor_and_mutator_methods_list))
        package_metrics.update({'PKNOAMM': sum(pk_accessor_and_mutator_methods_list)})

        pknoi = len(UnderstandUtility.get_package_interfaces_java(package_entity=package))
        pknoac = len(UnderstandUtility.get_package_abstract_class_java(package_entity=package))
        package_metrics.update({'PKNOI': pknoi})
        package_metrics.update({'PKNOAC': pknoac})

        # print('package metrics', len(package_metrics), package_metrics)
        return package_metrics

    @classmethod
    def compute_java_class_metrics_lexicon(cls, entity=None):
        """
        Args:

            entity (understand.Ent):

        Returns:

             dict: class-level metrics

        """

        class_lexicon_metrics_dict = dict()
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
        # print(entity.longname())
        lexeme = entity.lexer(show_inactive=False).first()
        while lexeme is not None:
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
            lexeme = lexeme.next()

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

        # print('class lexicon metrics dict', len(class_lexicon_metrics_dict), class_lexicon_metrics_dict)
        return class_lexicon_metrics_dict

    @classmethod
    def compute_java_class_metrics2(cls, db=None, entity=None):
        """
        Strategy #2: Take a list of all classes and search for target class
        Which strategy is used for our final setting? I do not know!

        Args:
            db (understand.Db):

            entity (understand.Ent):

        Returns:

            dict: Class-level metrics

        """

        method_list = UnderstandUtility.get_method_of_class_java2(db=db, class_name=entity.longname())
        if method_list is None:
            # raise TypeError('method_list is none for class "{}"'.format(entity.longname()))
            print('method_list is none for class "{}"'.format(entity.longname()))
            return None

        metrics_list = ['CountLineCode', 'CountStmt', 'CountDeclClassMethod', 'CountDeclClassVariable',
                        'CountDeclInstanceMethod', 'CountDeclInstanceVariable', 'SumCyclomatic', 'MaxNesting',
                        'PercentLackOfCohesion', 'CountClassCoupled', 'CountDeclMethodDefault',
                        'CountDeclMethodPrivate',
                        'CountDeclMethodProtected', 'CountDeclMethodPublic', 'MaxInheritanceTree', 'CountClassDerived',
                        'CountClassBase', ]
        class_metrics = entity.metric(metrics_list)

        parameters_length_list = list()
        for method in method_list:
            params = method.parameters().split(',')
            if len(params) == 1:
                if params[0] == ' ' or params[0] == '' or params[0] is None:
                    parameters_length_list.append(0)
                else:
                    parameters_length_list.append(1)
            else:
                parameters_length_list.append(len(params))
        parameters_length_list = list(filter(None, parameters_length_list))
        class_metrics.update({'SumCSNOP': sum(parameters_length_list)})

        class_metrics.update({'RFC': UnderstandUtility.RFC(class_name=entity)})
        class_metrics.update({'FANIN': UnderstandUtility.FANIN(db=db, class_entity=entity)})
        class_metrics.update({'FANOUT': UnderstandUtility.FANOUT(db=db, class_entity=entity)})

        class_metrics.update({'ATFD': UnderstandUtility.ATFD(db=db, class_entity=entity)})  # Not implement

        class_metrics.update({'CFNAMM': UnderstandUtility.CFNAMM_Class(class_name=entity)})
        class_metrics.update({'DAC': UnderstandUtility.get_data_abstraction_coupling(db=db, class_entity=entity)})
        class_metrics.update({'NumberOfMethodCalls': UnderstandUtility.number_of_method_call(class_entity=entity)})

        # Visibility metrics
        # Understand built-in metrics plus one custom metric.
        class_metrics.update({'CSNOAMM': UnderstandUtility.NOMAMM(class_entity=entity)})

        # Inheritance metrics
        class_metrics.update({'NIM': UnderstandUtility.NIM(class_name=entity)})
        class_metrics.update({'NMO': UnderstandUtility.NMO(class_name=entity)})

        class_metrics.update({'NOII': UnderstandUtility.NOII(db=db)})  # Not implemented

        class_count_path_list = list()
        class_knots_list = list()
        for method in method_list:
            class_count_path_list.append(method.metric(['CountPath'])['CountPath'])
            class_knots_list.append(method.metric(['Knots'])['Knots'])
        class_count_path_list = list(filter(None, class_count_path_list))
        class_metrics.update({'SumCountPath': sum(class_count_path_list)})
        class_knots_list = list(filter(None, class_knots_list))
        class_metrics.update({'SumKnots': sum(class_knots_list)})

        class_metrics.update({'NumberOfDepends': len(entity.depends())})
        class_metrics.update({'NumberOfDependsBy': len(entity.dependsby())})
        class_metrics.update({'NumberOfMethods': class_metrics['CountDeclInstanceMethod'] +
                                                 class_metrics['CountDeclClassMethod']})

        # print('class metrics', len(class_metrics), class_metrics)
        return class_metrics


def do(class_entity_long_name, project_db_path):
    import understand as und
    db = und.open(project_db_path)
    class_entity = UnderstandUtility.get_class_entity_by_name(class_name=class_entity_long_name, db=db)
    one_class_metrics_value = [class_entity.longname()]

    # print('Calculating package metrics')
    package_metrics_dict = TestabilityMetrics.compute_java_package_metrics(db=db, entity=class_entity)
    if package_metrics_dict is None or len(package_metrics_dict) == 0:
        return None

    # print('Calculating class lexicon metrics')
    class_lexicon_metrics_dict = TestabilityMetrics.compute_java_class_metrics_lexicon(entity=class_entity)
    if class_lexicon_metrics_dict is None or len(class_lexicon_metrics_dict) == 0:
        return None

    # print('Calculating class ordinary metrics')
    class_ordinary_metrics_dict = TestabilityMetrics.compute_java_class_metrics2(db=db, entity=class_entity)
    if class_ordinary_metrics_dict is None or len(class_ordinary_metrics_dict) == 0:
        return None

    one_class_metrics_value.extend([package_metrics_dict[metric_name] for
                                    metric_name in TestabilityMetrics.get_package_metrics_names()])

    one_class_metrics_value.extend([class_lexicon_metrics_dict[metric_name] for
                                    metric_name in TestabilityMetrics.get_class_lexicon_metrics_names()])

    one_class_metrics_value.extend([class_ordinary_metrics_dict[metric_name] for
                                    metric_name in TestabilityMetrics.get_class_ordinary_metrics_names()])

    db.close()
    del db
    # print(one_class_metrics_value)
    # quit()
    return one_class_metrics_value


# ------------------------------------------------------------------------
class PreProcess:
    """

    Writes all metrics in a csv file and performs preprocessing

    """

    @classmethod
    def compute_metrics_by_class_list(cls, project_db_path, n_jobs):
        """


        """

        # class_entities = cls.read_project_classes(db=db, classes_names_list=class_list, )
        # print(project_db_path)
        db = und.open(project_db_path)
        class_list = UnderstandUtility.get_project_classes_longnames_java(db=db)
        db.close()
        # del db

        if n_jobs == 0:  # Sequential computing
            res = [do(class_entity_long_name, project_db_path) for class_entity_long_name in class_list]
        else:  # Parallel computing
            res = Parallel(n_jobs=n_jobs, )(
                delayed(do)(class_entity_long_name, project_db_path) for class_entity_long_name in class_list
            )
        res = list(filter(None, res))

        columns = ['Class']
        columns.extend(TestabilityMetrics.get_all_primary_metrics_names())
        df = pd.DataFrame(data=res, columns=columns)
        # print('df for class {0} with shape {1}'.format(project_name, df.shape))
        # df.to_csv(csv_path + project_name + '.csv', index=False)
        # print(df)
        return df


class TestabilityModel:
    """

    Testability prediction model

    """

    def __init__(self, ):
        self.scaler = scaler1
        self.model = model5
        self.model_branch = model_branch
        self.model_line = model_line

    def inference(self, df_predict_data=None, verbose=False, log_path=None):
        df_predict_data = df_predict_data.fillna(0)
        X_test1 = df_predict_data.iloc[:, 1:]
        X_test = self.scaler.transform(X_test1)
        y_pred = self.model.predict(X_test)

        y_pred_branch = self.model_branch.predict(X_test)
        y_pred_line = self.model_line.predict(X_test)

        df_new = pd.DataFrame(df_predict_data.iloc[:, 0], columns=['Class'])
        df_new['PredictedTestability'] = list(y_pred)

        df_new['BranchCoverage'] = list(y_pred_branch)
        df_new['LineCoverage'] = list(y_pred_line)

        if verbose:
            self.export_class_testability_values(df=df_new, log_path=log_path)

        return df_new['PredictedTestability'].sum()  # Return sum instead mean

    @classmethod
    def export_class_testability_values(cls, df=None, log_path=None):
        if log_path is None:
            log_path = os.path.join(
                config.PROJECT_LOG_DIR,
                f'classes_testability2_for_problem_{config.PROBLEM}.csv')
        config.logger.info(log_path)
        config.logger.info(f'count classes testability2\t {df["PredictedTestability"].count()}')
        config.logger.info(f'minimum testability2\t {df["PredictedTestability"].min()}')
        config.logger.info(f'maximum testability2\t {df["PredictedTestability"].max()}')
        config.logger.info(f'variance testability2\t {df["PredictedTestability"].var()}')
        config.logger.info(f'sum classes testability2\t, {df["PredictedTestability"].sum()}')
        config.logger.info('-' * 50)

        df.to_csv(log_path, index=False)


# API
def main(project_db_path, initial_value=1.0, verbose=False, log_path=None):
    """

    testability_prediction module API

    """

    df = PreProcess().compute_metrics_by_class_list(
        project_db_path,
        n_jobs=0  # n_job must be set to number of CPU cores, use zero for non-parallel computing of metrics
    )
    testability_ = TestabilityModel().inference(df_predict_data=df, verbose=verbose, log_path=log_path)
    # print('testability=', testability_)
    return round(testability_ / initial_value, 5)


# Test module
if __name__ == '__main__':
    # project_path_ = r'../benchmark_projects/ganttproject/biz.ganttproject.core/biz.ganttproject.core.und'  # T=0.5253
    # project_path_ = r'../benchmark_projects/JSON/JSON.und'  # T=0.4531
    # project_path_ = r'D:/IdeaProjects/JSON20201115/JSON20201115.und'  # T=0.4749
    # project_path_ = r'D:/IdeaProjects/jvlt-1.3.2/src.und'  # T=0.3997
    print(f"UDB path: {config.UDB_PATH}")
    for i in range(0, 1):
        print('mean testability2 normalize by 1\t', main(config.UDB_PATH, initial_value=1.0, verbose=False))
