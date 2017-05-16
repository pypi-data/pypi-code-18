##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.app.tree package

"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

setup(name='zope.app.tree',
      version='4.0.0',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='Static Tree Implementation',
      long_description=(
          read('README.rst')
          + '\n\n' +
          read('src', 'zope', 'app', 'tree', 'README.rst')
          + '\n\n' +
          read('CHANGES.rst')
      ),
      keywords="zope3 tree static zpt",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'
      ],
      url='http://github.com/zopefoundation/zope.app.tree',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope', 'zope.app'],
      extras_require={
          'test': [
              'zope.app.rotterdam',
              'zope.browserpage',
              'zope.browserresource',
              'zope.configuration',
              'zope.security',
              'zope.testing',
              'zope.testrunner',
          ],
          'skin': [
              'zope.app.rotterdam',
          ]
      },
      install_requires=[
          'setuptools',
          'zope.container',
          'zope.component',
          'zope.interface',
          'zope.location',
          'zope.publisher',
          'zope.schema',
          'zope.security',
          'zope.traversing',
      ],
      include_package_data=True,
      zip_safe=False,
)
