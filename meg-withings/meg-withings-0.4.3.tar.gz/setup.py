#!/usr/bin/env python
import os

from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)


def get_version():
    import subprocess
    version = subprocess.check_output('git describe --always --tags'.split(' '), cwd=ROOT_DIR or None).strip()
    version = version.split('-')
    if len(version) == 1:
        return version[0]
    else:
        return '{0}.dev{1}'.format(*version)


setup(
    name='meg-withings',
    version=get_version(),
    description="Library for the Withings API",
    author='MEG Support Tools',
    author_email='michal@megsupporttools.com',
    url="https://git.megsupporttools.com/misc/python-withings",
    license="MIT License",
    packages=['withings'],
    install_requires=['requests', 'requests-oauth', 'pytz'],
    scripts=['bin/withings'],
    keywords="withings",
    zip_safe=True,
)
