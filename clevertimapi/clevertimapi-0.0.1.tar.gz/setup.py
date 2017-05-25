import os
from setuptools import setup, find_packages
import sys

current_dir = os.path.abspath(os.path.dirname(__name__))
with open(os.path.join(current_dir, 'README.md'), 'r') as f:
    long_description = f.read()

requires_list = ['requests']

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
    requires_list.append('unittest2')
else:
    import unittest


def unittest_discover_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(
    name='clevertimapi',
    version='0.0.1',
    description='Clevertim CRM Python API',
    long_description=long_description,
    url='https://github.com/ciprianmiclaus/clevertim-api-py',
    author='Ciprian Miclaus',
    author_email='ciprianm@gmail.com',
    license='BSD3',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Libraries',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='Clevertim CRM contact management API development',

    packages=find_packages(),
    install_requires=requires_list,

    test_suite='setup.unittest_discover_test_suite',

)
