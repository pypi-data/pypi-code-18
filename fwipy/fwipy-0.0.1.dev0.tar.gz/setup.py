# -*- coding: utf-8 -*-

import os

from codecs import open
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

packages = ['fwipy']

requires = ['requests']

classifiers = ('Intended Audience :: Developers',
               'Natural Language :: English',
               'License :: OSI Approved :: Apache Software License',
               'Development Status :: 1 - Planning',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2.6',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 3.3',
               'Programming Language :: Python :: 3.4',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               'Programming Language :: Python :: Implementation :: CPython')

about = {}
with open(os.path.join(here, 'fwipy', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(name=about['__title__'],
      version=about['__version__'],
      description=about['__description__'],
      long_description=readme,
      url=about['__url__'],
      download_url=about['__download_url__'],
      author=about['__author__'],
      author_email=about['__author_email__'],
      license=about['__license__'],
      packages=packages,
      install_requires=requires,
      classifiers=classifiers,
      zip_safe=False)