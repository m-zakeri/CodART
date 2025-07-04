from typing import List, Any

import networkx as nx
from networkx import DiGraph

from cfg_generator.src.data_structures.graph.builder_interface import IDiGraphBuilder


class NxDiGraphBuilder(IDiGraphBuilder):
    VALUE = "value"

    def __init__(self):
        self.__graph = DiGraph()

    @property
    def node_keys(self):
        for node in self.__graph.nodes:
            yield node

    @property
    def node_values(self):
        for _, content in self.__graph.nodes.data(self.VALUE):
            yield content

    @property
    def node_items(self):
        return zip(self.node_keys, self.node_values)

    @property
    def edge_keys(self):
        for edge in self.__graph.edges:
            yield edge

    @property
    def edge_values(self):
        for _, _, content in self.__graph.edges.data(self.VALUE):
            yield content

    @property
    def edge_items(self):
        return zip(self.edge_keys, self.edge_values)

    @property
    def head(self):
        return min(self.node_keys)

    @property
    def last(self):
        return max(self.node_keys)

    def descendants(self, node):
        return nx.descendants(self.__graph, node)

    def add_node(self, node=0, value=None):
        self.__graph.add_node(node, value=value, node_color="#FFFFFF")
        return self

    def successors(self, node: int):
        for successor in self.__graph.successors(node):
            yield successor
    def has_edge(self, u: int, b: int) -> bool:
        return self.__graph.has_edge(u, b)

    def get_last_nodes(self):
        last_nodes = []
        for node in self.node_keys:
            if not dict(self.node_items)[node]:
                last_nodes.extend(list(self.predecessors(node)))
            elif not self.__graph.out_degree(node):
                last_nodes.extend([node])
        return last_nodes

    def predecessors(self, node: int):
        for predecessor in self.__graph.predecessors(node):
            yield predecessor

    def remove_node(self, node):
        self.__graph.remove_node(node)
        return self

    def add_nodes_from(self, nodes):
        mapper = lambda node: (node if isinstance(node, int) else
                               (node[0], {self.VALUE: node[1]}))
        ns = [mapper(node) for node in nodes]
        self.__graph.add_nodes_from(ns)
        return self

    def remove_nodes_from(self, nodes):
        self.__graph.remove_nodes_from(nodes)

    def add_edge(self, f, t, value=None):
        self.__graph.add_edge(f, t, value=value)
        return self

    def remove_edge(self, f, t):
        self.__graph.remove_edge(f, t)
        return self

    def add_edges_from(self, edges):
        mapper = lambda edge: ((edge[0], edge[1]) if len(edge) == 2 else
                               (edge[0], edge[1], {self.VALUE: edge[2]}))
        es = [mapper(edge) for edge in edges]
        self.__graph.add_edges_from(es)
        return self

    def remove_edges_from(self, edges):
        self.__graph.remove_edges_from(edges)
        return self

    def compose(self, other):
        self.__graph = nx.compose(other.__graph, self.__graph)

    def reset_node_order(self):
        self.__graph = nx.relabel_nodes(self.__graph, {old: new for new, old in enumerate(sorted(self.__graph.nodes))})

    def reset_list_order(self, diffs):
        end_list = []
        for diff in diffs:
            data = diff[1][0]
            edge_label = diff[1][1]
            for v in self.node_items:
                if data == v[1]:
                    end_list.extend([(v[0], edge_label)] if (v[0], diff[1]) not in end_list else [])
                    break

        return end_list

    def build(self):
        return self.__graph

    def as_dict(self):
        return {"nodes": list(self.node_items), "edges": list(self.edge_items)}

    def copy(self) -> "IDiGraphBuilder":
        g = NxDiGraphBuilder()
        g.__graph = self.__graph.copy()
        return g

    def __or__(self, other):
        common_nodes = set(self.node_keys) & set(other.node_keys)
        common_data_by_nodes = [(node, self[node] + other[node]) for node in common_nodes]

        g = NxDiGraphBuilder()
        g.__graph = nx.compose(other.__graph, self.__graph)
        for node, data in common_data_by_nodes:
            g[node] = data
        return g

    def __rshift__(self, n):
        g = NxDiGraphBuilder()
        g.__graph = nx.relabel_nodes(self.__graph, {i: i + n for i in self.__graph.nodes})
        return g

    def __getitem__(self, item):
        return (self.__graph.edges[item][self.VALUE] if isinstance(item, tuple) else
                self.__graph.nodes[item][self.VALUE])

    def __setitem__(self, item, content):
        if isinstance(item, tuple):
            self.__graph.edges[item][self.VALUE] = content
        else:
            self.__graph.nodes[item][self.VALUE] = content

    def __len__(self):
        return len(self.__graph)

    def __str__(self):
        return str(self.as_dict())
