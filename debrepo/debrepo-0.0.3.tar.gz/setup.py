# Copyright (c) 2016 Andrew Hills
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import subprocess
from setuptools.command.test import test as TestCommand
from setuptools import setup, Command

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
LONG_DESCRIPTION = open(readme).read()

VERSION = '0.0.3'


class ReleaseCommand(Command):
    """ Tag and push a new release. """

    user_options = [('sign', 's', 'GPG-sign the Git tag and release files')]

    def initialize_options(self):
        self.sign = False

    def finalize_options(self):
        pass

    def run(self):
        # Create Git tag
        tag_name = 'v%s' % VERSION
        cmd = ['git', 'tag', '-a', tag_name, '-m', 'version %s' % VERSION]
        if self.sign:
            cmd.append('-s')
        print(' '.join(cmd))
        subprocess.check_call(cmd)

        # Push Git tag to origin remote
        cmd = ['git', 'push', 'origin', tag_name]
        print(' '.join(cmd))
        subprocess.check_call(cmd)

        # Push package to pypi
        cmd = ['python', 'setup.py', 'sdist', 'upload']
        if self.sign:
            cmd.append('--sign')
        print(' '.join(cmd))
        subprocess.check_call(cmd)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        ret = pytest.main('debrepo --flake8 ' + self.pytest_args)
        sys.exit(ret)

setup(
        name='debrepo',
        description='Inspect and compare Debian repositories',
        packages=['debrepo'],
        author='Andrew Hills',
        author_email='ahills@redhat.com',
        url='https://pagure.io/debrepo',
        version=VERSION,
        license='GPL',
        zip_safe=False,
        keywords='compose, repodiff',
        long_description=LONG_DESCRIPTION,
        scripts=['bin/debrepodiff'],
        # chardet is actually a dependency of python-debian, but the package is
        # poorly formed. https://bugs.debian.org/858906 is fixed in the
        # upcoming python-debian v0.1.30.
        install_requires=['python-debian', 'chardet'],
        tests_require=['pytest', 'pytest-flake8'],
        cmdclass={'test': PyTest, 'release': ReleaseCommand},
        )
