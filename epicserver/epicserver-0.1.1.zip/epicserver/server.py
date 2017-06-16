#!/usr/bin/env python3

from .log import system_log as _log, formatter
from . import __version__
from .utils import load_module
from .scheduler import scheduler
from .objects import Pool
from .databases import autodetect as autodetect_db
from .encoders import autodetect as autodetect_encoder
from .log import log_filter, print_logger, LogLevel

import importlib
import logging
import socket
import sys


log = _log.getChild('server')


def main(argv=sys.argv[1:]):
    from argparse import ArgumentParser, OPTIONAL
    args = ArgumentParser()
    
    args.add_argument('-i', '--identity', default=socket.getfqdn(),
        help="ID to uniquely identify the server (Default: fqdn (%(default)s))")
    args.add_argument('-d', '--debug', action='count', default=0,
        help="Invoke a debugger on program crash, specify twice to start in a debugger")
    args.add_argument('-v', '--verbose', default=0, action='count', dest='verbosity',
        help="Increase the verbosity of logging, can be specified multiple times")
    args.add_argument('--version', action='version', version=__version__)
    args.add_argument('-e', '--encoder', default="pickle://",
        help="Encoder used to save files to the database (Default: %(default)s)")
    args.add_argument('db', default='dbm://objects.db', nargs=OPTIONAL,
        help="Database to persist objects to/from (Default: %(default)s)")
    args.add_argument('module',
        help="Entry point of the code to run on the grid")


    options = args.parse_args(argv)

    if options.debug >= 1:
        def pdb_handler(*tb):
            import pdb
            log.exception("*" * 20 + " Error " + "*" * 20, exc_info=tb)
            print("==== PDB =====", file=sys.stderr)
            pdb.pm()
        sys.excepthook = pdb_handler

    if options.debug >= 2:
        import pdb
        pdb.set_trace()

    level = {1: logging.CRITICAL,
             2: logging.ERROR,
             3: logging.WARNING,
             4: logging.INFO,
             5: logging.DEBUG,
            }.get(options.verbosity, logging.DEBUG)
    filter_level = {1: LogLevel.exception,
                    2: LogLevel.error,
                    3: LogLevel.warn,
                    4: LogLevel.info,
                    5: LogLevel.debug,
                   }.get(options.verbosity, LogLevel.debug)
    # higher performance logging abstraction for game code
    logger = log_filter(filter_level, print_logger)
        
    if options.verbosity:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        _log.addHandler(handler)
        _log.setLevel(level)
        
    log.info("Logging initialized")

    log.info("Loading entry point")
    try:
        entry_point = load_module(options.module)
    except ValueError:
        log.error('Function name not specified')
        sys.exit(1)
    except ModuleNotFoundError as err:
        log.error(f'Could not locate module: {err.name}')
        sys.exit(1)
    except AttributeError:
        log.error('Function not found in module')
        sys.exit(1)

    log.info("Loading object encoder")
    try:
        encoder = autodetect_encoder(options.encoder)
    except ValueError:
        log.error("Unable to locate encoder from connection string")
        sys.exit(1)

    log.info("Loading object db")
    try:
        db = autodetect_db(options.db)
        db.encoder = encoder
    except ValueError:
        log.error("Unable to detect database type from connection string")
        sys.exit(1)

    log.info("Setting up object Pool")
    pool = Pool(db)

    try:
#        scheduler(entry_point(options.identity))
        scheduler(entry_point, pool, db, logger)
    except KeyboardInterrupt:
        print("User requested exit", file=sys.stderr)

if __name__ == "__main__":
    main()
