"""

This module contains modularity measurement script at package-level
to be used in refactoring process in addition to QMOOD metrics

## Changelog
### v0.2.2
- Improve performance
- Improve accuracy
- Remove unused codes

## Reference
[1] https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.quality.modularity.html
[2] https://networkx.org/documentation/stable/_modules/networkx/algorithms/community/quality.html
[3] M. E. J. Newman “Networks: An Introduction”, page 224. Oxford University Press, 2011.


"""

__version__ = '0.2.1'
__author__ = 'Morteza Zakeri'

import os
import re
from collections import defaultdict

import pandas
import networkx as nx
import networkx.algorithms.community as nx_comm
import pandas as pd

import understand


from codart.utility.directory_utils import export_understand_dependencies_csv


class Modularity:
    def __init__(self, graph_path, project_db_path, **kwargs):
        self.mdg_df = pandas.read_csv(graph_path)
        self.project_db_path = project_db_path
        # Delete nested classes
        # Dropping the rows of "(" or ")"
        # print('Before delete nested classes', self.mdg_df.shape)
        self.mdg_df = self.mdg_df[~self.mdg_df["From Class"].str.contains(r"\)")]
        self.mdg_df = self.mdg_df[~self.mdg_df["To Class"].str.contains(r"\)")]
        # print('After delete nested classes', self.mdg_df.shape)
        self.class_package_dict = dict()
        self.create_class_package_dict()

        self.mdg_graph = nx.from_pandas_edgelist(
            self.mdg_df, source='From Class',
            target='To Class',
            edge_attr='References',
            create_using=nx.DiGraph()
        )

    def create_class_package_dict(self):
        classes = []
        classes.extend(self.mdg_df["From Class"].values)
        classes.extend(self.mdg_df["To Class"].values)
        classes = set(classes)
        # print(len(classes), )
        # print(classes)
        # print(self.mdg_df.shape)
        db = understand.open(self.project_db_path)
        for class_longname in classes:
            # print('Processing ',class_longname )
            class_longname2 = class_longname.replace('$', '.')
            entities = db.lookup(re.compile(class_longname2 + r'$'), )
            if entities is None or len(entities) == 0:  # Nested classes
                self.mdg_df = self.mdg_df[~self.mdg_df["From Class"].str.contains(class_longname)]
                self.mdg_df = self.mdg_df[~self.mdg_df["To Class"].str.contains(class_longname)]
                # print('Removed rows with class', class_longname, self.mdg_df.shape)
            else:
                class_entity = entities[0]
                package_list = class_entity.ents('Containin', 'Java Package')
                while not package_list and class_entity.parent() is not None:
                    package_list = class_entity.parent().ents('Containin', 'Java Package')
                    class_entity = class_entity.parent()
                # print(package_list)
                if len(package_list) < 1:
                    self.class_package_dict.update({class_longname: 'default'})
                else:
                    self.class_package_dict.update({class_longname: package_list[0].longname()})
        db.close()

    def compute_modularity_newman_leicht(self, ):
        """
        ## Example:
            communities = [['p1.C1', 'p1.C2', 'p1.C3'], ['p2.C4', 'p2.C5']]
            G = nx.barbell_graph(3, 0)

        :return:
        """
        q = 0
        if self.mdg_graph is not None and self.mdg_graph.number_of_edges() > 0:
            # communities = {v: k for k, v in self.class_package_dict.items()}
            communities = defaultdict(list)
            for key, value in self.class_package_dict.items():
                communities[value].append(key)
            q = nx_comm.modularity(self.mdg_graph, communities=communities.values())
        # print(q)
        return q


# Modularity API
def main(project_db_path=None, project_name=None, initial_value=1.0):
    """
    A demo of using modularity module to measure modularity quality attribute based on graph-analysis
    """

    # csv_path = os.path.abspath('../metrics/mdg/MDG.csv')
    csv_path = os.path.join(os.path.dirname(__file__), f'mdg_production_code/{project_name}_MDG.csv')
    export_understand_dependencies_csv(
        csv_path=csv_path,
        db_path=project_db_path
    )
    # while not os.path.exists(csv_path):
    #     time.sleep(0.05)

    if not os.path.exists(csv_path):
        return initial_value
    modulo = Modularity(graph_path=csv_path, project_db_path=project_db_path)
    q = modulo.compute_modularity_newman_leicht()
    # os.remove(csv_path)
    # q = 0
    return round(q / initial_value, 5)


def compute_all_modularity(udbs_path):
    files = [f for f in os.listdir(udbs_path) if os.path.isdir(os.path.join(udbs_path, f)) and f[-4:] == '.und']
    df = pd.DataFrame(columns=['Project', 'Modularity'])
    for f in files[9:]:
        q = main(project_db_path=os.path.join(udbs_path, f), project_name=f[:-4],)
        df1 = pd.DataFrame(columns=['Project', 'Modularity'])
        df1['Project'] = [f[:-4]]
        df1['Modularity'] = [q]
        df = pd.concat([df, df1], ignore_index=True)
        print(f'Computed modularity for project {f[:-4]}: {q}')
    df.to_csv('SF110_codart_modularity_production_code.csv', index=False)


# Test module
if __name__ == '__main__':
    udbs_path_ = 'D:/AnacondaProjects/iust_start/testability/sf110_without_test/'
    compute_all_modularity(udbs_path_)
