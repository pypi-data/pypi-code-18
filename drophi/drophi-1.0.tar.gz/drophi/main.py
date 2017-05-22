import argparse
import logging
import pprint

import drophi.client

LOGGER = logging.getLogger(__name__)

def setup_log(level=logging.INFO):
    logging.basicConfig(level=level, format="[%(asctime)s] %(levelname)s pid:%(process)d %(name)s:%(lineno)d %(message)s")

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help="Show more verbose logging")

    subparsers = parser.add_subparsers(help='The command to perform')

    parser_ps = subparsers.add_parser('ps', help='Show the running containers')
    parser_ps.set_defaults(command=_ps)

    args = parser.parse_args()

    setup_log(level=logging.DEBUG if args.verbose else logging.INFO)

    client = drophi.client.Client()

    return args.command(args, client) or 0

def _ps(args, client):
    LOGGER.info("Running ps")
    pprint.pprint(client.ps())
