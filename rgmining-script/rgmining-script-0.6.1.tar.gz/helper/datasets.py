#
# hepler/datasets.py
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
# pylint: disable=import-error
"""Check which datasets are installed.

This module exports a constant variable, :data:`DATASETS`,
The ``DATASETS`` is a dictionary of which a key is the name of a dataset
installed, and of which the associated value is the loading function of the
dataset.

You can get a set of installed dataset names by ``DATASETS.keys()``, and
load a dataset by ``DATASETS["name"](graph)``.
"""
import functools
from logging import getLogger

import dataset_io

_LOGGER = getLogger(__name__)
"""Logger.
"""

DATASETS = {}
"""Dictionary of installed datasets.

Keys are the names of the installed datasets, and the associated values are
load function of that dataset.
"""

def ignore_kwargs(func):
    """Decorator to ignore kwargs.
    """
    @functools.wraps(func)
    def decorated_func(*args, **_kwargs):
        """Decorated function which ignore kwargs and run the wrapped function.
        """
        return func(*args)
    return decorated_func


# Load and register the synthetic dataset.
try:
    import synthetic  # pylint: disable=wrong-import-position
except ImportError:
    _LOGGER.info("rgmining-synthetic-dataset is not installed.")
else:
    DATASETS["synthetic"] = ignore_kwargs(synthetic.load)


# Load and register Amazon dataset.
# The loader of the Amazon dataset takes one argument, categories,
# to specify which reviews will be loaded.
try:
    import amazon  # pylint: disable=wrong-import-position
except ImportError:
    _LOGGER.info("rgmining-amazon-dataset is not installed.")
else:
    DATASETS["amazon"] = amazon.load


# Load and register Trip Advisor dataset.
try:
    import tripadvisor  # pylint: disable=wrong-import-position
except ImportError:
    _LOGGER.info("rgmining-tripadvisor-dataset is not installed.")
else:
    DATASETS["tripadvisor"] = tripadvisor.load


# Register the loader which load a dataset from a file.
# The loder function takes kwargument, fp, where it loads the dataset.
DATASETS["file"] = dataset_io.load


def load(graph, dataset, dataset_param):
    """Load a dataset and return a review graph.

    Args:
      graph: review graph object which the dataset is loaded to.
      dataset: name of the dataset to be loaded.
      dataset_param: list of key-value parameters.

    Returns:
      Review graph object, which is as same as the parameter graph.
    """
    _LOGGER.info("Prepare options for the selected dataset.")
    params = {key: value
              for key, value in [v.split("=") for v in dataset_param]}
    if "file" in params:
        params["fp"] = open(params["file"])
        del params["file"]

    try:
        _LOGGER.info("Load the dataset.")
        DATASETS[dataset](graph, **params)
    finally:
        if "fp" in params:
            params["fp"].close()
    return graph
