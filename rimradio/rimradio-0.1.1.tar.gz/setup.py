#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='rimradio',
    version='0.1.1',
    description='Simple GTK stream radio player',
    author='Marcin Rim',
    author_email='rimek@poczta.fm',
    url='https://github.com/rimek/radio-gtk',
    packages=find_packages(),
    package_data={
        '': ['*.png', 'README.md'],
    },
    zip_safe=False,
    install_requires=[
        'vext',
        'vext.gi',
        'requests',
    ],
    scripts=['bin/rimradio'],
    test_suite='tests',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
