#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Django>=1.8.18',
]

test_requirements = [
    # TODO: put package test requirements here
]

data_files = [
    ('', ['README.rst', 'HISTORY.rst'],),
]

setup(
    name='django-mailformer',
    version='0.0.1',
    description='Django Mailformer',
    long_description=readme + '\n\n' + history,
    author='The Developer Society',
    author_email='studio@dev.ngo',
    url='https://github.com/developersociety/django-mailformer',
    python_requires='>=3.5',
    packages=[
        'mailformer', 'mailformer.management',
        'mailformer.management.commands', 'mailformer.migrations',
        'mailformer.signals', 'mailformer.templatetags',
    ],
    package_dir={
        'mailformer': 'mailformer/',
    },
    include_package_data=True,
    install_requires=requirements,
    license='BSD license',
    zip_safe=False,
    keywords='django glitter',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    data_files=data_files,
)
