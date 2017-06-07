#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'certifi==2017.4.17',
    'chardet==3.0.3',
    'idna==2.5',
    'requests==2.17.3',
    'urllib3==1.21.1'
]

test_requirements = [
    'alabaster==0.7.10',
    'argh==0.26.2',
    'Babel==2.4.0',
    'bumpversion==0.5.3',
    'certifi==2017.4.17',
    'cffi==1.10.0',
    'chardet==3.0.3',
    'coverage==4.1',
    'cryptography==1.7',
    'docutils==0.13.1',
    'flake8==2.6.0',
    'idna==2.5',
    'imagesize==0.7.1',
    'Jinja2==2.9.6',
    'MarkupSafe==1.0',
    'mccabe==0.5.3',
    'pathtools==0.1.2',
    'pluggy==0.3.1',
    'py==1.4.34',
    'pyasn1==0.2.3',
    'pycodestyle==2.0.0',
    'pycparser==2.17',
    'pyflakes==1.2.3',
    'Pygments==2.2.0',
    'pytz==2017.2',
    'PyYAML==3.11',
    'requests==2.17.3',
    'six==1.10.0',
    'snowballstemmer==1.2.1',
    'Sphinx==1.4.8',
    'tox==2.3.1',
    'urllib3==1.21.1',
    'virtualenv==15.1.0',
    'watchdog==0.8.3'
]

setup(
    name='qiscus_sdk',
    version='0.1.1',
    description="Python version of Qiscus SDK wrapper",
    long_description=readme + '\n\n' + history,
    author="Muhamad Ishlah",
    author_email='nurul.ishlah@gmail.com',
    url='https://github.com/nurulishlah/qiscus_sdk',
    packages=[
        'qiscus_sdk',
    ],
    package_dir={'qiscus_sdk':
                 'qiscus_sdk'},
    entry_points={
        'console_scripts': [
            'qiscus_sdk=qiscus_sdk.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='qiscus_sdk qiscus sdk',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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
