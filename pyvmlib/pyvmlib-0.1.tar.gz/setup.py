"""Setup config for pyvmlib."""

from setuptools import setup

setup(name='pyvmlib',
      version='0.1',
      description='A simple library for controlling VMware vCenter / ESXi servers.',
      url='http://github.com/cambridgeconsultants/pyvmlib',
      author='Cambridge Consultants',
      author_email='jonathan.pallant@cambridgeconsultants.com',
      license='Apache-2.0',
      packages=['pyvmlib'],
      zip_safe=False)
