###############################################################################
#
# Copyright 2014 by Shoobx, Inc.
#
###############################################################################
import os
from setuptools import setup, find_packages


def read_file(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="shoobx.flowview",
    version='1.0.0',
    author="Shoobx, Inc.",
    author_email="dev@shoobx.com",
    description="XPDL Viewer and Browser",
    long_description=
    read_file('README.rst') +
    '\n\n' +
    read_file('CHANGES.rst'),
    keywords="xpdl process workflow",
    license='Proprietary',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['shoobx'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=['coverage', 'mock'],),
    install_requires=[
        'setuptools',
        'lxml'
    ],
    entry_points={
        'console_scripts': [
            'flowview = shoobx.flowview.cli:main',
        ],
    }
)
