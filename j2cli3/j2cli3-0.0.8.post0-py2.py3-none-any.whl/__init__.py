#! /usr/bin/env python

""" j2cli3 main file """
from __future__ import unicode_literals
import pkg_resources

__author__ = "Jun Jing Zhang"
__email__ = "zhangjunjing@gmail.com"
__version__ = pkg_resources.get_distribution('j2cli3').version

from j2cli3.cli import main

if __name__ == '__main__':
    main()
