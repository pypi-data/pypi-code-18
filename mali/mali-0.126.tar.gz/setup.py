# coding=utf-8
import os
from setuptools import setup, find_packages

build = os.environ['PIP_BUILD']
keywords = os.environ['PIP_KEYWORDS']


version = '0.{}'.format(build)

with open('requirements.txt') as f:
    install_requires = f.readlines()

setup(
    name='mali',
    version=version,
    py_modules=['mali'],
    packages=find_packages(),
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        mali=mali:cli
    ''',
)
