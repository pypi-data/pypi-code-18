from distutils.core import setup

from setuptools import find_packages

setup(
    name='agent-reporting',
    version='0.0.1',
    description='Agent Reporting',
    packages=find_packages(exclude=['test', 'test.*', 'docs', 'docs*']),
    license='__license__',
    long_description='Agent Reporting',
    install_requires=['libnacl', 'base58', 'requests']
)
