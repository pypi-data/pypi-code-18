import os
import sys

from setuptools import setup

# get version
sys.path.append(os.path.join(os.path.dirname(__file__), 'boned_html'))
from version import __version__ as release_version  # flake8: noqa
sys.path.pop()

# see also setup.cfg
setup(version=release_version,
      packages=["boned_html"],
      install_requires =["lxml"],
      extras_require={
        "test": ["nose>=1.3.7", "coverage>=4.0.3"],
        "quality": ["flake8>=2.5.4"]})
