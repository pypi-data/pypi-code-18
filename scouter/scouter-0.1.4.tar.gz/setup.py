#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Scouter Data
  Created: 2017/5/24
"""

from codecs import open as copen
from setuptools import setup, find_packages

packages = find_packages()

requires = []

version = '0.1.4'

#
# LOAD README.md
#
try:
    readme = None
    with copen('README.md',  encoding='utf-8') as f:
        readme = f.read()

except:
    readme = 'scouter is a tiny data struct, if add or change, ' + \
        'the callback will be called!'

setup(
    name='scouter',
    version=version,
    description='Watching Data with Callback!',
    long_description=readme,
    author='v1ll4n',
    author_email='v1ll4n@villanch.top',
    url='https://github.com/VillanCh/scouter',
    packages=packages,
    package_data={"":['README.md',]},
    package_dir={'scouter':'scouter'},
    include_package_data=True,
    install_requires=requires,
    license='BSD 2-Clause License',
    zip_safe=False,
)
