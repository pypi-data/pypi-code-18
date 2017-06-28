"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
import sys
import os
from datetime import datetime
from scapy.all import *
from os import uname
from subprocess import call
from sys import argv, exit
from time import ctime, sleep
from codecs import open
from os import path
from distutils.core import setup
setup(
  name = 'sarltdtgore',
  packages = ['sarltdtgore'], # this must be the same as the name above
  version = '0.1',
  description = 'A random test lib',
  author = 'Peter Downs',
  author_email = 'peterldowns@gmail.com',
  url = 'https://github.com/radolfterminator/', # use the URL to the github repo
  download_url = 'https://github.com/radolfterminator/ae/blob/master/1.tar.gz', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)

