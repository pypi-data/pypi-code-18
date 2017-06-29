
import sys
import os
import os.path as p
from termcolor import colored as col
from termcolor import cprint


_help_ = {
    "magic [stops | -s] [src] [dest]": "Formats stop data. Writes to dest/stops/.",
    "magic [trips | -t] [src] [dest]": "Checks and formats trip data. Writes to dest/trips/.",
    "magic trips [-h | --help]": "Open this help dialogue."
}


class Logger:
    @staticmethod
    def std(info: (int, str)):
        """
        Prints a message to standard output.
        :param info: tuple containing status code and message.
        """
        code = info[0]
        message = info[1]

        if code == 0:
            sys.stdout.write(message + "\n")
        elif code == 1:
            sys.stdout.write(col(message, "yellow") + "\n")
        else:
            sys.stderr.write(col(message + " Aborting.", "red") + "\n")
            sys.exit(1)

    @staticmethod
    def replace(message=None, stop=False):
        if message and not stop:
            sys.stdout.write(message + "\r")
        elif not message and stop:
            sys.stdout.write("\n")


def clean(directory: str):
    """
    Cleans the destination directory before writing.
    :return: tuple containing status code and log message.
    """

    # return without error
    cleaned = (0, "Cleaning {0}.".format(directory))

    try:
        for part in os.listdir(directory):
            os.remove(p.join(directory, part))
    except OSError or FileNotFoundError:
        cleaned = (2, "Couldn't clean {0}.".format(directory))

    Logger.std(cleaned)
    return


def args(arglist: list, defaults: list=[]):
    """
    If no source or destination directories are specified, take the
    current working directory and pick out /stoptimes/ and /merged/.
    Otherwise, use the specified source and destinations.

    :param arglist: list of system arguments.
    :param defaults: list of default source and destination paths.
    """
    cur = os.getcwd()

    if len(arglist) == 2:
        Logger.std((1, "No source or destination paths specified - using current working directory."))
        return [cur + defaults[0], cur + defaults[1]]
    elif len(arglist) == 1 or arglist[1] == "-h" or arglist[1] == "--help":
        cprint("bongo-magic 0.0.6", attrs=["bold", "underline"])
        for cmd in _help_:
            print(cmd + " -> " + _help_[cmd])

        print()
    else:
        return arglist[1:]
