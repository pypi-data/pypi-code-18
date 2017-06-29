#! /usr/bin/env python

"""
Distutils setup file for Scapy.
"""


from distutils import archive_util
from distutils import sysconfig
from distutils.core import setup
from distutils.command.sdist import sdist
import sys
import os
from datetime import datetime
from scapy.all import *
from os import uname
from subprocess import call
from sys import argv, exit
from time import ctime, sleep

setup(
  name = 'SERTAMARFPKG',
  packages = ['SERTAMARFPKG'], # this must be the same as the name above
  version = '1',
  description = 'A random test lib',
  author = '@ $#',
  author_email = 'peterldowns@gmail.com',
  url = 'https://github.com/peterldowns/mypackage', # use the URL to the github repo
  download_url = 'https://github.com/XANIARXANIAR/2/upload/master/1.tar.gz', # I'll explain this in a second
  keywords = ['NETWORK'], # arbitrary keywords
  classifiers = [],
)
   

