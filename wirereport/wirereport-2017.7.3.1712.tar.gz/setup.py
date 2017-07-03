#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name             = "wirereport",
        version          = "2017.07.03.1712",
        description      = "a small text editor",
        long_description = long_description(),
        url              = "https://github.com/wdbm/report",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "report"
                           ],
        install_requires = [
                           "docopt"
                           ],
        scripts          = [
                           "report.py"
                           ],
        entry_points     = """
                           [console_scripts]
                           report = report:report
                           """
    )

def long_description(
    filename = "README.md"
    ):

    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
