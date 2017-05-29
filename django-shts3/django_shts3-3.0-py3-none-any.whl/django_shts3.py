#!/usr/bin/env python3

import os
import sys
from subprocess import call
from os.path import expanduser

ALIASES = {
    # Django
    'c'  : 'collectstatic',
    'r'  : 'runserver',
    'sp' : 'startproject',
    'sa' : 'startapp',
    't'  : 'test',

    # Shell
    's'  : 'shell',
    'sh' : 'shell',

    # Auth
    'csu': 'createsuperuser',
    'cpw': 'changepassword',

    # Migrations
    'm'  : 'migrate',
    'mg' : 'migrate',
    'mkm': 'makemigrations'
}

class ParseException(Exception):
    pass


def run(command=None, *arguments):
    """
    Run the given command.

    Loads extra commands from file.

    Parameters:
    :param command: A string describing a command.
    :param arguments: A list of strings describing arguments to the command.
    """

    if command is None:
        sys.exit('django-shts3: No argument was supplied, please specify one.')

    script_path = os.getcwd()
    while not os.path.exists(os.path.join(script_path, 'manage.py')):
        base_dir = os.path.dirname(script_path)
        if base_dir != script_path:
            script_path = base_dir
        else:
            sys.exit('django-shts3: No \'manage.py\' script found in this directory or its parents.')
    try:
      config_file_path = os.path.join(expanduser("~"), ".django_shts3")
      with open(config_file_path, "r") as conifg_file:
        for x in conifg_file:
          parsed = x.split(" @@@ ")
          if not len(parsed) == 2:
            raise ParseException("Can't parse config file .django_shts3 (in your home dir)")
          alias = parsed[0]
          command = parsed[1]
          ALIASES[alias] = command
    except ParseException as e:
      print(e)
      exit(1)
    except Exception:
      pass

    if command in ALIASES:
        command = ALIASES[command]

    return call('%(python)s %(script_path)s %(command)s %(arguments)s' % {
        'python': sys.executable,
        'script_path': os.path.join(script_path, 'manage.py'),
        'command': command or '',
        'arguments': ' '.join(arguments)
    }, shell=True)


def main():
    """Entry-point function."""
    sys.exit(run(*sys.argv[1:]))

if __name__ == '__main__':
    main()
