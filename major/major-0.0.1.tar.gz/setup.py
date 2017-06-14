#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

test_requirements = []

setup(
    author='Stefan Fischer',
    author_email='sfischer13@ymail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
    ],
    description='Python implementation of the major system.',
    include_package_data=True,
    install_requires=requirements,
    keywords='major sytem phonetic mnemonic number',
    license='MIT',
    long_description=readme + '\n\n' + history,
    name='major',
    package_dir={'major': 'major'},
    packages=['major'],
    python_requires='>=3.3',
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sfischer13/python-major',
    version='0.0.1',
    zip_safe=False)
