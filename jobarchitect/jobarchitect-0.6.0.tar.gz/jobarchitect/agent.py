"""Jobarchitect agent."""

import os
import json
import argparse
import subprocess

from jobarchitect.utils import (
    path_from_hash,
    output_path_from_hash,
    mkdir_parents
)


class Agent(object):
    """Class to create commands to analyse data."""

    def __init__(
        self,
        tool_path,
        dataset_path,
        output_root="/tmp"
    ):
        self.tool_path = os.path.abspath(tool_path)
        self.dataset_path = dataset_path
        self.output_root = output_root


    def run_tool_on_identifier(self, identifier):
        """Run the tool on an item in the dataset."""
        output_path = output_path_from_hash(
            self.dataset_path, identifier, self.output_root)
        mkdir_parents(output_path)
        cmd = ["python",
               self.tool_path,
               "--dataset-path", self.dataset_path,
               "--identifier", identifier,
               "--output-directory", output_path]
        subprocess.call(cmd)


def analyse_by_identifiers(
        tool_path, dataset_path, output_root, identifiers):
    """Run analysis on identifiers.

    :param tool_path: path to tool
    :param dataset_path: path to input dataset
    :param output_root: path to output root
    :identifiers: list of identifiers
    """
    agent = Agent(tool_path, dataset_path, output_root)
    for i in identifiers:
        agent.run_tool_on_identifier(i)


def cli():
    """Command line interface for _analyse_by_ids"""

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--tool_path', required=True)
    parser.add_argument('--input_dataset_path', required=True)
    parser.add_argument('--output_root', required=True)
    parser.add_argument('identifiers', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    analyse_by_identifiers(
        args.tool_path,
        args.input_dataset_path,
        args.output_root,
        args.identifiers)
