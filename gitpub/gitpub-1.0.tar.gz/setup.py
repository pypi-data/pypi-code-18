"""
Python package setup file.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='gitpub',
    version='1.0',
    description="a module to interact with Github's API",
    long_description=long_description,
    url='https://github.com/demfier/gitpub',

    author='Gaurav Sahu',
    author_email='sahu.gaurav719@googlemail.com',
    license='MIT',

    classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    ],

    keywords='github api development interact',

    packages=find_packages(),
    install_requires=['peppercorn'],

    entry_points={
        'console_scripts': [
            'sample=samples.most_popular_repo:sample'
        ]
    }
)
