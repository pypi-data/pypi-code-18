#!/usr/bin/env python
# vi: et sw=2 fileencoding=utf-8
#============================================================================
# pitargparse
# Copyright (c) 2017 Pispalan Insinööritoimisto Oy (http://www.pispalanit.fi)
#
# Redistributions of files shall retain the above copyright notice.
#
# @created     26.05.2017
# @author      Harry Karvonen <harry.karvonen@pispalanit.fi>
# @copyright   Copyright (c) Pispalan Insinööritoimisto Oy
# @license     MIT Licence
#============================================================================

from setuptools import setup, find_packages

setup(name='pitargparse',
    version='0.1.2',
    description='extensions for python argparse',
    url='https://git.pispalanit.fi/pit/pitargparse',
    author='Harry Karvonen',
    author_email='harry.karvonen@pispalanit.fi',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

         'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
zip_safe=False)

