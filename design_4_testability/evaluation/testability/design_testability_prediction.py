"""

The module predicts design testability based on the novel design testability prediction model

"""

__version__ = '0.1.0'
__author__ = 'Morteza Zakeri'

import os
import pandas as pd
import networkx as nx
import re
import joblib

import understand

from design_4_testability.evaluation.testability.directory_utils import export_understand_dependencies_csv


class TestabilityPrediction:
    def __init__(self, **kwargs):
        self.db_path = kwargs['db_path']
        self.project_name = kwargs['project_name']
        graph_path = self.create_mdg()
        self.mdg_df = pd.read_csv(graph_path)
        self.mdg_df.rename(columns={"From Entities": "From_Entities", "To Entities": "To_Entities"}, inplace=True)
        if self.mdg_df is not None and not self.mdg_df.empty:
            self.mdg_graph = nx.from_pandas_edgelist(
                self.mdg_df, source='From Class', target='To Class',
                edge_attr=True, create_using=nx.DiGraph()
            )
        else:
            self.mdg_graph = None

    def create_mdg(self):
        csv_path = os.path.join(
            os.path.dirname(__file__),
            f'mdg_production_code_experiments/{self.project_name}_MDG.csv'
        )
        export_understand_dependencies_csv(
            csv_path=csv_path,
            db_path=self.db_path
        )
        return csv_path

    def extract_node_statistics(self, ):
        db: understand.Db = understand.open(self.db_path)
        G = self.mdg_graph
        # G = nx.subgraph(self.mdg_graph, max(nx.weakly_connected_components(self.mdg_graph), key=len))
        df = pd.DataFrame()
        if self.mdg_graph is None:
            return

        print('Computing graph attributes for all nodes in the graph components ...')
        average_neighbor_degree_dict = nx.average_neighbor_degree(G)
        # Category: Node centrality features
        degree_centrality_dict = nx.degree_centrality(G)
        in_degree_centrality_dict = nx.in_degree_centrality(G)
        out_degree_centrality_dict = nx.out_degree_centrality(G)
        closeness_centrality_dict = nx.closeness_centrality(G)
        betweenness_centrality_dict = nx.betweenness_centrality(G)
        katz_centrality_dict = nx.katz_centrality(G)
        eigenvector_centrality_numpy_dict = nx.eigenvector_centrality_numpy(G)
        harmonic_centrality_dict = nx.harmonic_centrality(G)

        current_flow_closeness_centrality_dict = dict()
        current_flow_betweenness_centrality_dict = dict()
        for node_set in nx.weakly_connected_components(self.mdg_graph):
            CCG = nx.subgraph(self.mdg_graph, node_set)
            current_flow_closeness_centrality_dict.update(nx.current_flow_closeness_centrality(nx.Graph(CCG)))
            # time-consuming
            current_flow_betweenness_centrality_dict.update(nx.current_flow_betweenness_centrality(nx.Graph(CCG)))

        pagerank_dict = nx.pagerank(G)

        print('Computing feature vector for each node (class) ...')
        for i, u in enumerate(self.mdg_graph.nodes()):
            df_temp = pd.DataFrame()
            df_temp['Class'] = [u]

            entities = db.lookup(re.compile(u + r'$'), )
            if entities is None or len(entities) == 0:  # Nested classes
                continue
            if str(entities[0].kind().name()).find('Enum') != -1:
                continue
            if str(entities[0].kind().name()).find('Unknown') != -1:
                continue
            if str(entities[0].kind().name()).find('Unresolved') != -1:
                continue

            if ('Abstract' in entities[0].kind().name()) or ('Interface' in entities[0].kind().name()):
                df_temp['AbstractOrInterface'] = [1]
            else:
                df_temp['AbstractOrInterface'] = [0]

            # Features for source class, u (15)
            df_temp['InDegree'] = [self.mdg_graph.in_degree(u)]
            df_temp['OutDegree'] = [self.mdg_graph.out_degree(u)]
            df_temp['AverageNeighborDegree'] = [average_neighbor_degree_dict[u]]
            # Category: Node centrality features
            df_temp['DegreeCentrality'] = [degree_centrality_dict[u]]
            df_temp['InDegreeCentrality'] = [in_degree_centrality_dict[u]]
            df_temp['OutDegreeCentrality'] = [out_degree_centrality_dict[u]]
            df_temp['ClosenessCentrality'] = [closeness_centrality_dict[u]]
            df_temp['BetweennessCentrality'] = [betweenness_centrality_dict[u]]
            df_temp['KatzCentrality'] = [katz_centrality_dict[u]]
            df_temp['EigenvectorCentrality'] = [eigenvector_centrality_numpy_dict[u]]
            df_temp['HarmonicCentrality'] = [harmonic_centrality_dict[u]]
            df_temp['CurrentFlowClosenessCentrality'] = [current_flow_closeness_centrality_dict[u]]
            df_temp['CurrentFlowBetweennessCentrality'] = [current_flow_betweenness_centrality_dict[u]]

            df_temp['PageRank'] = [pagerank_dict[u]]
            avg_shortest_path = nx.single_source_dijkstra_path_length(G=G, source=u).values()
            df_temp['AverageDijkstraPathLength'] = [sum(avg_shortest_path) / len(avg_shortest_path)]

            df = pd.concat([df, df_temp], ignore_index=True)
            # print(df.values)
        db.close()
        print(df)
        return df

    def inference_model(self, model_path=None, scaler_path=None):
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)

        df_predict_data = self.extract_node_statistics()
        df_predict_data = df_predict_data.fillna(0)
        df_predict_data1 = df_predict_data.loc[df_predict_data['AbstractOrInterface'] == 1]
        df_predict_data2 = df_predict_data.loc[df_predict_data['AbstractOrInterface'] == 0]

        X_test1 = df_predict_data2.iloc[:, 2:]
        X_test = scaler.transform(X_test1)
        y_pred = model.predict(X_test)

        df_predict_data2['Testability'] = list(y_pred)

        df_predict_data1['Testability'] = [1]*len(df_predict_data1)
        df_new = pd.concat([df_predict_data2, df_predict_data1], ignore_index=True)
        print(df_new)

        df_new.to_csv(f'{self.project_name}_testability.csv', index=False)
        print(f'Design testability for "{self.project_name}" = {df_new["Testability"].mean()}')
        return df_new["Testability"].mean()


def main(db_path=None, project_name=None, model_path=None, scaler_path=None):
    tp = TestabilityPrediction(db_path=db_path, project_name=project_name)
    tp.inference_model(model_path=model_path, scaler_path=scaler_path)


if __name__ == '__main__':
    db_path_ = r'C:/Users/Zakeri/Desktop/SF110/10_water-simulator.und'  # This path should be replaced for each project
    project_name_ = '10_water-simulator'

    model_path_ = r'../test_effectiveness/sklearn_models_nodes_regress/VoR1_DS2.joblib'
    scaler_path_ = r'../test_effectiveness/sklearn_models_nodes_regress/scaler.joblib'

    main(db_path=db_path_, project_name=project_name_, model_path=model_path_, scaler_path=scaler_path_)
