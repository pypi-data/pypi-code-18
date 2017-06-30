from __future__ import print_function

import time
import itertools
from datetime import datetime, timedelta
from tabulate import tabulate
import getpass
import click
from .client import Client, config, UnAuthorizedException
from .utils import datestr, truncate, setup_logger, PY2
from . import __version__

if PY2:
    # In Python 2, the input function takes in the input and evaluates it.
    # To equivalant of Python3's input function is raw_input in Python2.
    input = raw_input

# initialized in cli
client = None

class CatchAllExceptions(click.Group):
    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except Exception as exc:
            click.echo('ERROR %s' % exc)

@click.group(cls=CatchAllExceptions)
@click.version_option(version=__version__)
@click.option("--verbose", is_flag=True, default=False, help="Enable verbose logging")
def cli(verbose=False):
    """rorocloud is the command-line interface to the rorocloud service.
    """
    global client
    client = Client()
    setup_logger(verbose=verbose)

@cli.command()
def help():
    """Show this help message."""
    cli.main(args=[])


@cli.command()
def version():
    """Prints the version of rorocloud client."""
    cli.main(args=["--version"])


@cli.command()
def login():
    """Log into rorocloud service.
    """
    try:
        email = input("E-mail: ")
        pw = getpass.getpass("Password: ")
        client.login(email, pw)
    except UnAuthorizedException:
        print('Login failed')


@cli.command()
def whoami():
    """prints the details of current user.
    """
    user = client.whoami()
    print(user['email'])


@cli.command(context_settings={"allow_interspersed_args": False})
@click.argument("command", nargs=-1)
@click.option("-i", "--instance", default="C1",
    help="instance type to run the job on, Available instance types C1 and C2"
)
@click.option("--gpu", "instance", flag_value="G1",
    help="runs the job on GPU instance type"
)
@click.option("--docker-image", default="rorodata/sandbox",
    help="docker image to use to run the job (experimental)"
)
@click.option("-w", "--workdir")
@click.option("--foreground", default=False, is_flag=True)
def run(command, shell=None, instance=None, workdir=None, foreground=False, docker_image=None):
    """Runs a command in the cloud.

    Typical usage:

        rorocloud run python myscript.py
    """
    _run(command, shell=shell, instance=instance, workdir=workdir, foreground=foreground, docker_image=docker_image)

def _run(command, shell=None, instance=None,workdir=None, foreground=False, docker_image=None):
    job = client.run(command, instance=instance, shell=shell, workdir=workdir, docker_image=docker_image)
    print("created new job", job.id)
    if foreground:
        _logs(job.id, follow=True)
    return job


@cli.command(name="run:notebook")
@click.option("-i", "--instance", default="C1",
    help="instance type to run the job on, Available instance types C1 and C2"
)
@click.option("--gpu", "instance", flag_value="G1",
    help="runs the job on GPU instance type"
)
@click.option("--docker-image", default="rorodata/sandbox",
    help="docker image to use to run the job (experimental)"
)
@click.option("-w", "--workdir")
def run_notebook(**kwargs):
    """Starts jupyter notebook.

    The notebooks will be saved in /data/notebooks directory.
    """
    job = _run(["/opt/rorodata/jupyter-notebook"], **kwargs)
    _logs(job.id, follow=True, end_marker="-" * 40)


@cli.command()
@click.option("-a","--all", default=False, is_flag=True)
def status(all=False):
    """Shows the status of recent jobs.
    """
    jobs = client.jobs(all=all)
    rows = []
    for job in jobs:
        start = _parse_time(job.start_time)
        end = _parse_time(job.end_time)
        total_time = (end - start)
        total_time = timedelta(total_time.days, total_time.seconds)
        rows.append([job.id, job.status, datestr(start), str(total_time), job.instance_type, truncate(job.command, 50)])
    print(tabulate(rows, headers=['JOBID', 'STATUS', 'WHEN', 'TIME', 'INSTANCE TYPE', 'CMD']))

def _parse_time(timestr):
    if not timestr:
        return datetime.utcnow()
    try:
        return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")

@cli.command()
@click.option("-f", "--follow", default=False, is_flag=True)
@click.option("-t", "--show-timestamp", default=False, is_flag=True)
@click.argument("job_id")
def logs(job_id, follow=False, show_timestamp=False):
    """Prints the logs of a job.
    """
    _logs(job_id, follow=follow, show_timestamp=show_timestamp)

def _display_logs(logs, show_timestamp=False):
    def parse_time(timestamp):
        t = datetime.fromtimestamp(timestamp//1000)
        return t.isoformat()

    if show_timestamp:
        log_pattern = "[{timestamp}] {message}"
    else:
        log_pattern = "{message}"

    for line in logs:
        line['timestamp'] = parse_time(line['timestamp'])
        print(log_pattern.format(**line))


def _logs(job_id, follow=False, show_timestamp=False, end_marker=None):
    """Shows the logs of job_id.
    """
    def get_logs(job_id, follow=False):
        if follow:
            seen = 0
            while True:
                response = client.get_logs(job_id)
                logs = response.get('logs', [])
                for log in logs[seen:]:
                    yield log
                seen = len(logs)
                job = client.get_job(job_id)
                if job.status in ['success', 'cancelled', 'failed']:
                    break
                time.sleep(0.5)
        else:
            response = client.get_logs(job_id)
            logs = response.get("logs") or []
            for log in logs:
                yield log


    logs = get_logs(job_id, follow)
    if end_marker:
        logs = itertools.takewhile(lambda log: not log['message'].startswith(end_marker), logs)

    _display_logs(logs, show_timestamp=show_timestamp)

@cli.command()
@click.argument("job_id")
def stop(job_id):
    """Stops a job.
    """
    client.stop_job(job_id)

@cli.command()
@click.argument("source")
@click.argument("target")
def put(source, target):
    """Copies a file from the local mahcine into the cloud.

    Usage:

        rorocloud put helloworld.py /data/helloworld.py
    """
    return client.put_file(source, target)

def main():
    cli()

def main_dev():
    config["ROROCLOUD_URL"] = "http://rorocloud-api.local.rorodata.com:8080/"
    cli()
