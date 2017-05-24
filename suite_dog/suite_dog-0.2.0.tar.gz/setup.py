#!/usr/bin/env python

import os
import sys
import unittest
from os import path as p
from setuptools import Command
from distutils.core import setup
from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt', session='hack')

requirements = [str(ir.req) for ir in install_reqs]


def get_files(root):
    for dirname, dirnames, filenames in os.walk(root):
        for filename in filenames:
            yield os.path.join(dirname, filename)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def parse_requirements(filename, parent=None):
    parent = (parent or __file__)
    filepath = p.join(p.dirname(parent), filename)
    content = read(filename, parent)

    for line_number, line in enumerate(content.splitlines(), 1):
        candidate = line.strip()

        if candidate.startswith('-r'):
            for item in parse_requirements(candidate[2:].strip(), filepath):
                yield item
        else:
            yield candidate


class DatadogTest(Command):
    """
    Run the tests for datadog
    """
    description = "Run tests for datadog"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(self.distribution.tests_require)

        from tests import suite
        test_result = unittest.TextTestRunner(verbosity=2).run(suite())

        if test_result.wasSuccessful():
            sys.exit(0)
        sys.exit(-1)


setup(
    name='suite_dog',
    packages=[
        'suitedog',
        'suitedog.metrics',
    ],
    package_dir={
        'suitedog': 'suitedog',
        'suitedog.metrics': 'suitedog/metrics',
    },
    version='0.2.0',
    url='https://github.com/suitepad-gmbh/datadog',
    author='Rajat Gupta',
    author_email='rajat.gupta@suitepad.de',
    description='Datadog metrices',
    long_description=open('README.md').read(),
    platform='any',
    zip_safe=False,
    classifiers=[
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Office/Business',
    ],
    test_suite='tests.suite',
    tests_require=[
        'flake8',
        'check-manifest',
        'coverage',
    ],
    install_requires=requirements,
    cmdclass={
        'test': DatadogTest,
    },
)
