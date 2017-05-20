#!/usr/bin/env python
from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as textfile:
    readme = textfile.read()


setup(
    name='resyndicator',
    version='0.5.2',
    author='Denis Drescher',
    author_email='denis.drescher+resyndicator@claviger.net',
    url='https://bitbucket.org/Telofy/resyndicator',
    description='Aggregates data from many sources into merged and filtered Atom feeds.',
    long_description=readme,
    license='Apache 2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'utilofies',
        'birdy',
        'requests',
        'python-dateutil',
        'feedparser',
        'SQLAlchemy',
        'awesome-slugify',
        'beautifulsoup4',
        'psycopg2',
        'readability-lxml',
        'xmltodict',
        'cached-property',
    ],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'resyndicator = resyndicator.console:run'
        ]
    }
)
