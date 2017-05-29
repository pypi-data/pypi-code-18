import os
import sys

from setuptools import setup, find_packages, Command

setup(
    name='shabby',
    version='0.0.0',
    url='https://github.com/chriscz/shabby',
    description='Useful programming snippets',

    author='Chris Coetzee',
    author_email='chriscz93@gmail.com',

    # XXX we will need to evaluate this later on
    license='Mozilla Public License 2.0 (MPL 2.0)',

    install_requires=[],
    #packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
