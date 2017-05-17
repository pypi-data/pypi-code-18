#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='sample_qrzt6y2s',
    version='0.1.0',
    description="sample_qrzt6y2s_short_description",
    long_description=readme + '\n\n' + history,
    author="qrZt6y2S",
    author_email='qrZt6y2S@inbox.lv',
    url='https://github.com/qrZt6y2S/sample_qrzt6y2s',
    packages=[
        'sample_qrzt6y2s',
    ],
    package_dir={'sample_qrzt6y2s':
                 'sample_qrzt6y2s'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='sample_qrzt6y2s',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
