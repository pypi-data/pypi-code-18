#!/usr/bin/env python
import subprocess
import platform

from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):

    def run(self):
        print('Platform = %s' % (platform.dist(), ))
        if platform.dist()[0] == 'Ubuntu':
            cmd = 'apt-get -y update && apt-get -y --force-yes install libmysqlclient-dev'
            print('Running command: %s' % (cmd, ))
            output = subprocess.check_output(cmd, shell=True)
            print(output)
        install.run(self)


setup(
    name='mysqlclient-deps',
    version='0.0.1',
    description='',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dataup.io/',
    packages=[],
    cmdclass={
        'install': CustomInstallCommand,
    }
)
