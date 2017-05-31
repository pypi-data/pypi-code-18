# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools.command.test import test as test_command
from sped_common import __version__


class PyTest(test_command):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        test_command.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # doctest
        import sys
        import pytest

        errno = pytest.main(self.pytest_args)

        sys.exit(errno)


setup(
    name='sped-common',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    package_data={
    },
    version=__version__,
    description='Biblioteca de componentes comuns do SPED.',
    long_description='Biblioteca de componentes comuns do SPED.',
    author='Sergio Garcia',
    author_email='sergio@ginx.com.br',
    url='https://github.com/sped-br/python-sped-common',
    download_url='https://github.com/sped-br/python-sped-common/releases',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='sped fiscal contábil contabilidade receita federal',
    install_requires=[''],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
