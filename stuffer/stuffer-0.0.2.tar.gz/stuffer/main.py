import logging
import os
from pathlib import Path

import sys

from stuffer import content
from stuffer import debconf
from stuffer import docker


os.environ['LANG'] = 'C.UTF-8'
os.environ['LC_ALL'] = 'C.UTF-8'

from stuffer import click

from stuffer import apt
from stuffer import configuration
from stuffer import contrib
from stuffer import files
from stuffer import pip
from stuffer import store
from stuffer import system
from stuffer import user
from stuffer import utils
from stuffer.core import Action


def command_script(file_path, operations):
    if operations:
        if file_path:
            raise click.UsageError("Cannot pass both --file/-f and operations on command line")
        return "\n".join(operations) + "\n"
    logging.info("Reading commands from %s", file_path)
    with open(file_path) as f:
        contents = f.read()
        logging.info("Read %d bytes from %s", len(contents), file_path)
        return contents


def script_substance(contents):
    all_lines = contents.splitlines()
    no_comments = [line for line in all_lines if not line.startswith('#')]
    return "\n".join([line for line in no_comments if line.strip()] + [''])


@click.command()
@click.option("--file", "-f", 'file_path')
@click.option("--log-file", "-l", 'log_file', default="/var/log/stuffer.log")
@click.option("--store-dir", "-s", 'store_dir', default="/var/lib/stuffer/store")
@click.option('--verbose', '-v', is_flag=True)
@click.option('--version', '-V', is_flag=True)
@click.argument("operations", nargs=-1)
def cli(file_path, log_file, store_dir, verbose, version, operations):
    setup_logging(log_file, verbose)
    if version:
        click.echo("0.0.1")
        return

    configuration.config.store_directory = Path(store_dir)

    script = command_script(file_path, operations)
    logging.debug("Read script:\n%s", script)
    full_command = script_substance(script)
    logging.debug("Script substance:\n%s", full_command)
    action_namespace = {'apt': apt, 'configuration': configuration, 'content': content, 'contrib': contrib,
                        'debconf': debconf, 'docker': docker, 'files': files, 'pip': pip, 'store': store,
                        'system': system, 'user': user, 'utils': utils,
                        '__name__': __name__}
    if file_path:
        action_namespace['__file__'] = file_path
    if not Action.tmp_dir().is_dir():
        Action.tmp_dir().mkdir(parents=True)
    exec(full_command, action_namespace)

    actions = list(Action.registered())
    logging.info("Loaded %d actions: %s", len(actions), ', '.join(map(repr, actions)))
    for act in actions:
        act.execute()


def setup_logging(log_file, verbose):
    logging.basicConfig(filename=log_file, filemode='a', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s : %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if verbose else logging.INFO)
    formatter = logging.Formatter('%(levelname)-8s : %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


if __name__ == '__main__':
    sys.exit(cli())
