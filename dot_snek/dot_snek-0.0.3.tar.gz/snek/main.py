from os import chdir
from os.path import expanduser
from pathlib import Path
from sys import argv

from snek.core import link_all, shell_command
from snek.update import update


def main():
    if len(argv) < 2:
        return
    chdir(list(shell_command('echo $PWD', False))[0].strip('\n'))
    if argv[1].lower() == 'update':
        update()
    elif argv[1] == 'link':
        environments = argv[2:]
        for e in environments:
            link_all(Path(f'./{e}').resolve(), Path(expanduser('~')))
