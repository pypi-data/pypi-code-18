#!/usr/bin/env python

import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('pythonwhat_ext.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
	name = 'pythonwhat-ext',
	version = version,
        py_modules= ['pythonwhat_ext'],
        install_requires = ['pythonwhat>=2.7'],
        description = 'pythonwhat extensions - high level SCTs',
        author = 'Michael Chow',
        author_email = 'michael@datacamp.com',
        url = 'https://github.com/datacamp/pythonwhat-ext')
