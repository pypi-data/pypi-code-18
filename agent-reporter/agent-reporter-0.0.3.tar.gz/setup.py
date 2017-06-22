from distutils.core import setup

from setuptools import find_packages

setup(
    name='agent-reporter',
    version='0.0.3',
    description='Agent Reporter',
    packages=find_packages(exclude=['test', 'test.*', 'docs', 'docs*']),
    license='__license__',
    long_description='Agent Reporter',
    install_requires=['libnacl', 'base58', 'requests']
)
