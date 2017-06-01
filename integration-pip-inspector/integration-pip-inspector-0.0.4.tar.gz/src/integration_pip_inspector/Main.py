
"""
hub_pip
Usage:
  hub_pip create-config [<file_path>]
  hub_pip <project-name> <project-version>
        [
        ((-c | --Config) <hub_config.ini>)
        --OutputDirectory=<build/output/>
        --RequirementsFile=<None>
        --IgnoreFailure=<False>
        ]

Options:
    -h --help                            Show this screen.
    --version                            Show version.

Examples:
  hub-pip -c config.ini --DeployHubBdio=True
Help:
  For help using this tool, please open an issue on the Github_pip repository:
  https://github.com/BlackDuckSoftware/hub-python-plugin
"""

from inspect import getmembers, isclass
import os

from docopt import docopt

from integration_pip_inspector.BlackDuckConfig import BlackDuckConfig
from integration_pip_inspector.BlackDuckCore import BlackDuckCore

from . import __version__ as VERSION


def cli():
    """Main CLI entrypoint."""
    options = docopt(__doc__, version=VERSION)

    if options["<project-name>"]:
        options["--Project-Name"] = options["<project-name>"]

    if options["<project-version>"]:
        options["--Project-Version"] = options["<project-version>"]

    if options["create-config"]:
        if options["<file_path>"]:
            copy_config(path=options["<file_path>"])
        else:
            copy_config()
    else:
        main(options)


def main(options):
    """Build config file from options"""
    config_str = "[Black Duck Config]\n"

    for key, value in options.items():
        if "--" in key and value is not None and value is not "--Config":
            field = key.replace("--", "")
            config_option = field + " = " + str(value) + "\n"
            config_str += config_option

    config = None
    if options["-c"] or options["--Config"]:
        config_file_path = options["<hub_config.ini>"]
        config = BlackDuckConfig.from_file(config_file_path)

    config = BlackDuckConfig.from_string(config_str, black_duck_config=config)

    core = BlackDuckCore(config)
    core.run()


sample_config = """
[Black Duck Config]
OutputDirectory = build/blackduck/
RequirementsFile = None
IgnoreFailure = False

Project-Name = None
Project-Version = None
"""


def copy_config(path=None):
    fullpath = os.path.join(os.getcwd(), "hub_config.ini")
    if path is None:
        path = fullpath
    with open(path, "w+") as file:
        file.write(sample_config)
        print("Created a sample config file @ " + path)
