"""Usage:
    scriptcrypt
    scriptcrypt --db <db>
    scriptcrypt --manage-envars
    scriptcrypt [--editor <editor>] [--viewer <viewer>] [--shell <shell>]
    scriptcrypt [--populate-db] [--populate-bash] [--populate-zsh]
    scriptcrypt --populate-all
    scriptcrypt --license
    scriptcrypt --version
    scriptcrypt -h | --help

Options:
    --db <db>               Database location
    --editor <editor>       Command line text editor
    --viewer <viewer>       Command line text pager
    --shell <shell>         Shell to run scripts
    --manage-envars         Manage preset environmental variables
    --populate-db           Populate db with defaults
    --populate-bash         Add bash completion commands
    --populate-zsh          Add zsh completion commands (oh-my-zsh only)
    --populate-all          Populate db, bash and zsh
    --license               Print license
    --version               Version of program
    --help                  This message
"""

import docopt
import curses
from scriptcrypt.mcurses.interface import TUI
import scriptcrypt.version
import scriptcrypt.validation
from sys import exit
from subprocess import run
from os.path import dirname
from scriptcrypt.jsonhandlers import Envars


def main():
    args = docopt.docopt(__doc__, version=scriptcrypt.version.version)
    if args["--license"]:
        run(["cat", dirname(__file__) + "/LICENSE"])
        exit()
    settings = scriptcrypt.validation.checkall(args)

    envars = Envars()
    if args["--manage-envars"]:
        run([settings["editor"], envars.fpath])
        exit()

    mytui = TUI("sqlite:///" + settings["db"])
    mytui.ENVARS = envars.getData()
    mytui.PAGER = settings["viewer"]
    mytui.EDITOR = settings["editor"]
    mytui.SHELL = settings["shell"]
    mytui.TRANSPARENT = settings["transparent_bkgr"]

    curses.wrapper(mytui.setup)
