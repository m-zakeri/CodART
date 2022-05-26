"""
This script implements machine learning models
for predicting testability for IEEE TSE paper revision 2

T[X] = C(X)/ Effort(X)

Model 1: DecisionTreeRegressor
Model 2: RandomForestRegressor
Model 3: GradientBoostingRegressor
Model 4: HistGradientBoostingRegressor
Model 5: SGDRegressor
Model 6: MLPRegressor

The results will be saved in sklearn_models6c

Dataset	Applied preprocessing	Number of metrics
DS1: (default)	Simple classes elimination, data classes elimination, outliers elimination, and metric standardization	262
DS2:	DS1 + Feature selection	20
DS3:	DS1 + Context vector elimination	194
DS4:	DS1 + Context vector elimination and lexical metrics elimination 	177
DS5:	DS1 + Systematically generated metrics elimination	71
DS6:    Top 15 important source code metrics affecting testability

Use the method `inference_model2` of the class `Regression` to predict testability of new Java classes.

"""

__version__ = '0.7.2'
__author__ = 'Morteza Zakeri'

import os
import math
import datetime

import pandas as pd
import joblib
from joblib import dump, load

from sklearn.metrics import *
from sklearn.preprocessing import QuantileTransformer
from sklearn.inspection import permutation_importance
from sklearn.neural_network import MLPRegressor
from sklearn import linear_model, feature_selection
from sklearn.model_selection import train_test_split
from sklearn.model_selection import ShuffleSplit, GridSearchCV
from sklearn import tree, preprocessing
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.ensemble import VotingRegressor


class Regression(object):
    def __init__(self, df_path: str = None, feature_selection_mode=False):
        self.df = pd.read_csv(df_path, delimiter=',', index_col=False)
        self.X_train1, self.X_test1, self.y_train, self.y_test = train_test_split(self.df.iloc[:, 1:-1],
                                                                                  self.df.iloc[:, -1],
                                                                                  test_size=0.10,
                                                                                  random_state=117,
                                                                                  )

        # ---------------------------------------
        # -- Feature selection (For DS2)
        if feature_selection_mode:
            selector = feature_selection.SelectKBest(feature_selection.f_regression, k=15)
            # clf = linear_model.LassoCV(eps=1e-3, n_alphas=100, normalize=True, max_iter=5000, tol=1e-4)
            # clf.fit(self.X_train1, self.y_train)
            # importance = np.abs(clf.coef_)
            # print('importance', importance)
            # clf = RandomForestRegressor()
            # selector = feature_selection.SelectFromModel(clf, prefit=False, norm_order=2, max_features=20)
            selector.fit(self.X_train1, self.y_train)

            # Get columns to keep and create new dataframe with only selected features
            cols = selector.get_support(indices=True)
            self.X_train1 = self.X_train1.iloc[:, cols]
            self.X_test1 = self.X_test1.iloc[:, cols]
            print('Selected columns by feature selection:', self.X_train1.columns)
        # -- End of feature selection

        # ---------------------------------------
        # Standardization
        # self.scaler = preprocessing.RobustScaler(with_centering=True, with_scaling=True, unit_variance=True)
        # self.scaler = preprocessing.StandardScaler()
        self.scaler = QuantileTransformer(n_quantiles=1000, random_state=11)
        self.scaler.fit(self.X_train1)
        self.X_train = self.scaler.transform(self.X_train1)
        self.X_test = self.scaler.transform(self.X_test1)
        dump(self.scaler, df_path[:-4]+'.joblib')

    def evaluate_model(self, model=None, model_path=None):
        if model is None:
            model = joblib.load(model_path)
        y_true, y_pred = self.y_test, model.predict(self.X_test)
        # y_score = model.predict_proba(X_test)
        # Print all classifier model metrics
        print('Evaluating regressor ...')
        print('Regressor minimum prediction', min(y_pred), 'Regressor maximum prediction', max(y_pred))
        df = pd.DataFrame()
        df['r2_score_uniform_average'] = [r2_score(y_true, y_pred, multioutput='uniform_average')]
        df['r2_score_variance_weighted'] = [r2_score(y_true, y_pred, multioutput='variance_weighted')]
        df['explained_variance_score_uniform_average'] = [explained_variance_score(y_true, y_pred,
                                                                                   multioutput='uniform_average')]
        df['explained_variance_score_variance_weighted'] = [explained_variance_score(y_true, y_pred,
                                                                                     multioutput='variance_weighted')]
        df['mean_absolute_error'] = [mean_absolute_error(y_true, y_pred)]
        df['mean_squared_error_MSE'] = [mean_squared_error(y_true, y_pred)]
        df['mean_squared_error_RMSE'] = [mean_squared_error(y_true, y_pred, squared=False)]
        df['median_absolute_error'] = [median_absolute_error(y_true, y_pred)]

        if min(y_pred) >= 0:
            df['mean_squared_log_error'] = [mean_squared_log_error(y_true, y_pred)]

        # To handle ValueError: Mean Tweedie deviance error with power=2 can only be used
        # on strictly positive y and y_pred.
        if min(y_pred > 0) and min(y_true) > 0:
            df['mean_poisson_deviance'] = [mean_poisson_deviance(y_true, y_pred, )]
            df['mean_gamma_deviance'] = [mean_gamma_deviance(y_true, y_pred, )]
        df['max_error'] = [max_error(y_true, y_pred)]

        df.to_csv(model_path[:-7] + '_evaluation_metrics_R1.csv', index=True, index_label='Row')

    def regress(self, model_path: str = None, model_number: int = None):
        """
        Train testability prediction on different model
        :param model_path:
        :param model_number: 1: DTR, 2: RFR, 3: GBR, 4: HGBR, 5: SGDR, 6: MLPR,
        :return:
        """
        if model_number == 1:
            regressor = tree.DecisionTreeRegressor(random_state=23, )
            # Set the parameters to be used for tuning by cross-validation
            parameters = {
                # 'criterion': ['mse', 'friedman_mse', 'mae'],
                'max_depth': range(3, 50, 5),
                'min_samples_split': range(2, 30, 2)
            }
        elif model_number == 2:
            regressor = RandomForestRegressor(random_state=19, )
            parameters = {
                'n_estimators': range(100, 200, 100),
                # 'criterion': ['mse', 'mae'],
                'max_depth': range(10, 50, 10),
                # 'min_samples_split': range(2, 30, 2),
                # 'max_features': ['auto', 'sqrt', 'log2']
            }
        elif model_number == 3:
            regressor = GradientBoostingRegressor(n_estimators=400, learning_rate=0.05, random_state=17, )
            parameters = {
                # 'loss': ['ls', 'lad', ],
                'max_depth': range(10, 50, 10),
                'min_samples_split': range(2, 30, 3)
            }
        elif model_number == 4:
            regressor = HistGradientBoostingRegressor(max_iter=400, learning_rate=0.05, random_state=13, )
            parameters = {
                # 'loss': ['least_squares', 'least_absolute_deviation'],
                'max_depth': range(10, 50, 10),
                'min_samples_leaf': range(5, 50, 10)
            }
        elif model_number == 5:
            regressor = linear_model.SGDRegressor(early_stopping=True, n_iter_no_change=5, random_state=11, )
            parameters = {
                'loss': ['squared_loss', 'huber', 'epsilon_insensitive'],
                'penalty': ['l2', 'l1', 'elasticnet'],
                'max_iter': range(50, 1000, 50),
                'learning_rate': ['invscaling', 'optimal', 'constant', 'adaptive'],
                'eta0': [0.1, 0.01],
                'average': [32, ]
            }
        elif model_number == 6:
            regressor = MLPRegressor(random_state=7, )
            parameters = {
                'hidden_layer_sizes': [(256, 100), (512, 256, 100), ],
                'activation': ['tanh', ],
                'solver': ['adam', ],
                'max_iter': range(50, 200, 50)
            }

        # Set the objectives which must be optimized during parameter tuning
        # scoring = ['r2', 'neg_mean_squared_error', 'neg_root_mean_squared_error', 'neg_mean_absolute_error',]
        scoring = ['neg_root_mean_squared_error', ]
        # CrossValidation iterator object:
        # https://scikit-learn.org/stable/tutorial/statistical_inference/model_selection.html
        cv = ShuffleSplit(n_splits=5, test_size=0.20, random_state=101)
        # Find the best model using gird-search with cross-validation
        clf = GridSearchCV(regressor, param_grid=parameters, scoring=scoring, cv=cv,
                           n_jobs=7, refit='neg_root_mean_squared_error')
        print('Fitting model number', model_number)
        clf.fit(X=self.X_train, y=self.y_train)

        print('Writing grid search result ...')
        df = pd.DataFrame(clf.cv_results_, )
        df.to_csv(model_path[:-7] + '_grid_search_cv_results.csv', index=False)
        df = pd.DataFrame()
        print('Best parameters set found on development set:', clf.best_params_)
        df['best_parameters_development_set'] = [clf.best_params_]
        print('Best classifier score on development set:', clf.best_score_)
        df['best_score_development_set'] = [clf.best_score_]
        print('best classifier score on test set:', clf.score(self.X_test, self.y_test))
        df['best_score_test_set:'] = [clf.score(self.X_test, self.y_test)]
        df.to_csv(model_path[:-7] + '_grid_search_cv_results_best.csv', index=False)

        # Save and evaluate the best obtained model
        print('Writing evaluation result ...')
        clf = clf.best_estimator_
        y_true, y_pred = self.y_test, clf.predict(self.X_test)
        dump(clf, model_path)
        self.evaluate_model(model=clf, model_path=model_path)
        print('=' * 50)

    def vote(self, model_path=None, dataset_number=1):
        # Trained regressors
        reg1 = load(r'sklearn_models7/HGBR1_DS{0}.joblib'.format(dataset_number))
        reg2 = load(r'sklearn_models7/RFR1_DS{0}.joblib'.format(dataset_number))
        reg3 = load(r'sklearn_models7/MLPR1_DS{0}.joblib'.format(dataset_number))
        # reg4 = load(r'sklearn_models7/SGDR1_DS1.joblib')
        ereg = VotingRegressor(
            [('HGBR1_DS{0}'.format(dataset_number), reg1),
             ('RFR1_DS{0}'.format(dataset_number), reg2),
             ('MLPR1_DS{0}'.format(dataset_number), reg3)],
            weights=[3. / 6., 2. / 6., 1. / 6.]
        )
        ereg.fit(self.X_train, self.y_train)
        dump(ereg, model_path)
        self.evaluate_model(model=ereg, model_path=model_path)


def train_dateset_g7(ds_number=0):
    """
    Dataset generation G7
    """
    reg = None
    if ds_number == 0:
        return
    elif ds_number == 1:
        # DS1
        reg = Regression(df_path=r'data_model/DS07012.csv')
    elif ds_number == 2:
        reg = Regression(df_path=r'data_model/DS07012.csv', feature_selection_mode=True)
    elif ds_number == 3:
        reg = Regression(df_path=r'data_model/DS07310.csv')
    elif ds_number == 4:
        reg = Regression(df_path=r'data_model/DS06410.csv')
    elif ds_number == 5:
        reg = Regression(df_path=r'data_model/DS07510.csv')
    elif ds_number == 6:
        reg = Regression(df_path=r'data_model/DS07610.csv')
    elif ds_number == 7:
        reg = Regression(df_path=r'data_model/DS07710.csv')

    if reg is None:
        return

    # reg.regress(model_path=r'sklearn_models7/DTR1_DS1.joblib', model_number=1)
    reg.regress(model_path=f'sklearn_models7/RFR1_DS{ds_number}.joblib', model_number=2)
    # reg.regress(model_path=f'sklearn_models7/GBR1_DS{ds_number}.joblib', model_number=3)
    reg.regress(model_path=f'sklearn_models7/HGBR1_DS{ds_number}.joblib', model_number=4)
    # reg.regress(model_path=f'sklearn_models7/SGDR1_DS{ds_number}.joblib', model_number=5)
    reg.regress(model_path=f'sklearn_models7/MLPR1_DS{ds_number}.joblib', model_number=6)
    reg.vote(model_path=f'sklearn_models7/VR1_DS{ds_number}.joblib', dataset_number=ds_number)


def create_testability_dataset_with_only_important_metrics():
    """
    Create DS#6 (DS07610)
    For use in Mr Esmaeili project
    Select only top 15 important testability features
    :return:
    """
    df_path = r'data_model/DS07012.csv'
    df_important_metrics_path = r'data_model/DS07610.csv'
    df = pd.read_csv(df_path, delimiter=',', index_col=False)
    df_imp = pd.DataFrame()
    df_imp['Class'] = df['Class']  # 0
    df_imp['CSORD_AvgLineCodeExe'] = df['CSORD_AvgLineCodeExe']  # 1
    df_imp['CSLEX_NumberOfConditionalJumpStatements'] = df['CSLEX_NumberOfConditionalJumpStatements']  # 2
    df_imp['CSORD_AvgLineCode'] = df['CSORD_AvgLineCode']  # 3
    df_imp['CSORD_NumberOfDepends'] = df['CSORD_NumberOfDepends']  # 4
    df_imp['CSLEX_NumberOfUniqueIdentifiers'] = df['CSLEX_NumberOfUniqueIdentifiers']  # 5
    df_imp['CSLEX_NumberOfDots'] = df['CSLEX_NumberOfDots']  # 6
    df_imp['CSORD_CountDeclInstanceMethod'] = df['CSORD_CountDeclInstanceMethod']  # 7
    df_imp['CSORD_CountDeclMethodPublic'] = df['CSORD_CountDeclMethodPublic']  # 8
    df_imp['CSORD_NIM'] = df['CSORD_NIM']  # 9
    df_imp['CSORD_AvgStmtDecl'] = df['CSORD_AvgStmtDecl']  # 10
    df_imp['CSORD_CountDeclClassMethod'] = df['CSORD_CountDeclClassMethod']  # 11
    df_imp['CSLEX_NumberOfNewStatements'] = df['CSLEX_NumberOfNewStatements']  # 12
    df_imp['CSLEX_NumberOfReturnAndPrintStatements'] = df['CSLEX_NumberOfReturnAndPrintStatements']  # 13
    df_imp['CSORD_NumberOfClassConstructors'] = df['CSORD_NumberOfClassConstructors']  # 14
    df_imp['PK_CountDeclClassMethod'] = df['PK_CountDeclClassMethod']  # 15
    df_imp['Testability'] = df['Testability']  # 16

    df_imp.to_csv(df_important_metrics_path, index=False)


def create_testability_dataset_with_only_10_important_metrics():
    df_path = r'data_model/DS07610.csv'
    df_new_path = r'data_model/DS07710.csv'
    df = pd.read_csv(df_path, delimiter=',', index_col=False)
    df.drop(columns=['CSORD_CountDeclClassMethod','CSLEX_NumberOfNewStatements',
                     'CSLEX_NumberOfReturnAndPrintStatements','CSORD_NumberOfClassConstructors',
                     'PK_CountDeclClassMethod'], inplace=True)
    df.to_csv(df_new_path, index=False)


def main():
    train_dateset_g7(ds_number=7)
    # create_testability_dataset_with_only_important_metrics()
    # create_testability_dataset_with_only_10_important_metrics()


# -----------------------------------------------
if __name__ == '__main__':
    print(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), '\t Program Start ...')
    main()
    print(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), '\t Program End ...')
