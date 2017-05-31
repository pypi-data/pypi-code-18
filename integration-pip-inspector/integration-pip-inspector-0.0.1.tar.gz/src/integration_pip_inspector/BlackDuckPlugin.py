
import os

from setuptools import Command

from docopt import docopt
from integration_pip_inspector.BlackDuckConfig import BlackDuckConfig
from integration_pip_inspector.BlackDuckCore import BlackDuckCore
from integration_pip_inspector.Main import main

from . import __version__ as VERSION


class BlackDuckCommand(Command):

    description = "Setuptools hub_pip"

    user_options = [
        ("Config=", "c", "Path to Black Duck Configuration file"),
        ("OutputDirectory=", None, None),
        ("RequirementsFile=", None, None),
        ("IgnoreFailure=", None, None),
        ("CreateFlatDependencyList=", None, None),
        ("CreateTreeDependencyList=", None, None),
        ("Project-Name=", None, None),
        ("Project-Version=", None, None),
    ]

    options = None

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.Config = None
        self.OutputDirectory = None
        self.RequirementsFile = None
        self.IgnoreFailure = None
        self.CreateFlatDependencyList = None
        self.CreateTreeDependencyList = None
        self.Project_Name = None
        self.Project_Version = None

    def finalize_options(self):
        if self.Project_Name is None:
            self.Project_Name = self.distribution.get_name()
        if self.Project_Version is None:
            self.Project_Version = self.distribution.get_version()

        self.options = {
            '-c': self.Config,
            '--Config': self.Config,
            '--OutputDirectory': self.OutputDirectory,
            '--RequirementsFile': self.RequirementsFile,
            '--IgnoreFailure': self.IgnoreFailure,
            '--CreateFlatDependencyList': self.CreateFlatDependencyList,
            '--CreateTreeDependencyList': self.CreateTreeDependencyList,
            '<hub_config.ini>': self.Config,
            '--Project-Name': self.Project_Name,
            '--Project-Version': self.Project_Version,
        }

    def run(self):
        """Run command."""
        main(self.options)


def string_to_boolean(string):
    if string == True:
        return True
    if string == False:
        return False
    if string == 'True' or string == 'true':
        return True
    elif string == 'False' or string == 'true':
        return False
    else:
        raise ValueError
