#!/usr/bin/env python

from distutils.core import setup

# convert readme to thingy
try:
   import pypandoc
   long_description = pypandoc.convert('README.md', 'rst')
except:
   long_description = ''

setup(name='thxgh',
      version='0.2',
      description='CLI for GitHub user contrib graph & statistics.',
      long_description=long_description,
      author='Chris McCormick',
      author_email='chris@mccormick.cx',
      url='http://github.com/chr15m/thxgh',
      packages=['thxgh'],
      package_data = {
          'thxgh' : ['*.hy'],
      },
      #dependency_links=[
      #    'https://github.com/chr15m/...',
      #],
      install_requires=[
          'hy==0.12.0',
          'beautifulsoup4==4.3.2',
      ],
      scripts=['bin/thxgh']
)

