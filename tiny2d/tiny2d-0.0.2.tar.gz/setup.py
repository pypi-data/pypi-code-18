import codecs
import os
import re

from setuptools import setup


# read version in __init__.py
# code adapted from: https://github.com/pypa/pip/blob/1.5.6/setup.py#L33
here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")


setup(name='tiny2d',
      version=find_version("tiny2d/__init__.py"),
      description='A python library for basic 2-D geometry.',
      url='https://github.com/ngroup/tiny2d',
      author='Chun Nien',
      author_email='contact@chunnien.com',
      license='MIT',
      packages=['tiny2d'],
      zip_safe=False)
