import time

from design_4_testability.class_diagram_extraction.class_diagram import ClassDiagram
from design_4_testability.config import test_class_diagram

import networkx as nx
import csv


class Complexity():
    def __init__(self, class_diagram):
        self.class_diagram = class_diagram.class_diagram_graph
        self.CDG = class_diagram.get_CDG()

        # calculate hierarchical inheritance complexity
        self.inheritance_complexity_dic = {}
        candidate_nodes = self.__find_inheritance_candidates()
        for node in candidate_nodes:
            self.inheritance_complexity_dic[node] = self.__calculate_inheritance_complexity(node)

    def calculate_interaction_complexity(self, source, target):
        complexity = 1
        has_path = False
        for path in nx.all_simple_paths(self.class_diagram, source=source, target=target):
            has_path = True
            complexity *= self.__calculate_path_complexity(path)
        if not has_path:
            complexity = None
        return complexity

    def __calculate_path_complexity(self, path):
        complexity = 1
        for i in range(len(path) - 1):
            if self.CDG[path[i]][path[i+1]]['relation_type'] == 'use_def':
                if path[i] in self.inheritance_complexity_dic:
                    complexity *= self.inheritance_complexity_dic[path[i]]
        return complexity

    def __calculate_inheritance_complexity(self, node):
        complexity = 0
        stack = []
        stack.append(node)

        depth_dic = {node:1}
        while stack != []:
            current_node = stack.pop()
            is_leave = True
            for neighbor in self.CDG[current_node]:
                if (current_node in self.CDG[neighbor]):
                    if self.CDG[current_node][neighbor]['relation_type'] == 'child' and self.CDG[neighbor][current_node]['relation_type'] == 'parent':
                        is_leave = False
                        stack.append(neighbor)
                        depth_dic[neighbor] = depth_dic[current_node] + 1

            if is_leave:
                complexity += depth_dic[current_node] * (depth_dic[current_node] - 1)
        return complexity

    def __find_inheritance_candidates(self):
        candidates = set()
        for edge in self.CDG.edges:
            if self.CDG.edges[edge]['relation_type'] == 'parent':
                candidates.add(edge[1])
        return candidates

    def get_matrix(self):
        start_time = time.time()
        node_list = list(self.CDG.nodes)
        no_nodes = len(node_list)
        node_list.sort()

        matrix = []
        for s in range(no_nodes):
            matrix.append([])
            for d in range(no_nodes):
                if self.CDG.nodes[node_list[s]]['type'] == "class" and self.CDG.nodes[node_list[d]]['type'] == "class":
                    complexity = self.calculate_interaction_complexity(node_list[s], node_list[d])
                    matrix[s].append(complexity)
                else:
                    matrix[s].append(None)
        execution_time = time.time() - start_time
        return matrix, execution_time

    @staticmethod
    def get_avg_of_matrix(matrix):
        n = 0
        s = 0
        for i in matrix:
            for j in i:
                if j is not None:
                    n += 1
                    s += j
        return s / n

    @staticmethod
    def get_sum_of_matrix(matrix):
        s = 0
        for i in matrix:
            for j in i:
                if j is not None:
                    s += j
        return s

    def save_csv(self, path):
        node_list = list(self.CDG.nodes)
        no_nodes = len(node_list)
        node_list.sort()
        header = ['src', 'dest', 'complexity']

        with open(path, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)

            # write the header
            no_row = 0
            writer.writerow(header)
            for s in range(no_nodes):
                for d in range(no_nodes):
                    print(s, d)
                    if self.CDG.nodes[node_list[s]]['type'] == "class" and self.CDG.nodes[node_list[d]][
                        'type'] == "class":
                        complexity = self.calculate_interaction_complexity(str(node_list[s]), str(node_list[d]))
                        no_row += 1

if __name__ == "__main__":
    cd = ClassDiagram(java_project_address='', base_dirs='', files=[], index_dic={})
    cd.class_diagram_graph = test_class_diagram
    cd.show(cd.class_diagram_graph)
    c = Complexity(cd)
    print(c.calculate_interaction_complexity(8, 7))




