"""Jobarchitect agent."""

import os
import json
import argparse
import subprocess

from jobarchitect.utils import (
    path_from_hash,
    output_path_from_hash,
    tmp_dir_context,
)


class Agent(object):
    """Class to create commands to analyse data."""

    def __init__(
        self,
        cwl_tool_wrapper_path,
        dataset_path,
        output_root="/tmp"
    ):
        self.cwl_tool_wrapper_path = os.path.abspath(cwl_tool_wrapper_path)
        self.dataset_path = dataset_path
        self.output_root = output_root

    def run_analysis(self, hash_str):
        """Run the analysis on an item in the dataset.

        :param hash_str: dataset item identifier as a hash string
        """
        cwl_job_description = self.create_cwl_job(hash_str)
        with tmp_dir_context() as d:
            job_filename = os.path.join(d, 'cwl_job.json')
            with open(job_filename, 'w') as fh:
                json.dump(cwl_job_description, fh)

            # cwltool is not python3.5 compatible therefore we need to make
            # sure it gets run with python2
            which_cwltool_output = subprocess.check_output(
                ['which', 'cwltool'])
            cwltool_path = which_cwltool_output.decode('utf-8').strip()

            command = ['python2', cwltool_path, '--quiet',
                       self.cwl_tool_wrapper_path, job_filename]

            subprocess.call(command, cwd=self.output_root)

    def create_cwl_job(self, hash_str):
        """Run the analysis on an item in the dataset.

        :param hash_str: dataset item identifier as a hash string
        :returns: dictionary defining job
        """

        input_file = path_from_hash(self.dataset_path, hash_str)
        output_file = output_path_from_hash(
            self.dataset_path, hash_str, '.')
        return dict(
            input_file={"class": "File", "path": input_file},
            output_file=output_file
        )


def analyse_by_identifiers(
        cwl_tool_wrapper_path, dataset_path, output_root, identifiers):
    """Run analysis on identifiers.

    :param cwl_tool_wrapper_path: path to cwl tool wrapper
    :param dataset_path: path to input dataset
    :param output_root: path to output root
    :identifiers: list of identifiers
    """
    agent = Agent(cwl_tool_wrapper_path, dataset_path, output_root)
    for i in identifiers:
        agent.run_analysis(i)


def cli():
    """Command line interface for _analyse_by_ids"""

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--cwl_tool_wrapper_path', required=True)
    parser.add_argument('--input_dataset_path', required=True)
    parser.add_argument('--output_root', required=True)
    parser.add_argument('identifiers', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    analyse_by_identifiers(
        args.cwl_tool_wrapper_path,
        args.input_dataset_path,
        args.output_root,
        args.identifiers)
