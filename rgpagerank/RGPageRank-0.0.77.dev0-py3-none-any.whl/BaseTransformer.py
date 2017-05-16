from abc import ABCMeta, abstractmethod
from re import findall
import networkx as nx
from pylab import show
from collections import OrderedDict


class BaseTransformer(metaclass=ABCMeta):
    """
    :var data
    :type dict|OrderedDict
    """
    __data = {}

    """
    :var graph
    :type DiGraph
    """
    __graph = False

    def __init__(self, data):
        self.__data = self.prepare(data)

    @abstractmethod
    def prepare(self, data):
        pass

    def get_data(self):
        return self.__data

    def count(self):
        return len(self.__data)

    def nodes_with_number(self):
        return OrderedDict((node, number) for number, node in enumerate(self.nodes()))

    def nodes(self):
        return list(self.__data.keys())

    def prepare_nodes(self):

        """
        grasp links (keys) from given resources (values)

        :return: dict
        """

        links = OrderedDict([])

        pattern = ''
        for node in self.__data.keys():
            pattern += str(node) + '|'

        pattern = pattern.rstrip('|')

        for node, content in self.__data.items():
            links[node] = findall(pattern, content)

        return links

    def make_graph(self):

        """
        build directed graph with the prepared data

        :return: DiGraph
        """

        if isinstance(self.__graph, nx.DiGraph):
            return self.__graph

        edges = []
        for key, values in self.prepare_nodes().items():
            edges_weights = {}
            for v in values:
                if v == key:
                    continue

                edges_weights[v] = edges_weights[v] + 1 if v in edges_weights else 1

            for successor, weight in edges_weights.items():
                edges.append([key, successor, {'weight': weight}])

        self.__graph = nx.DiGraph()
        self.__graph.add_nodes_from(self.nodes())
        self.__graph.add_edges_from(edges)

        return self.__graph

    def draw_graph(self):
        G = self.make_graph()

        edge_labels = dict([((u, v,), d['weight'])
                            for u, v, d in G.edges(data=True)])

        node_labels = {node: node for node in G.nodes()}

        pos = nx.spring_layout(G)
        nx.draw_networkx_labels(G, pos, labels=node_labels)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw(G, pos, node_size=1000)
        show()
