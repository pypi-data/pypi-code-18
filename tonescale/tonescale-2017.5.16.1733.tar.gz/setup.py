#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name                 = "tonescale",
        version              = "2017.05.16.1733",
        description          = "sound utilities and sounds",
        long_description     = long_description(),
        url                  = "https://github.com/wdbm/tonescale",
        author               = "Will Breaden Madden",
        author_email         = "wbm@protonmail.ch",
        license              = "GPLv3",
        py_modules           = [
                               "tonescale"
                               ],
        install_requires     = [
                               "numpy",
                               "scipy",
                               "shijian"
                               ],
        scripts              = [
                               "sound_search.py"
                               ],
        entry_points         = """
            [console_scripts]
            tonescale = tonescale:tonescale
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
