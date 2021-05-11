
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

def draw(g: nx.DiGraph = None):
    """

    :param g:
    :return:
    """
    pos = nx.kamada_kawai_layout(G=g)
    # pos = graphviz_layout(G=g,
    #                       prog='dot',
                          # prog='circo',
                          # )
    # pos = nx.bipartite_layout(G=g, nodes=g.nodes)
    # pos = nx.spectral_layout(G=g)
    # pos = hierarchy_pos(G=g,)
    # pos = nx.spiral_layout(G=g)
    # pos = nx.spiral_layout(G=g)
    # colors = [g[u][v]['color'] for u, v in g.edges]
    nx.draw(g,
            with_labels=True,
            node_size=500,
            # node_color='black',
            # edge_color=colors,
            pos=pos,
            )
    # edge_labels = nx.get_edge_attributes(g, 'edge_type')
    # print('#', edge_labels)
    # nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, )

    """
    node_labels = {}
    for node in g.nodes():
        # set the node name as the key and the label as its value
        node_labels[node] = node.value
    nx.draw_networkx_labels(g, pos, node_labels, font_size=12, font_color='w')
    """

    # plt.savefig('../../docs/figs/ast1.png')
    plt.show()