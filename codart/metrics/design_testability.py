"""


"""

import os
import pandas as pd

import networkx as nx


class Design:
    def __init__(self, graph_path, **kwargs):
        self.mdg_df = pd.read_csv(graph_path)
        self.mdg_df.rename(columns={"From Entities": "From_Entities", "To Entities": "To_Entities"}, inplace=True)
        if self.mdg_df is not None and not self.mdg_df.empty:
            self.mdg_graph = nx.from_pandas_edgelist(
                self.mdg_df,
                source='From Class', target='To Class',
                edge_attr=True,
                create_using=nx.DiGraph()
            )
        else:
            self.mdg_graph = None


    def extract_statistics(self, project_name):
        # G = self.mdg_graph
        G = nx.subgraph(self.mdg_graph, max(nx.weakly_connected_components(self.mdg_graph), key=len))

        df = pd.DataFrame()
        df['Project'] = [project_name[:-9]]
        # visualize_graph(graph=G)

        # nx.algorithms.community.asyn_lpa_communities
        df['number_of_nodes'] = [nx.number_of_nodes(G)]
        df['number_of_edges'] = [nx.number_of_edges(G)]
        df['number_of_selfloops'] = [nx.number_of_selfloops(G)]

        nx.betweenness_centrality

        df['average_degree'] = [sum([i[1] for i in nx.degree(G)]) / float(len(G))]

        df['average_neighbor_degree'] = [sum(nx.average_neighbor_degree(G).values()) / len(G)]
        df['average_degree_connectivity'] = [sum(nx.average_degree_connectivity(G).values()) / len(G)]
        # df['average_node_connectivity'] = [nx.average_node_connectivity(G)]  # time-consuming
        df['density'] = [nx.density(G)]

        # Just for directed graphs
        # print('condensation', nx.condensation(G))

        # Clustering coefficient 1 (Transitivity)
        df['transitivity'] = [nx.transitivity(G)]
        # Clustering coefficient 2 (CC)
        df['clustering_coefficient_2'] = [nx.average_clustering(G)]

        # print('degree_assortativity_coefficient', nx.degree_assortativity_coefficient(G))
        df['degree_pearson_correlation_coefficient'] = [nx.degree_pearson_correlation_coefficient(G)]

        # Category: Node centrality features
        df['degree_centrality'] = [sum(nx.degree_centrality(G).values()) / len(G)]
        # print('degree_centrality', sorted(nx.degree_centrality(G).items(), key=lambda kv: (kv[1], kv[0]))[:10])
        df['in_degree_centrality'] = [sum(nx.in_degree_centrality(G).values()) / len(G)]
        df['out_degree_centrality'] = [sum(nx.out_degree_centrality(G).values()) / len(G)]

        df['closeness_centrality'] = [sum(nx.closeness_centrality(G).values()) / len(G)]
        df['betweenness_centrality'] = [sum(nx.betweenness_centrality(G).values()) / len(G)]
        df['katz_centrality'] = [sum(nx.katz_centrality(G).values()) / len(G)]
        df['eigenvector_centrality'] = [sum(nx.eigenvector_centrality_numpy(G).values()) / len(G)]
        df['harmonic_centrality'] = [sum(nx.harmonic_centrality(G).values()) / len(G)]
        # df['percolation_centrality'] = sum(nx.percolation_centrality(G, attribute=None).values()) / len(G)
        df['current_flow_closeness_centrality'] = [
            sum(nx.current_flow_closeness_centrality(nx.Graph(G)).values()) / len(G)]
        df['current_flow_betweenness_centrality'] = [
            sum(nx.current_flow_betweenness_centrality(nx.Graph(G)).values()) / len(G)]  # time-consuming

        # Category: Edge centrality features
        df['edge_betweenness_centrality'] = [
            sum(nx.edge_betweenness_centrality(nx.Graph(G)).values()) / nx.number_of_edges(G)]
        df['edge_current_flow_betweenness_centrality'] = [sum(
            nx.edge_current_flow_betweenness_centrality(nx.Graph(G)).values()) / nx.number_of_edges(G)]

        df['page_rank'] = [sum(nx.pagerank(G).values()) / len(G)]

        print(df)
        return df

    def extract_components(self, project_name):
        # x = nx.number_connected_components(self.mdg_graph)
        x = 1
        y = nx.number_strongly_connected_components(self.mdg_graph)
        z = nx.number_weakly_connected_components(self.mdg_graph)
        for wcc in nx.weakly_connected_components(self.mdg_graph):
            print(len(wcc), nx.subgraph(self.mdg_graph, wcc))
        print(project_name, y, z)

        return z

def extract_design_metrics():
    mdg_path = 'mdgs_remained/'
    files = [f for f in os.listdir(mdg_path) if os.path.isfile(os.path.join(mdg_path, f))]
    z = 0
    for f in files:
        print(f'processing understand db file {f}:')
        mdg = Design(mdg_path + f, )
        df1 = mdg.extract_statistics(project_name=f)
        df1.to_csv(f'dataset/{f}', index=False)


if __name__ == '__main__':
    extract_design_metrics()
    # quit()
