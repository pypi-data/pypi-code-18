# from distutils.core import setup
from setuptools import setup

setup(
  name = 'python_jarvis',
  packages = ['python_jarvis'], # this must be the same as the name above
  version = '0.1',
  description = 'Simple helper functions for python projects',
  author = 'Akash Wankhede',
  author_email = 'acwankhede@gmail.com',
  url = 'https://github.com/akash1551/python_jarvis.git', # use the URL to the github repo
  download_url = 'https://github.com/akash1551/python_jarvis/archive/master.zip',
  keywords = ['python helper functions', 'quicktool', 'regular used functions'], # arbitrary keywords
  classifiers = ['Development Status :: 4 - Beta',
                 'Intended Audience :: System Administrators',
                 'Programming Language :: Python :: 2.7']
)
