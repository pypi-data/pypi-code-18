#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()

# doclink = """
# Documentation
# -------------
#
# The full documentation is at http://bupper.rtfd.org."""
# history = open('HISTORY').read().replace('.. :changelog:', '')
doclink = ''
history = ''

setup(
    name='bupper',
    version='0.1.1',
    description='Very simple backup application intended to be run on '
                'cron to allow user-controllable remote backups',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='michaelb',
    author_email='michaelpb@gmail.com',
    url='https://github.com/michaelpb/bupper',
    packages=[
        'bupper',
    ],
    entry_points={
        'console_scripts': ['bupper=bupper.bupper:cli'],
    },
    package_dir={'bupper': 'bupper'},
    install_requires=[],
    license='GPL3',
    keywords='bupper',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        "Environment :: Console",
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
    ],
)
