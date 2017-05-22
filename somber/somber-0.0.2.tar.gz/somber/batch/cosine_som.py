import logging
import numpy as np

from somber.utils import expo, linear, static
from somber.batch.som import Som as Base_Som


logger = logging.getLogger(__name__)


class CosineSom(Base_Som):
    """
    This is the batched version of the basic SOM class.
    """

    def __init__(self,
                 map_dim,
                 weight_dim,
                 learning_rate,
                 lrfunc=expo,
                 nbfunc=expo,
                 sigma=None):
        """
        :param map_dim: A tuple of map dimensions, e.g. (10, 10) instantiates a 10 by 10 map.
        :param weight_dim: The data dimensionality.
        :param learning_rate: The learning rate, which is decreases according to some function
        :param lrfunc: The function to use in decreasing the learning rate. The functions are
        defined in utils. Default is exponential.
        :param nbfunc: The function to use in decreasing the neighborhood size. The functions
        are defined in utils. Default is exponential.
        :param sigma: The starting value for the neighborhood size, which is decreased over time.
        If sigma is None (default), sigma is calculated as ((max(map_dim) / 2) + 0.01), which is
        generally a good value.
        """

        super().__init__(map_dim=map_dim,
                         weight_dim=weight_dim,
                         learning_rate=learning_rate,
                         lrfunc=lrfunc,
                         nbfunc=nbfunc,
                         sigma=sigma,
                         min_max=np.argmax)

    def batch_distance(self, x, weights):
        """
        batched version of the euclidean distance.

        :param x: The input
        :param weights: The weights
        :return: A matrix containing the distance between each
        weight and each input.
        """

        norm = np.sqrt(np.sum(np.square(x), axis=1))
        nonzero = norm > 0
        norm_vectors = np.zeros_like(x)
        norm_vectors[nonzero] = x[nonzero] / norm[nonzero, np.newaxis]

        w_norm = np.sqrt(np.sum(np.square(weights), axis=1))
        nonzero = w_norm > 0
        w_norm_vectors = np.zeros_like(weights)
        w_norm_vectors[nonzero] = weights[nonzero] / w_norm[nonzero, np.newaxis]

        res = np.dot(norm_vectors, w_norm_vectors.T)
        return res

    def _get_bmus(self, x):
        """
        Gets the best matching units, based on euclidean distance.

        :param x: The input vector
        :return: The activations, which is a vector of map_dim, and
         the distances between the input and the weights, which can be
         reused in the update calculation.
        """

        diff = self._distance_difference(x, self.weights)
        distance = self.batch_distance(x, self.weights)

        return distance, diff

    def _distance_difference(self, x, weights):
        """
        Calculates the difference between an input and all the weights.

        :param x: The input.
        :param weights: An array of weights.
        :return: A vector of differences.
        """

        return np.array([v - weights for v in x])

if __name__ == "__main__":

    s = CosineSom((20, 20), 3, 1.0)
    s.trained = True
    s.weights += 0
    # s_2 = Base_Som((10, 10), 3, 1.0)