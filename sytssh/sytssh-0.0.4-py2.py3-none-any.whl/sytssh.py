""" Main module """

import argparse
import logging
import os
import re
from os.path import expanduser
import yaml
import argcomplete

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
        parser_project = subparsers.add_parser(project)
        parser_project.add_argument('environment', choices=attr.keys(), \
            help='Choose the environment')
        parser_project.add_argument('-n', help='Which instance of the host', type=int, default=0)

    argcomplete.autocomplete(parser)
    return parser.parse_args()

def connect(doc, args):
    """ Connect to the server via SSH """
    value = doc['hosts'][args.project][args.environment]
    hostname = get_hostname(value, args.n)
    port = get_port(value, doc['port'])

    os.system('ssh {username}@{host} -p {port}'.format(host=hostname, \
        username=doc['username'], port=port))

def get_port(value, default_port=22):
    return value[value.find(':')+1:] if has_port(value) \
        else default_port

def get_hostname(value, n=0):
    hostname = value if not has_port(value) else value[:value.find(':')]
    return re.sub(r'\{.*\}', '%s' % n, hostname)

def has_port(str):
    return ':' in str

def main():
    try:
        doc = load_yaml(CONFIG_PATH)
        args = parse_args(doc)
        connect(doc, args)
    except FileNotFoundError:
        logging.error("You need to configure %s file", CONFIG_PATH)

if __name__ == '__main__':
    main()
