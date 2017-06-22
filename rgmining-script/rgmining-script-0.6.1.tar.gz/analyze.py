#! /usr/bin/env python
#
# analyze.py
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
"""Analyze a dataset by a method.

This command takes two mandatory arguments, dataset and method, in this order.

If you choose ``file`` as the dataset, you can give a file path for the dataset
via --dataset-param flag with ``file`` key.
The --dataset-param flag takes key and value within the format ``KEY=VALUE``,
i.e. if the path of your dataset is ~/path/to/dataset.json,
give --dataset-param file=~/path/to/dataset.json.

If your chosen dataset supports other options, you can also give them via
--dataset-param flags.

Most of methods also take options.
You can give those options via --method-param flag.
The flag takes key and value as same format as --dataset-param,
i.e. to set alpha = 1, give --dataset-param alpha=1.
"""
from __future__ import absolute_import
import logging
import sys

import dsargparse

import dataset_io
import helper


def analyze(graph, output=sys.stdout, loop=20, threshold=10**-5):
    """Execute iteration.

    The iteration ends if the number of iteration reaches the given maximum
    number of iteration, loop, or the update becomes smaller than or equal to
    the given threshold.

    After each iteration ends, the current status of the graph will be outputted
    using :meth:`dataset_io:dataset_io.helper.print_state`.

    Args:
      graph: Review graph object.
      output: Writable object to write outputs.
      loop: Maximum number of iteration (default: 20).
      threshold: Threshold of the update (default: 10^5).
    """
    # Initial summary
    dataset_io.print_state(graph, 0, output)

    # Updates
    logging.info("Start iterations.")
    for i in range(loop):

        diff = graph.update()
        if diff is not None and diff < threshold:
            break

        # Current summary
        logging.info("Iteration %d ends. (diff=%s)", i + 1, diff)
        dataset_io.print_state(graph, i + 1, output)

    # Print final state.
    dataset_io.print_state(graph, "final", output)


def run(method, method_param, dataset, dataset_param, **kwargs):
    """Prepare a review graph, load a dataset to it, and execute analyze.

    Args:
      method: name of the method to be run.
      method_param: list of strings representing key-value pairs.
      dataset: name of the dataset to be loaded.
      dataset_param: list of strings representing key-value pairs.
    """
    graph = helper.graph(method, method_param)
    analyze(helper.load(graph, dataset, dataset_param), **kwargs)


def main():
    """Main function.
    """
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    parser = dsargparse.ArgumentParser(main=main)

    # Dataset
    parser.add_argument(
        "dataset", choices=sorted(helper.DATASETS.keys()),
        help=(
            "choose one dataset to be analyzed.\n"
            "If choose `file`, give a file path via dataset-param with file key\n"
            "i.e. --dataset-param file=<path>."))
    parser.add_argument(
        "--dataset-param", action="append", default=[], dest="dataset_param",
        help=(
            "key and value pair which are connected with '='.\n"
            "This option can be set multiply."))

    # Algorithm
    parser.add_argument(
        "method", choices=sorted(helper.ALGORITHMS.keys()),
        help="choose one method.")
    parser.add_argument(
        "--method_param", action="append", default=[],
        help=(
            "key and value pair which are connected with '='.\n"
            "This option can be set multiply."))
    parser.add_argument(
        "--loop", type=int, default=20,
        help="At most the given number of iteration will be run (default: 20).")
    parser.add_argument(
        "--threshold", type=float, default=10 ^ -5,
        help=(
            "Loop ends the update will be smaller than the given number "
            "(default: 10^-5)."))

    # Output configuration
    parser.add_argument(
        "--output", default=sys.stdout,
        type=dsargparse.FileType("w"),  # pylint: disable=no-member
        help="file path to store results (Default: stdout).")

    # Run
    try:
        return run(**vars(parser.parse_args()))
    except KeyboardInterrupt:
        return "Canceled"
    except Exception as e:  # pylint: disable=broad-except
        logging.exception("Untracked exception occurred.")
        return e.message
    finally:
        logging.shutdown()


if __name__ == "__main__":
    main()
