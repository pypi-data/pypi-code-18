import argparse
import asyncio
import logging
import os
import subprocess
import sys

import aiohttp
import maxillo.definitions
import maxillo.listener
import maxillo.git
import maxillo.setup
import maxillo.web.slave
import maxillo.web.master

LOGGER = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose logging")
    parser.add_argument('--pdb', action='store_true', help='Enable debugging when things go wrong')

    subparsers = parser.add_subparsers(help='The command to perform')

    parser_setup = subparsers.add_parser('setup', help="Set up your maxillo-based swarm")
    parser_setup.set_defaults(command=setup)

    parser_slave = subparsers.add_parser('slave', help='Run the webapp')
    parser_slave.add_argument('--host', default=None, help="The host to connect to")
    parser_slave.set_defaults(command=slave)

    parser_setup_master = subparsers.add_parser('setup-master', help='Set up the maxillo master')
    parser_setup_master.add_argument('hostname', help='The hostname where this master should be reached')
    parser_setup_master.add_argument('email', help='The email address to use when registering for SSL certs')
    parser_setup_master.add_argument('password', help='The password used to log in to the website. Your username is the email for your SSL cert')
    parser_setup_master.add_argument('--staging', action='store_true', help='If present, get an SSL cert from staging')
    parser_setup_master.set_defaults(command=setup_master)

    parser_master = subparsers.add_parser('master', help='Run the webapp')
    parser_master.set_defaults(command=master)

    parser_local_definition = subparsers.add_parser('local-definition', help='Set up a swarm from a local definition')
    parser_local_definition.add_argument('source', help='The directory with the source to use in the definition')
    parser_local_definition.set_defaults(command=local_definition)

    parser_populate = subparsers.add_parser('populate-volume', help='For internal use to populate config files')
    parser_populate.add_argument('filename', help='The file name to populate')
    parser_populate.add_argument('content', help='The content to populate')
    parser_populate.set_defaults(command=populate)

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    if args.pdb:
        def excepthook(_type, value, tb):
            import pdb
            import traceback
            traceback.print_exception(_type, value, tb)
        sys.excepthook = excepthook
        LOGGER.info("Installed pdb hook on exception")
    if not hasattr(args, 'command'):
        LOGGER.error("You must select a command to run")
        parser.print_help()
        return 1

    if args.command in (master, slave):
        return args.command(args)
    else:
        coro = args.command(args)
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)

async def setup(args):
    LOGGER.info("Setting up maxillo")
    if not os.path.exists('/var/run/docker.sock'):
        raise Exception(
            "Could not find /var/run/docker.sock so I can't communicate with docker. "
            "Please run this container with '-v /var/run/docker.sock:/var/run/docker.sock' "
            "to give this program the ability to control docker"
        )

async def setup_master(args):
    LOGGER.info("Setting up maxillo master")
    maxillo.setup.master(args.hostname, args.email, args.password)

async def _create_session():
    return aiohttp.ClientSession()

def slave(args):
    LOGGER.info("Running maxillo slave")
    loop = asyncio.get_event_loop()
    session = loop.run_until_complete(_create_session())
    exit_event = asyncio.Event()
    listener_queue, listen_task = maxillo.listener.initialize(exit_event, session, args.host)
    maxillo.web.slave.run(exit_event, listener_queue, listen_task, session, args.host)
    session.close()

async def populate(args):
    with open(args.filename, 'w') as f:
        f.write(args.content)
    LOGGER.info("Wrote %s with %d bytes", args.filename, len(args.content))

def master(args):
    LOGGER.info("Running maxillo master")
    maxillo.git.configure()
    maxillo.web.master.run()

async def local_definition(args):
    source = args.source
    LOGGER.info("Setting up local defintion from %s", source)
    try:
        await maxillo.definitions.source(source)
    except maxillo.definitions.LoadError as e:
        return None
