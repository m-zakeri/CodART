"""

This module contains modularity measurement script at package-level
to be used in refactoring process in addition to qmood metrics

## Reference
[1]
[2]


"""

__version__ = '0.1.1'
__author__ = 'Morteza Zakeri'

import os
import re
import time
from collections import defaultdict

import pandas
import networkx as nx
import networkx.algorithms.community as nx_comm
from matplotlib import pyplot as plt

import understand

from codart.utility.directory_utils import export_understand_dependencies_csv


class Modularity:
    def __init__(self, graph_path, project_db_path, **kwargs):
        self.mdg_df = pandas.read_csv(graph_path)
        self.project_db_path = project_db_path
        # Delete nested classes
        # Dropping the rows of "(" or ")"
        print('Before delete nested classes', self.mdg_df.shape)
        self.mdg_df = self.mdg_df[~self.mdg_df["From Class"].str.contains(r"\)")]
        self.mdg_df = self.mdg_df[~self.mdg_df["To Class"].str.contains(r"\)")]
        print('After delete nested classes', self.mdg_df.shape)
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
        db = understand.open(self.project_db_path)
        for class_longname in classes:
            # print('Processing ',class_longname )
            entities = db.lookup(re.compile(class_longname + r'$'), )
            if entities is None or len(entities) == 0:  # Nested classes
                self.mdg_df = self.mdg_df[~self.mdg_df["From Class"].str.contains(class_longname)]
                self.mdg_df = self.mdg_df[~self.mdg_df["To Class"].str.contains(class_longname)]
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


    def show_mdg(self):
        pos = nx.spring_layout(self.mdg_graph)
        nx.draw(self.mdg_graph, pos=pos, with_labels=True, )
        edge_labels = nx.get_edge_attributes(self.mdg_graph, 'References')
        nx.draw_networkx_edge_labels(self.mdg_graph, pos=pos, edge_labels=edge_labels, font_color='red')
        plt.show()

    def compute_modularity_newman_leicht(self, ):
        """
        https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.quality.modularity.html

        ## Example:
            communities = [['p1.C1', 'p1.C2', 'p1.C3'], ['p2.C4', 'p2.C5']]
            G = nx.barbell_graph(3, 0)

        :return:
        """
        q = 0
        if self.mdg_graph is not None and self.mdg_graph.number_of_edges() > 0:
            # communities = self.__roster_communities()

            # communities = {v: k for k, v in self.class_package_dict.items()}
            communities = defaultdict(list)
            for key, value in self.class_package_dict.items():
                communities[value].append(key)
            q = nx_comm.modularity(self.mdg_graph, communities=communities.values())
        # print(q)
        return q

    def __roster_communities(self):
        """
        # Example:
        communities = self.df_class.groupby(['Parent'])['LongName'].apply(list)
        print(list(communities))
        :return:
        """
        communities_dict = dict()
        for node_ in self.mdg_graph:
            # print('node_:', node_)
            # package_name = self.__get_package_name_by_parsing(node_)
            # package_name = self.__get_package_name_by_understand_query(node_)
            package_name = self.class_package_dict[node_]
            if package_name in communities_dict.keys():
                communities_dict[package_name].append(node_)
            else:
                communities_dict[package_name] = [node_]
        # print(communities_dict.values())
        return communities_dict

    def __get_package_name_by_understand_query(self, class_longname: str = None):
        """
        This method can be used instead of `__get_package_name_by_parsing` and it is more accurate

        """
        db = understand.open(self.project_db_path)
        entities = db.lookup(re.compile(class_longname + r'$'), )
        if entities is None or len(entities) == 0:  # Nested classes
            db.close()
            return 'default'
        else:
            class_entity = entities[0]
            package_list = class_entity.ents('Containin', 'Java Package')
            while not package_list and class_entity.parent() is not None:
                package_list = class_entity.parent().ents('Containin', 'Java Package')
                class_entity = class_entity.parent()
            if len(package_list) < 1:
                db.close()
                return 'default'
            else:
                package_name = package_list[0].longname()
                db.close()
                return package_name

    def __get_package_name_by_parsing(self, class_longname: str = None):
        if class_longname.find('.') == -1:
            return 'default'
        else:
            package_name, class_short_name = class_longname.rsplit('.', 1)
            return package_name


# Modularity API
def main(project_db_path=None, initial_value=1.0):
    """
    A demo of using modularity module to measure modularity quality attribute based on graph-analysis
    """
    csv_path = os.path.abspath('../metrics/mdg/MDG.csv')
    export_understand_dependencies_csv(
        csv_path=csv_path,
        db_path=project_db_path
    )
    while not os.path.exists(csv_path):
        time.sleep(0.05)

    modulo = Modularity(graph_path=csv_path, project_db_path=project_db_path)
    q = modulo.compute_modularity_newman_leicht()
    os.remove(csv_path)
    return q / initial_value


# Test module
if __name__ == '__main__':
    from sbse.config import UDB_PATH

    for i in range(10):
        print(main(UDB_PATH))
