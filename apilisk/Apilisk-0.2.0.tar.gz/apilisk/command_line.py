#!/usr/bin/env python
import json
import argparse

import apilisk.printer
from apilisk.runner import Runner
from apilisk.exceptions import ApiliskException
from apilisk.printer import eprint, vprint
from apilisk.apiwatcher_client import ApiwatcherClient
from apilisk.junit_formatter import JunitFormatter

def _check_args(args):


    if args.action == "init":
        # Must all be filled
        if (
            args.client_id is None or
            args.agent_id is None or
            args.client_secret is None
        ):
            eprint("Options --client-id, --client-secret and --agent-id must "
                "be set for init action."
            )
            exit(1)

    elif args.action == "run":
        cfg = {}
        if (args.client_id is not None or args.client_secret is not None
        ):
            cfg = _get_config_data(
                args.client_id, args.client_secret, args.agent_id
            )
        else:
            try:
                with open(args.config_file) as cfg_file:
                    cfg = json.load(cfg_file)
            except IOError as e:
                eprint("Could not open configuration file at {0}: {1}".format(
                    args.config_file, e.message
                ))
                exit(1)

        if args.project is None:
            eprint("Project hash (-p) is mandatory for action 'run'")
            exit(1)

        return cfg

    else:
        eprint(
            u"Unknown action {0}, allowed values are run or init".format(
            args.action
        ))
        parser.print_usage()
        exit(1)


def _get_config_data(client_id, client_secret, name):
    return {
        "host": "https://api2.apiwatcher.com",
        "port": 443,
        "client_id": client_id,
        "client_secret": client_secret,
        "agent_id": name
    }

def _create_config_file(data, filename):

    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", default=None,
        help="What to do - init or run."
    )
    parser.add_argument(
        "--client-id", default=None, type=str,
        help="Client id for init"
    )
    parser.add_argument(
        "--client-secret", default=None, type=str,
        help="Client id for init"
    )
    parser.add_argument(
        "--agent-id", default="NOT SET", type=str,
        help="Agent id for init"
    )
    parser.add_argument(
        "-p", "--project", default=None,
        help="Hash of the project."
    )
    parser.add_argument(
        "-d", "--dataset", type=int,
        help="Id of dataset to use. None if no dataset should be used."
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

    cfg = _check_args(args)

    # Switch according to action
    if args.action == "init":
        _create_config_file(
            _get_config_data(
                args.client_id, args.client_secret, args.agent_id
            ),
            args.config_file
        )
    elif args.action == "run":
        try:
            client = ApiwatcherClient(cfg)
            project_cfg = client.get_project_config(args.project)

            runner = Runner(project_cfg, args.dataset)
            results = runner.run_project(
                include_data=args.include_data, debug=True
            )

            if args.junit:
                fmt = JunitFormatter(project_cfg, results)
                fmt.to_file("./output.xml")

            if args.upload:
                client.upload_results(project_cfg, results)

        except ApiliskException as e:
            eprint(e.message)
            exit(1)
