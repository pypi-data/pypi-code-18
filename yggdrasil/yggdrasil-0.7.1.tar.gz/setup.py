#!/usr/bin/env python

from setuptools import setup
import unittest

def unit_tests():
    loader = unittest.TestLoader()
    test_suite = loader.discover('test', pattern='test_*.py')
    return test_suite

setup(
    name = 'yggdrasil'
    ,version = '0.7.1'
    ,author = 'frank2'
    ,author_email = 'frank2@dc949.org'
    ,description = 'A tree library. Contains implementations for binary trees and AVL trees.'
    ,license = 'GPLv3'
    ,keywords = 'trees binary_trees'
    ,url = 'https://github.com/frank2/yggdrasil'
    ,package_dir = {'yggdrasil': 'lib'}
    ,packages = ['yggdrasil']
    ,test_suite = 'setup.unit_tests'
    ,long_description = '''Yggdrasil is a flexible tree library that allows you to define your very own trees from the ground up.'''
    ,classifiers = [
        'Development Status :: 4 - Beta'
        ,'Topic :: Software Development :: Libraries'
        ,'License :: OSI Approved :: GNU General Public License v3 (GPLv3)']
)
