"""Tool to create jobs to carry out analyses on datasets."""

import os
import argparse

from dtoolcore import DataSet

from jobarchitect.utils import (
    split_iterable,
    are_identifiers_in_dataset
)

from jobarchitect.backends import (
    JobSpec,
    generate_bash_job,
    generate_docker_job,
    generate_singularity_job,
    render_script,
)


def generate_jobspecs(
        tool_path,
        dataset_path,
        output_root,
        nchunks,
        image_name=None,
        identifiers=None
        ):
    """Return generator yielding instances of :class:`jobarchitect.JobSec`.

    :param tool_path: path to tool
    :param dataset_path: path to input dataset
    :param output_root: path to output root
    :param nchunks: number of chunks the job should be split into
    :param image_name: container image name
    :returns: generator yielding instances of :class:`jobarchitect.JobSec`
    """
    dataset = DataSet.from_path(dataset_path)

    if not identifiers:
        identifiers = dataset.identifiers

    for identifiers_chunk in split_iterable(identifiers, nchunks):

        yield JobSpec(
            tool_path,
            dataset_path,
            output_root,
            identifiers_chunk,
            image_name=image_name
        )


class JobSketcher(object):
    """Class to build up jobs to analyse a dataset."""

    def __init__(
            self,
            tool_path,
            dataset_path,
            output_root,
            image_name=None
            ):
        self.tool_path = tool_path
        self.dataset_path = dataset_path
        self.output_root = output_root
        self.image_name = image_name

    def _generate_jobspecs(self, nchunks, identifiers):
        for jobspec in generate_jobspecs(self.tool_path,
                                         self.dataset_path,
                                         self.output_root,
                                         nchunks,
                                         image_name=self.image_name,
                                         identifiers=identifiers):
            yield jobspec

    def sketch(self, backend, nchunks, identifiers):
        """Return generator yielding instances of :class:`jobarchitect.JobSec`.

        :param backend: backend function for generating job scripts
        :param nchunks: number of chunks the job should be split into
        :param identifiers: identifiers to create jobs for
        :returns: generator yielding jobs as strings
        """

        if not are_identifiers_in_dataset(self.dataset_path, identifiers):
            raise(KeyError(
                "One or more supplied identifiers are not in the dataset."
            ))

        for jobspec in self._generate_jobspecs(nchunks, identifiers):
            yield backend(jobspec)


def identifiers_where_overlay_is_true(dataset, overlay_name):

    overlays = dataset.access_overlays()

    overlay = overlays[overlay_name]

    selected = [identifier
                for identifier in dataset.identifiers
                if overlay[identifier]]

    return selected


def sketchjob(tool_path, dataset_path, output_root,
              backend, nchunks, image_name=None,
              overlay_filter=None):
    """Return list of jobs as strings.

    :param tool_path: path to tool
    :param dataset_path: path to input dataset
    :param output_root: path to output root
    :param backend: backend function for generating job scripts
    :param nchunks: number of chunks the job should be split into
    :returns: generator yielding jobs as strings
    """
    dataset = DataSet.from_path(dataset_path)

    if overlay_filter is not None:

        overlays = dataset.access_overlays()
        if overlay_filter not in overlays:
            raise ValueError("Overlay {} not found".format(overlay_filter))
        identifiers = identifiers_where_overlay_is_true(
            dataset, overlay_filter)
    else:
        identifiers = dataset.identifiers

    jobsketcher = JobSketcher(
        tool_path=tool_path,
        dataset_path=dataset_path,
        output_root=output_root,
        image_name=image_name)

    for job in jobsketcher.sketch(backend, nchunks, identifiers):
        yield job


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tool_path", help="Path to 'smart' tool")
    parser.add_argument("dataset_path", help="Path to dataset to be analysed")
    parser.add_argument(
        "output_path",
        help="Path to where output will be written")
    parser.add_argument(
        "-n",
        "--nchunks",
        default=1,
        type=int,
        help="Number of chunks the job should be split up into")
    backend_function_map = {'docker': generate_docker_job,
                            'singularity': generate_singularity_job,
                            'bash': generate_bash_job}
    wrapper_script_map = {'slurm-single': "slurm_script_single.slurm.j2",
                          'slurm-multiple': "slurm_script_multiple.slurm.j2",
                          'bash': "basic_bash_script.sh.j2"}
    parser.add_argument(
        "-b",
        "--backend",
        choices=backend_function_map.keys(),
        default='bash')
    parser.add_argument(
        "-i",
        "--image-name")
    parser.add_argument(
        "-s",
        "--wrapper-script",
        choices=wrapper_script_map.keys(),
        default='bash')
    parser.add_argument(
        "--overlay-filter",
        default=None,
        help="Overlay to use to filter identifiers to process. Only those \
              identifiers where the overlay for that identifier has the \
              value True will be processed.")
    args = parser.parse_args()

    tool_path = os.path.abspath(args.tool_path)
    if not os.path.isfile(tool_path):
        parser.error("Job description file does not exist: {}".format(
            tool_path))

    if not os.path.isdir(args.dataset_path):
        parser.error("Dataset path does not exist: {}".format(
            args.dataset_path))

    if args.backend in ['docker', 'singularity']:
        if args.image_name is None:
            parser.error("""You must specify an image to use a container based
backend ({})""".format(args.backend))

    jobs = list(sketchjob(tool_path,
                          args.dataset_path,
                          args.output_path,
                          backend_function_map[args.backend],
                          args.nchunks,
                          args.image_name,
                          args.overlay_filter))

    script = render_script(
        wrapper_script_map[args.wrapper_script],
        {"jobs": jobs, "partition": "rg-mh", "jobmem": 4000})
    print(script)
