#
# hepler/algorithms.py
#
# Copyright (c) 2017 Junpei Kawamoto
#
# This file is part of rgmining-script.
#
# rgmining-script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rgmining-script. If not, see <http://www.gnu.org/licenses/>.
#
"""Check which algorithms are installed.

This module exports a constant variable, :data:`ALGORITHMS`,
The ``ALGORITHMS`` is a dictionary mapping an installed algorithm name to a
constructor of the review graph implementing the algorithm.

You can get a set of installed algorithms names by ``ALGORITHMS.keys()``, and
create a review graph by ``ALGORITHMS["name"](params)``.
"""
from logging import getLogger

_LOGGER = getLogger(__name__)
"""Logger.
"""

ALGORITHMS = {}
"""Dictionary of installed algorithms.

Keys are the names of the installed algorithms, and the associated value is
the graph creation function of that dataset.
"""


# Load and register RIA.
try:
    import ria
except ImportError:
    _LOGGER.info("rgmining-ria is not installed.")
else:
    def ignore_args(func):
        """Returns a wrapped function which ignore given arguments."""
        def _(*_args):
            """The function body."""
            return func()
        return _
    ALGORITHMS["ria"] = ria.ria_graph
    ALGORITHMS["one"] = ignore_args(ria.one_graph)
    ALGORITHMS["onesum"] = ignore_args(ria.one_sum_graph)
    ALGORITHMS["mra"] = ignore_args(ria.mra_graph)


# Load and register RSD.
try:
    import rsd  # pylint: disable=wrong-import-position
except ImportError:
    _LOGGER.info("rgmining-rsd is not installed.")
else:
    ALGORITHMS["rsd"] = rsd.ReviewGraph


# Load and register Fraud Eagle.
try:
    import fraud_eagle  # pylint: disable=wrong-import-position
except ImportError:
    _LOGGER.info("rgmining-fraud-eagle is not installed.")
else:
    ALGORITHMS["feagle"] = fraud_eagle.ReviewGraph


# Load and register FRAUDAR.
try:
    import fraudar  # pylint: disable=wrong-import-position
except ImportError:
    _LOGGER.info("rgmining-fraudar is not installed.")
else:
    def create_fraudar_graph(nblock=1):
        """Create a review graph defined in Fraud Eagle package.
        """
        return fraudar.ReviewGraph(int(nblock))
    ALGORITHMS["fraudar"] = create_fraudar_graph


def graph(method, method_param):
    """Create a review graph.

    Args:
      method: name of the method to be run.
      method_param: list of strings representing key-value pairs.

    Returns:
      Graph object.
    """
    # Create a review graph.
    method_param = {key: float(value)
                  for key, value in [v.split("=") for v in method_param]}
    return ALGORITHMS[method](**method_param)
