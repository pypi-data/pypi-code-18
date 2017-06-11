#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import vcversioner

# with open('requirements.txt', 'r') as f:
#     # Filter comments
#     lines = (x.strip() for x in f.readlines() if x.strip()[0] != '#')
#     # Filter non -i/-r lines
#     install_requires = [x for x in lines if x[0] != '-']

# with open('test-requirements.txt', 'r') as f:
#     # Filter comments
#     lines = (x.strip() for x in f.readlines() if x.strip()[0] != '#')
#     # Filter non -i/-r lines
#     test_requires = [x for x in lines if x[0] != '-']

install_requires = [
    'pip>=8.0',
    'wheel',
    'setuptools',
    'vcversioner',
    'arghandler',
]


setup(name='silktool',
      description='Tooler app to create layout for other tools',
      long_description='''
Tooler app to create layout for other tools
''',
      keywords='',
      author='Binay Kumar Ray',
      author_email='binayray2009@gmail.com',
      license='',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: Other/Proprietary License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.7',
          'Operating System :: OS Independent',
      ],
      packages=find_packages(exclude=("test",)),
      include_package_data=True,
      install_requires=install_requires,
      # setup_requires=['tcversioner'],
      # tcversioner={
      #     'version_module_paths': ['silktool/_version.py'],
      #     'use_dev_not_post': True,
      # },
      version=vcversioner.find_version().version,
      test_suite='nose.collector',
      extras_require={
          'tests': install_requires,
      },
      entry_points={
          'console_scripts': [
              'silktool=silktool.main:main',
          ],
      },)
