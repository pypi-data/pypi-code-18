#!/usr/bin/env python
import os
import subprocess
import platform

from setuptools import setup, find_packages
from setuptools.command.install import install


def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


class CustomInstallCommand(install):

    def run(self):
        if platform.dist()[0] == 'Ubuntu':
            cmd = 'apt-get -y update && apt-get -y --force-yes install libmysqlclient-dev'
            print('Running command: %s' % (cmd, ))
            output = subprocess.check_output(cmd, shell=True)
            print(output)
        install.run(self)


setup(
    name='dojo-mysql',
    version='0.0.12',
    description='Dojo source and sink adapters for MySQL connections.',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=find_packages(),
    install_requires=[
      'dojo',
      'mysqlclient'
    ]
)
