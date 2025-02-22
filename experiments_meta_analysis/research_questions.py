"""
The script contains functions used to answer CodART experiments_meta_analysis research questions

"""

__version__ = '0.1.1'
__author__ = 'Morteza Zakeri'

import glob
import itertools
import os
from decimal import Decimal

import numpy as np
import pandas
import pandas as pd
from scipy.stats import ttest_ind, mannwhitneyu, ranksums, brunnermunzel, wilcoxon, kruskal

from matplotlib import pyplot as plt
import seaborn as sns
from sklearn import preprocessing

experimental_results_path = r'E:/LSSDS/CodART/Experimental1/prj_src/'

project1_path = 'tabula-java_CodART_Log/execution__2022-04-25_15-20-26/classes_testability2_for_problem_2.csv'
project1_path_after = 'tabula-java_CodART_Log/execution__2022-04-25_15-20-26/classes_testability2_for_problem_2_best_sequence_2.csv'

project2_path = '88_jopenchart_CodART_Log/execution__2022-04-29_22-27-14/classes_testability2_for_problem_2.csv'
project2_path_after = '88_jopenchart_CodART_Log/execution__2022-04-29_22-27-14/classes_testability2_for_problem_2_best_sequence_2.csv'

project3_path = '10_water-simulator_CodART_Log/execution__2022-04-25_16-18-19/classes_testability2_for_problem_2.csv'
project3_path_after = '10_water-simulator_CodART_Log/execution__2022-04-25_16-18-19/classes_testability2_for_problem_2_best_sequence_0.csv'

project4_path = 'commons-codec_CodART_Log/execution__2022-04-28_21-19-07/classes_testability2_for_problem_2.csv'
project4_path_after = 'commons-codec_CodART_Log/execution__2022-04-28_21-19-07/classes_testability2_for_problem_2_best_sequence_1.csv'

project5_path = 'jvlt-1.3.2_CodART_Log/execution__2022-05-05_10-27-43/classes_testability2_for_problem_2.csv'
project5_path_after = 'jvlt-1.3.2_CodART_Log/execution__2022-05-05_10-27-43/classes_testability2_for_problem_2_best_sequence_1.csv'

project6_path = 'JHotDraw-7.0.6_CodART_Log/execution__2022-05-12_12-23-00/classes_testability2_for_problem_2.csv'
project6_path_after = 'JHotDraw-7.0.6_CodART_Log/execution__2022-05-12_12-23-00/classes_testability2_for_problem_2_best_sequence_1.csv'

project_name_path_dict = {
    'Tabula-java': [experimental_results_path + project1_path, experimental_results_path + project1_path_after],
    'JOpenChart': [experimental_results_path + project2_path, experimental_results_path + project2_path_after],
    'Water-Simulator': [experimental_results_path + project3_path, experimental_results_path + project3_path_after],
    'Commons Codec': [experimental_results_path + project4_path, experimental_results_path + project4_path_after],
    'jVLT': [experimental_results_path + project5_path, experimental_results_path + project5_path_after],
    'JHotDraw': [experimental_results_path + project6_path, experimental_results_path + project6_path_after],
}


def testability_improvement_statistical_test(test_all=True):
    """

    """

    if test_all:
        # For all projects
        df_before = pd.DataFrame()
        df_after = pd.DataFrame()
        for project, paths in project_name_path_dict.items():
            df1 = pd.read_csv(paths[0], index_col=False)
            df2 = pd.read_csv(paths[1], index_col=False)
            df_before = pd.concat([df_before, df1], ignore_index=True)
            df_after = pd.concat([df_after, df2], ignore_index=True)
    else:
        # For a single project
        df_before = pd.read_csv(
            project_name_path_dict['JHotDraw'][0],
            index_col=False
        )

        df_after = pd.read_csv(
            project_name_path_dict['JHotDraw'][1],
            index_col=False
        )

    print(df_before.describe())
    print(df_after.describe())

    tests = []
    meters = ['PredictedTestability', 'LineCoverage', 'BranchCoverage']
    for meter in meters:
        print(f'p-value for {meter}')
        absolute_meter_gain = df_after[meter].sum() - df_before[meter].sum()
        relative_meter_gain = (df_after[meter].sum() - df_before[meter].sum()) / df_before[meter].sum()
        print(f'Absolute {meter} gain: {absolute_meter_gain}')
        print(f'Relative {meter} gain: {relative_meter_gain}')

        s, p = ttest_ind(df_after[meter], df_before[meter], alternative="greater", )
        print(f'1 statistic independent t-test = {s}, p-value={p:.4E}',
              'Passed' if p < 0.05 else 'Failed'
              )

        s, p = mannwhitneyu(df_after[meter], df_before[meter], alternative="greater", )
        print(f'2 statistic Mann-Whitney U test = {s}, p-value={p:.4E}',
              'Passed' if p < 0.05 else 'Failed'
              )

        s, p = ranksums(df_after[meter], df_before[meter], alternative="greater", )
        print(f'3 statistic Wilcoxon rank-sum test = {s}, p-value={p:.4E}',
              'Passed' if p < 0.05 else 'Failed'
              )

        s, p = brunnermunzel(df_after[meter], df_before[meter], alternative="greater", )
        print(f'4 statistic Brunner-Munzel test = {s}, p-value={p:.4E}',
              'Passed' if p < 0.05 else 'Failed'
              )

        s, p = kruskal(df_after[meter], df_before[meter], )
        print(f'4 statistic Kruskal test = {s}, p-value={p:.4E}',
              'Passed' if p < 0.05 else 'Failed'
              )

        if len(df_before[meter]) == len(df_after[meter]):
            s, p = wilcoxon(df_after[meter], df_before[meter], alternative="greater", )
            print(f'5 statistic Wilcoxon test = {s}, p-value={p:.4E}',
                  'Passed' if p < 0.05 else 'Failed'
                  )

        print('-' * 50)


def plot_testability_box_whisker_plot():
    df_all = pandas.DataFrame()
    for project, paths in project_name_path_dict.items():
        df = pandas.DataFrame()
        df_before = pd.read_csv(
            paths[0],
            index_col=False
        )
        df_after = pd.read_csv(
            paths[1],
            index_col=False
        )

        df['Project'] = [project] * (len(df_before) + len(df_after))
        df['Stage'] = [*['Before refactoring'] * len(df_before), *['After refactoring'] * len(df_after)]

        df = pd.concat([df, pd.concat([df_before, df_after], ignore_index=True)], axis=1, join='inner')
        df.drop(columns=['Class', 'PredictedTestability'], inplace=True)
        # df.drop(columns=['Class', ], inplace=True)
        df_all = pd.concat([df_all, df], ignore_index=True)

    print(df_all)

    df3 = df_all.melt(id_vars=['Project', 'Stage'], var_name='Metric', value_name='Value')
    print(df3)
    # quit()
    g = sns.catplot(data=df3,
                    # x='Metric', y='Value', hue='Stage', col='Project',
                    x='Project', y='Value', hue='Stage', col='Metric',
                    col_wrap=1,
                    kind='box',
                    sharex=False, sharey=False, margin_titles=True,
                    height=1.75, aspect=1.25, orient='v',
                    legend_out=False, legend=True, dodge=True)

    g2 = sns.catplot(data=df3,
                     # x='Metric', y='Value', hue='Stage', col='Project',
                     x='Project', y='Value', hue='Stage', col='Metric',
                     col_wrap=1,
                     kind='point',
                     sharex=False, sharey=False, margin_titles=True,
                     height=2.5, aspect=0.95, orient='v',
                     legend_out=False, legend=True, dodge=True,
                     # axes=g.axes
                     palette=reversed(sns.color_palette('tab10', n_colors=2)),
                     markers=['o', '*', 'X'] * 2, linestyles=['dashed', 'dotted', '-.'] * 2
                     )
    # g.set(yscale="log")
    g.despine(left=True)
    g2.despine(left=True)
    # g.axes[19].legend(loc='upper center')
    # g2.axes[19].legend(loc='upper center')
    plt.tight_layout()
    plt.show()


def plot_conflict_study():
    res_path = r'E:/LSSDS/CodART/Experimental1/experimental1_excels_merged.xlsx'
    df = pd.read_excel(res_path, sheet_name='ConflictAnalysis')

    x = df.iloc[:, 2:].values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df2 = pd.DataFrame(x_scaled, columns=df.columns[2:])
    df2['Project'] = df['Project']
    df2['Version'] = df['Version']

    df3 = df2.melt(id_vars=['Project', 'Version', 'Testability'], var_name='Quality attribute', value_name='Value')

    g = sns.lmplot(
        data=df3, x="Testability", y="Value",
        # hue="Version",
        row="Project", col='Quality attribute',
        # kind="scatter",
        fit_reg=True,
        n_boot=10,
        x_ci='sd',
        ci=None,
        order=0,
        height=2,
        aspect=1.0,
        # markers=['o', 'x'],
        facet_kws={'sharey': False, 'sharex': False, 'margin_titles': True},
        # scatter_kws={"color": "black"},
        # line_kws={"color": "red"},

    )

    g2 = sns.relplot(
        data=df3, x="Testability", y="Value",
        row="Project", col='Quality attribute',
        kind="line",
        height=1.75,
        aspect=1.,

        facet_kws={'sharey': False, 'sharex': False, 'margin_titles': True}
    )

    g.set_titles(row_template='{row_name}', col_template='{col_name}')
    g2.set_titles(row_template='{row_name}', col_template='{col_name}')

    plt.tight_layout()
    plt.show()


def plot_position_analysis():
    csv_paths = glob.glob(os.path.join('E:/LSSDS/CodART/Experimental1/excels/position_data', 'positions_map*.csv'))
    df = pd.DataFrame()
    for path_ in csv_paths:
        df1 = pd.read_csv(path_, index_col=False, converters={'Position': int})
        df = pd.concat([df, df1])

    print(df)

    pos_map = {}
    for index, row in df.iterrows():
        if pos_map.get((row[1], f'Pos {row[2]}')) is None:
            pos_map[(row[1], f'Pos {row[2]}')] = 1
        else:
            pos_map[(row[1], f'Pos {row[2]}')] += 1

    print(pos_map)
    refactorings = [
        'Make Field Non-Static',
        'Make Field Static',
        'Make Method Static',
        'Make Method Non-Static',
        'Pull Up Field',
        'Push Down Field',
        'Pull Up Method',
        'Pull Up Constructor',
        'Push Down Method',
        'Move Field',
        'Move Method',
        'Move Class',
        'Extract Class',
        'Extract Interface',
        'Increase Field Visibility',
        'Increase Method Visibility',
        'Decrease Field Visibility',
        'Decrease Method Visibility',
    ]

    df2 = pd.DataFrame()
    df2['Refactoring'] = refactorings
    for col in [f'Pos {i}' for i in range(0, 50)]:
        df2[col] = [0] * len(refactorings)

    for key, value in pos_map.items():
        # print(key, ':::', value)
        df2.at[refactorings.index(key[0]), key[1]] = int(value)

    print(df2)
    df2.sort_values(by=['Refactoring'], ignore_index=True, inplace=True, axis=0)

    # quit()
    sns.heatmap(
        df2.iloc[:, 1:],
        annot=True,
        linewidths=.75,
        cmap="YlGnBu",
        yticklabels=df2['Refactoring']
    )

    plt.tight_layout()
    plt.show()

    df2['Sum'] = df2.iloc[:, 1:].sum(axis=1)

    df2.sort_values(by=['Sum'], ignore_index=True, inplace=True, axis=0)

    print(df2)
    print(df2.max())


def plot_tools_performance():
    res_path = r'E:/LSSDS/CodART/Experimental1/experimental1_excels_merged.xlsx'
    df = pd.read_excel(res_path, sheet_name='RelatedWorks', index_col=False)

    # df.drop(columns=[])

    g = sns.catplot(
        data=df,
        x='Project',
        y='Manual precision',
        hue='Tool',
        kind='bar',
        ci=95,
        errwidth=0.5,
        height=6.0,
        aspect=1.5,
        legend_out=False, legend=True, dodge=True,
        palette=sns.color_palette('tab10', n_colors=3),
        estimator=np.mean,
    )

    num_locations = 6
    hatches = itertools.cycle(['/', '\\', '//'])
    for i, bar in enumerate(g.axes[0, 0].patches):
        if i % num_locations == 0:
            hatch = next(hatches)
        bar.set_hatch(hatch)
        bar.set_width(0.20)

    plt.legend(ncol=3, fancybox=True,)

    # g.despine(left=True)
    # plt.legend(loc='upper center')
    # g.axes[0].legend(loc='upper center')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # testability_improvement_statistical_test()
    # plot_testability_box_whisker_plot()
    # plot_conflict_study()
    # plot_position_analysis()
    plot_tools_performance()
