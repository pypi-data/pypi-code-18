from collections import OrderedDict

from RGPageRank.BaseTransformer import BaseTransformer
from RGPageRank.DirectoryTransformer import DirectoryTransformer
from numpy import matrix
from numpy import sum, ones, dot
from numpy import zeros
from numpy.random import random

from RGPageRank.DictTransformer import DictTransformer


class PageRank(object):

    __graph = False

    __NX = 0

    __epsilon = 0.005

    def __init__(self, graph, recursive=False, truncate_extension=True):

        if isinstance(graph, BaseTransformer):
            self.__graph = graph
        elif isinstance(graph, str):
            self.__graph = DirectoryTransformer(graph, recursive, truncate_extension)
        elif isinstance(graph, dict) or isinstance(graph, OrderedDict):
            self.__graph = DictTransformer(graph)
        else:
            raise TypeError(
                'PageRank class must receive '
                'DictTransformer or DirectoryTransformer or directory path or dict or OrderedDict.'
            )

        self.__NX = self.__graph.count()

    def set_epsilon(self, value):
        if value is float and round(value, 5) != 0:
            self.__epsilon = value
            return self

        raise TypeError('Epsilon must be a float and have a least one not null decimal digit for the first 5 digits.')

    def get_epsilon(self):
        return self.__epsilon

    def references_matrix(self):
        """
        1. Make matrix filled with zeros
        2. Get nodes with order numbers
        3. Attach weight to each matrix field

        :return: matrix
        """

        references_matrix = matrix(zeros((self.__NX, self.__NX)))

        nodes_numbers = self.__graph.nodes_with_number()

        for predecessor, successors in self.__graph.make_graph().adj.items():
            for successor, edge_data in successors.items():
                references_matrix[nodes_numbers[predecessor], nodes_numbers[successor]] = edge_data['weight']

        return references_matrix

    def markov_chain(self):
        """
        1. Get matrix with references from the given graph
        2. Make uniform probability matrix E
        3. Add matrix with graph's references T to L (L = T + eE) e is needed to make sure that
           markov chain wont be trapped in a circle
        4. Sum al values in each L's row and divide the row by the sum to make sure that all
           values in a row sums to 1, another words make a stochastic matrix G (Markov chain)

        :return: matrix
        """

        T = self.references_matrix()
        E = ones(T.shape)/self.__NX
        L = T + E * self.__epsilon
        G = matrix(zeros(L.shape))

        for i in range(self.__NX):
            G[i, :] = L[i, :] / sum(L[i, :])

        return G

    def calculate_ranks(self):
        """
        1. Make initial vector
        2. Get Markov chain with calculated parameters from the graph
        3. Product markov chain with initial vector till the vector stop changing

           init_vector(ranks_vector(0)) * markov chain = ranks_vector(1)
           ranks_vector(1) * markov chain = ranks_vector(2)
           ranks_vector(2) * markov chain = ranks_vector(3)
           etc

        :return: matrix
        """

        ranks_vector = random(self.__NX)
        ranks_vector /= sum(ranks_vector)

        G = self.markov_chain()

        check_point = False
        check_point_index = False

        for __ in range(100):
            ranks_vector = dot(ranks_vector, G)

            if not isinstance(check_point, bool) and not isinstance(check_point_index, bool):
                if round(check_point, 5) == round(ranks_vector[0, check_point_index], 5):
                    break

            if not isinstance(check_point_index, bool):
                check_point = ranks_vector[0, check_point_index]

            if isinstance(check_point_index, bool):
                for i in range(ranks_vector.shape[1]):
                    if round(ranks_vector[0, i], 5) > self.__epsilon:
                        check_point_index = i
                        check_point = ranks_vector[0, i]
                        break

        return ranks_vector

    def page_rank(self):
        """
        Attach ranks to nodes

        :return: dict
        """

        ranks = self.calculate_ranks().tolist()[0]
        nodes = self.__graph.nodes()

        page_rank = OrderedDict([])

        for i in range(self.__NX):
            page_rank[nodes[i]] = ranks[i]

        return page_rank

    def sorted_page_rank(self, reverse=True):
        return OrderedDict(sorted(self.page_rank().items(), key=lambda x: x[1], reverse=reverse))
