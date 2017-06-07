import re
from copy import deepcopy
from functools import reduce
from utilofies.stdlib import cached_property
from . import stopwatch


class StringItem:

    token_pattern = re.compile(r"(\w+(?:['’-]\w+)?)", re.U)

    def __init__(self, item, key):
        self.item = item
        self.key = key

    @cached_property
    def value(self):
        """Returns a canonical value to represent the string."""
        string = self.key(self.item)
        for separator in (' - ', ' – ', ' | '):
            string = max(string.split(separator), key=len)
        return set(self.token_pattern.findall(string.lower()))


class StringCluster(list):

    def __init__(self, items):
        super(StringCluster, self).__init__(items)
        self.update_value()

    def update_value(self):
        self.value = reduce(set.__or__, (item.value for item in self))

    @staticmethod
    def _jaccard_distance(set0, set1):
        if set0 == set1:  # Avoid division by zero for empty sets
            return 0
        return 1 - len(set0 & set1) / len(set0 | set1)

    def distance(self, cluster):
        return self._jaccard_distance(self.value, cluster.value)

    def append(self, item):
        super(StringCluster, self).append(item)
        self.update_value()

    def extend(self, cluster):
        super(StringCluster, self).extend(cluster)
        self.update_value()

    @property
    def items(self):
        return [item.item for item in self]


class Clustering:
    """
    Wrapper for clustering methods.

        >>> Clustering.clustered(strings, level=0.8)

    So far they can be used as class methods, but eventually I might put in
    language-dependent stemming and stopword removal, so that the class will
    need to be instantiated with the respective language as parameter.
    """

    @staticmethod
    def _agglomeratively_clustered(clusters, level):
        """Low-level clustering method"""
        clusters = deepcopy(clusters)
        changes = range(len(clusters))
        while changes:
            new_changes = []
            for change in changes:
                if clusters[change] is None:
                    continue
                for i in range(len(clusters)):
                    if change == i or clusters[i] is None:
                        continue
                    if clusters[change].distance(clusters[i]) < level:
                        clusters[change].extend(clusters[i])
                        clusters[i] = None
                        new_changes.append(change)
            changes = new_changes
        return [cluster.items for cluster in clusters if cluster is not None]

    @classmethod
    @stopwatch
    def clustered(cls, iterable, level, key=lambda item: item):
        """
        Clusters members of an interable.

        :param iterable: The iterable to cluster.

        :param level: The distance treshold that determines if two items
            are to be put in a cluster or not. A large value means that
            even not so similar items belong to one cluster, small value
            groups only very similar members. For example: for a set of
            20 members a value of 0.4 produce 7 2-3 item clusters, while
            a value of 0.8 gives 3 5-10 item clusters.

        :param key: (Optional) Like in Python's builtin `sorted` a
            function used to extract the significant value off the item
            to group on. Default: the identity function, only
            practicable for an iterable of strings.
        """

        items = [StringItem(item, key) for item in iterable]
        clusters = [StringCluster([item]) for item in items]
        return cls._agglomeratively_clustered(clusters, level)
