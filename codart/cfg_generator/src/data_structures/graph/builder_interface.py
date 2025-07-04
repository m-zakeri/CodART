import abc
from typing import List, Tuple, Any, Dict, Union, Iterable


class IDiGraphBuilder(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def node_keys(self) -> Iterable[int]:
        """get nodes"""

    @property
    @abc.abstractmethod
    def node_values(self) -> Iterable:
        """get nodes content"""

    @property
    @abc.abstractmethod
    def node_items(self) -> Iterable:
        """get graph node items"""

    @property
    @abc.abstractmethod
    def edge_keys(self) -> Iterable[Tuple[int, int]]:
        """get edges"""

    @property
    @abc.abstractmethod
    def edge_values(self) -> Iterable:
        """get edges content"""

    @abc.abstractmethod
    def get_last_nodes(self) -> List:
        """get last nodes"""

    @property
    @abc.abstractmethod
    def edge_items(self) -> Iterable:
        """get graph edge items"""

    @property
    @abc.abstractmethod
    def head(self) -> int:
        """get the head node"""

    @property
    @abc.abstractmethod
    def last(self) -> int:
        """get the last node"""

    @abc.abstractmethod
    def descendants(self, node):
        """get graph node descendants"""

    @abc.abstractmethod
    def successors(self, node: int):
        """successors of a given node"""

    @abc.abstractmethod
    def has_edge(self, u: int, b: int) -> bool:
        """ Check if edge exists """

    @abc.abstractmethod
    def predecessors(self, node: int) -> Iterable:
        """predecessors of a given node"""

    @abc.abstractmethod
    def add_node(self, node: int, value: Any = None) -> "IDiGraphBuilder":
        """add a node"""

    @abc.abstractmethod
    def remove_node(self, node: int) -> "IDiGraphBuilder":
        """remove a node"""

    @abc.abstractmethod
    def add_nodes_from(self, nodes: List) -> "IDiGraphBuilder":
        """add a set of nodes"""

    @abc.abstractmethod
    def remove_nodes_from(self, nodes: List) -> "IDiGraphBuilder":
        """remove a set of nodes"""

    @abc.abstractmethod
    def add_edge(self, f: int, t: int, value: Any = None) -> "IDiGraphBuilder":
        """add an edge"""

    @abc.abstractmethod
    def remove_edge(self, f: int, t: int) -> "IDiGraphBuilder":
        """remove an edge"""

    @abc.abstractmethod
    def add_edges_from(self, edges: List) -> "IDiGraphBuilder":
        """add a set of edges"""

    @abc.abstractmethod
    def remove_edges_from(self, edges: List) -> "IDiGraphBuilder":
        """remove a set of edges"""

    @abc.abstractmethod
    def compose(self, graph: "IDiGraphBuilder") -> None:
        """compose (union) with a graph"""

    @abc.abstractmethod
    def reset_node_order(self) -> None:
        """reset node labels from zero"""

    @abc.abstractmethod
    def build(self):
        """build graph"""

    @abc.abstractmethod
    def as_dict(self) -> Dict:
        """get a dictionary presentation of graph"""

    @abc.abstractmethod
    def copy(self) -> "IDiGraphBuilder":
        """return a deep copy of object"""

    def __or__(self, other: "IDiGraphBuilder") -> "IDiGraphBuilder":
        """compose graphs and merge graph data"""

    @abc.abstractmethod
    def __rshift__(self, n: int) -> "IDiGraphBuilder":
        """shift right the nodes"""

    @abc.abstractmethod
    def __getitem__(self, item: Union[int, Tuple]):
        """get content of a node"""

    @abc.abstractmethod
    def __setitem__(self, item: Union[int, Tuple], content: Any):
        """set content of a node"""

    @abc.abstractmethod
    def __len__(self):
        """number of nodes"""

    def reset_list_order(self, diff) -> List:
        """reset node labels base on new graph node order"""
