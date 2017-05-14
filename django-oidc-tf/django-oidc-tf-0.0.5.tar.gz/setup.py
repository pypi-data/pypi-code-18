#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import djangooidc

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = djangooidc.__version__

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-oidc-tf',
    version=version,
    description="""A Django OpenID Connect (OIDC) authentication backend""",
    long_description=readme + '\n\n' + history,
    author='Thomas Frössman',
    author_email='thomasf@jossystem.se',
    url='https://github.com/thomasf/django-oidc',
    packages=[
        'djangooidc',
    ],
    include_package_data=True,
    install_requires=[
        'django>=1.10',
        'oic>=0.10.0',
    ],
    license="Apache Software License",
    zip_safe=False,
    keywords='repo_name',
    classifiers=[
        'Environment :: Web Environment',
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
)
