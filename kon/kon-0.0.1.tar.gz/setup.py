#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages
import os
import os.path as op

HERE = op.abspath(op.dirname(__file__))

setup(name='kon',
      version=open(op.join(HERE, 'VERSION')).read(),
      author='Wampeter Foma',
      author_email='foma@wampeter.org',
      url='https://bitbucket.org/wampeter/kon',
      license='GNU GPL v3',
      description='A configuration file(s) management library',
      long_description=open(op.join(HERE, 'README.rst')).read(),
      zip_safe=False,
      py_modules=['kon'],
      platforms='any',
      install_requires=[],
      extras_require={
        'tests': [
            'nose',
            'mock',
            'coverage',
            'tox'
        ],
        'dev': [
            'flake8',
            'pylint'
        ]
      },
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ]
)
