"""

This module contains modularity measurement script
to be used in refactoring process in addition to qmood metrics

## Reference
[1]
[2]


"""

__version__ = '0.1.0'
__author__ = 'Morteza Zakeri'

import sys
import os
import pandas
import pandas as pd
import networkx as nx
import networkx.algorithms.community as nx_comm

import understand
from matplotlib import pyplot as plt

from naming import UnderstandUtility


class Modularity:
    def __init__(self, graph_path, db, **kwargs):
        self.mdg_df = pandas.read_csv(graph_path)
        self.mdg_graph = nx.from_pandas_edgelist(self.mdg_df, source='From Class', target='To Class',
                                                 edge_attr='References', create_using=nx.DiGraph())
        self.db = db

        # self.show_mdg()

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
            communities = self.__roster_communities()
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
            package_name = self.__get_package_name_by_understand_query(node_)
            if package_name in communities_dict.keys():
                communities_dict[package_name].append(node_)
            else:
                communities_dict[package_name] = [node_]
        # print(communities_dict.values())
        return communities_dict

    def __get_package_name_by_parsing(self, class_longname: str = None):
        if class_longname.find('.') == -1:
            return 'default'
        else:
            package_name, class_short_name = class_longname.rsplit('.', 1)
            return package_name

    def __get_package_name_by_understand_query(self, class_longname: str = None):
        """
        This method can be used instead of `__get_package_name_by_parsing` and it is more accurate

        """
        package_entity, package_longname = UnderstandUtility.get_package_of_given_class_2(self.db, class_longname)
        # print(package_entity.longname())

        return package_longname


# Modularity API
def main(project_path='../benchmark_projects/JSON/JSON.und'):
    """
    A demo of using modularity module to measure modularity quality attribute based on graph-analysis
    """
    project_path = '../benchmark_projects/ganttproject/biz.ganttproject.core/biz.ganttproject.core.und'
    db = understand.open(project_path)
    # entities = db.ents('Java Class')
    cmd_ = 'und export -dependencies class csv {0} {1}'.format('mdg/MDG.csv', project_path)
    os.system('cmd /c "{0}"'.format(cmd_))

    modulo = Modularity(graph_path=r'mdg/MDG.csv', db=db)
    q = modulo.compute_modularity_newman_leicht()
    print(q)
    return q


if __name__ == '__main__':
    main()
