import os
import pip
from setuptools import setup

# Parse the requirements files with pip to generate the install_requires and
# tests_require lists dynamically.
session = pip.download.PipSession()
curpath = os.path.dirname(os.path.abspath(__file__))
install_requires = pip.req.parse_requirements(
    os.path.join(curpath, 'requirements.txt'),
    session=session
)
test_requires = pip.req.parse_requirements(
    os.path.join(curpath, 'test_requirements.txt'),
    session=session
)

setup(
    name='pgdeploy',
    version='0.0.1',
    packages=['pgdeploy'],
    install_requires=[str(item.req) for item in install_requires],
    tests_require=[str(item.req) for item in test_requires],
    description='Simple Postgres schema management tool',
    maintainer='Ross Schlaikjer',
    maintainer_email='developers@schlaikjer.com',
)
