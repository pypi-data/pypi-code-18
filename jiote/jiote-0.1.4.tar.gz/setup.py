import os
import sys

import jiote

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
    pass

packages = [
    'jiote',
    'jiote.models'
]

requires = []
setup(
    name='jiote',
    version=jiote.__version__,
    description='IOT abstraction',
    long_description=open('README.txt').read(),
    author='Gamaliel Espinoza Macedo',
    author_email='gamaliel.espinoza@gmail.com',
    url='https://github.com/gamikun/jiote',
    packages=packages,
    package_dir={'jiote': 'jiote'},
    install_requires=requires,
    include_package_data=True,
    package_data={},
    ext_modules=[],
    zip_safe=False,
    #classifiers=(
    #    'Development Status :: 5 - Production/Stable',
    #    'Programming Language :: Python :: 2.7',
    #),
)