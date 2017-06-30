from tempfile import TemporaryDirectory
from pathlib import Path
import shutil

import click

from . import cli
from ..api import api as mtk_api, resource_representation
from ..jobs.calculation import vasp_calculation
from ..jobs.utils import zip_directory


@cli.command()
@click.argument('job')
@click.argument('uuid')
def run(job, uuid):
    print(job, uuid)
    if job == 'calculation':
        calculation = resource_representation('calculations', uuid)
        calculation.get()

        # if rec.data['status'] != 'submitted':
        #     raise ValueError('Can only run a calculation that has been submitted')

        # Implement to get number of cores
        cluster_job = calculation.cluster_job
        cluster_job.get()

        cluster = cluster_job.cluster
        cluster.get()

        # Assemble Vasp Command and check that executables exist
        programs = {program['program']: {'module': program['module'], 'command': program['command']}  for program in cluster.data['programs']}
        for program in ['mpi', 'VASP']:
            if shutil.which(programs[program]['command']) is None:
                raise ValueError('Could not find command %s needed for calculation' % programs[program]['command'])
        vasp_command = [programs['mpi']['command'], '-n', str(cluster_job.data['cores']), programs['VASP']['command']]
        print('Running vasp with command: {}'.format(vasp_command))

        # Check that scratch directory does exist
        scratch_dir = Path(cluster.data['scratch_directory']).expanduser().absolute()
        if not scratch_dir.is_dir():
            raise ValueError('Scratch directory path %s does not exist' % str(scratch_dir))

        zip_filename = '/tmp/example.zip'
        with TemporaryDirectory(dir=str(scratch_dir)) as tempdir:
            calculation.notify_running(Path(tempdir))
            vasp_calculation(calculation.input, tempdir, calculation.previous_calculation, vasp_command=vasp_command)
            zip_directory(zip_filename, tempdir)
        calculation.upload_results(zip_filename)
    else:
        raise ValueError('Unknown job type calculation')
