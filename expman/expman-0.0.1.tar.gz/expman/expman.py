"""
Expman

Experiment management library for machine learning.
"""

import uuid
import os
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pprint import pformat
from expman.experiment import Experiment
from expman.listing import Listing


HEADER = """
****************************************
*
* Running experiment {name}
*
****************************************
The configuration for Expman is:
{expman_args}

The following environment variables have been set:
{envs}

The configuration for the experiment is:
{exp_args}
"""


def run_new(args, exp_args):
    exp_args = exp_args[1:]
    exp = Experiment(vars(args), exp_args)
    print(HEADER.format(**{k: pformat(v) if isinstance(v, dict) else v for k, v in exp.config.items()}, name=exp.name, envs=pformat(exp.envs)))
    exp.run()


def run_rerun(args):
    exp = Experiment.load(args.dir)
    exp.expman_args['force'] = False
    exp.run()


def run_clean(args):
    print('cleaning')
    for root, dirs, files in os.walk(args.dir):
        for ext in args.ext:
            match = [os.path.join(root, f) for f in files if os.path.splitext(f)[-1] == ext]
            if len(match) > args.keep:
                earliest_to_latest = sorted(
                    match,
                    key=lambda f: os.path.getmtime(f)
                )
                for fdelete in earliest_to_latest[:-args.keep]:
                    print('Removing {}'.format(fdelete))
                    if not args.dry:
                        os.remove(fdelete)


def run_list(args):
    listing = Listing(args.dir)
    listing.print_listings()
    if args.db:
        db = listing.create_db(args.db)
    if args.interactive:
        print()
        print('>>> The variable "listing" contains the listing object')
        print('>>> The variable "db" contains the listing database, with the "experiments" table containing the experiments')
        print()
        import code
        code.interact(local=locals())


def main():
    """
    Implementation of the expman executable
    """
    rand_str = str(uuid.uuid4().hex.upper()[0:8])
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    sub_parsers = parser.add_subparsers(title='command', dest='command')

    new_parser = sub_parsers.add_parser('new', help='Create a new experiment', formatter_class=ArgumentDefaultsHelpFormatter)
    new_parser.add_argument('-g', '--gpu', nargs='*', type=int, help='GPUs to use')
    new_parser.add_argument('-n', '--name', default=rand_str, help='Name of the experiment. If this is not given then it defaults to a random string')
    new_parser.add_argument('-d', '--dir', default='experiments', help='where to store the experiments')
    new_parser.add_argument('-f', '--force', action='store_true', help='Whether to overwite existing experiment')

    resume_parser = sub_parsers.add_parser('rerun', help='Resume an experiment', formatter_class=ArgumentDefaultsHelpFormatter)
    resume_parser.add_argument('dir', help='Experiment directory')

    clean_parser = sub_parsers.add_parser('clean', help='Clean up old experiments by removing old files', formatter_class=ArgumentDefaultsHelpFormatter)
    clean_parser.add_argument('ext', nargs='+', help='File extensions to prune')
    clean_parser.add_argument('-k', '--keep', type=int, help='How many most recent files to keep', default=5)
    clean_parser.add_argument('-d', '--dir', default='experiments', help='where the experiments are stored')
    clean_parser.add_argument('--dry', action='store_true', help='Print but do not delete')

    list_parser = sub_parsers.add_parser('list', help='List experiments', formatter_class=ArgumentDefaultsHelpFormatter)
    list_parser.add_argument('-d', '--dir', default='experiments', help='where the experiments are stored')
    list_parser.add_argument('--db', default='', help='If given, a database will be created under this name')
    list_parser.add_argument('-i', '--interactive', action='store_true', help='Whether to go into interactive mode after showing the results')

    args, exp_args = parser.parse_known_args()

    if args.command == 'new':
        if not exp_args or '--' != exp_args[0]:
            print('Error: Missing experiment arguments!')
            parser.print_help()
            sys.exit(1)
        run_new(args, exp_args)
    elif args.command == 'rerun':
        run_rerun(args)
    elif args.command == 'clean':
        run_clean(args)
    elif args.command == 'list':
        run_list(args)
