""" Main module """

import argparse
import logging
import os
import re
from os.path import expanduser
import yaml
import argcomplete
from hostname_resolver import HostnameResolver

CONFIG_PATH = expanduser('~/.sytssh.yaml')

def load_yaml(path):
    """Load a yaml as dict"""
    with open(path, 'r') as stream:
        return yaml.safe_load(stream)

def parse_args(doc):
    """ Setup the app arguments """
    parser = argparse.ArgumentParser(prog='sytssh')
    subparsers = parser.add_subparsers(help='Choose the project you want to connect', \
        dest='project')

    for project, attr in doc['hosts'].items():
        parserProject = subparsers.add_parser(project)
        parserProject.add_argument('environment', choices=attr.keys(), \
            help='Choose the environment')
        parserProject.add_argument('-n', help='Which instance of the host', type=int, default=0)

    argcomplete.autocomplete(parser)
    return parser.parse_args()

def connect(doc, args):
    """ Connect to the server via SSH """
    value = doc['hosts'][args.project][args.environment]
    hostnameResolver = HostnameResolver(value)
    hostname = hostnameResolver.get_hostname(args.n)
    port = hostnameResolver.get_port(doc['port'])

    os.system('ssh {username}@{host} -p {port}'.format(host=hostname, \
        username=doc['username'], port=port))

def main():
    try:
        doc = load_yaml(CONFIG_PATH)
        args = parse_args(doc)
        connect(doc, args)
    except FileNotFoundError:
        logging.error("You need to configure %s file", CONFIG_PATH)

if __name__ == '__main__':
    main()
