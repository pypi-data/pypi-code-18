# Copyright (c) 2008-2014 Simplistix Ltd, 2015-2016 Chris Withers
# See license.txt for license details.

import os

from setuptools import setup, find_packages

name = 'testfixtures'
base_dir = os.path.dirname(__file__)

setup(
    name=name,
    version=open(os.path.join(base_dir, name, 'version.txt')).read().strip(),
    author='Chris Withers',
    author_email='chris@simplistix.co.uk',
    license='MIT',
    description=("A collection of helpers and mock objects "
                 "for unit tests and doc tests."),
    long_description=open(os.path.join(base_dir,
                                       'docs',
                                       'description.txt')).read(),
    url='https://github.com/Simplistix/testfixtures',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    extras_require=dict(
        test=['nose', 'nose-fixes', 'nose-cov', 'mock', 'manuel', 'coveralls',
              'zope.component', 'django'],
        build=['sphinx', 'pkginfo', 'setuptools-git', 'wheel', 'twine']
    )
)
