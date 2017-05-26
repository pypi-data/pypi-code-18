#!/usr/bin/env python
import json
import argparse

import apilisk.printer
from apilisk.runner import Runner
from apilisk.exceptions import ApiliskException
from apilisk.printer import eprint, vprint
from apilisk.apiwatcher_client import ApiwatcherClient
from apilisk.junit_formatter import JunitFormatter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "project", default=None,
        help="Hash of the project."
    )
    parser.add_argument(
        "-d", "--dataset", type=int,
        help="Id of dataset to use. None if not dataset should be used."
    )
    parser.add_argument(
        "-v", "--verbose", type=int, default=1,
        help="0 = no output, 1 = what is being done, 2 = data"
    )
    parser.add_argument(
        "-c", "--config-file", default="~/.apilisk.json",
        help="Path to configuration file."
    )
    parser.add_argument(
        "-j", "--junit", help="Provide output in junit format.",
        action="store_true"
    )
    parser.add_argument(
        "-o", "--junit-output-file", help="Path to junit output file",
        type=str, default="./output.xml"
    )
    parser.add_argument(
        "-i", "--include-data", help="Insert data into results.",
        action="store_true"
    )
    parser.add_argument(
        "-u", "--upload", help="Upload data to platform.",
        action="store_true"
    )

    args = parser.parse_args()
    apilisk.printer.verbosity = args.verbose

    include_data=False
    if args.include_data:
        include_data = True


    # Load configuration
    try:
        with open(args.config_file) as cfg_file:
            cfg = json.load(cfg_file)

        client = ApiwatcherClient(cfg)
        project_cfg = client.get_project_config(args.project)

        runner = Runner(project_cfg, args.dataset)
        results = runner.run_project(
            include_data=include_data, debug=True
        )

        if args.junit:
            fmt = JunitFormatter(project_cfg, results)
            fmt.to_file("./output.xml")

        if args.upload:
            client.upload_results(project_cfg, results)

    except IOError as e:
        eprint("Could not open configuration file at {0}: {1}".format(
            args.config_file, e.message
        ))
        parser.print_usage()
        exit(1)
    except ApiliskException as e:
        eprint(e.message)
        exit(1)
