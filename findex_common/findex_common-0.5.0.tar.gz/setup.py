from setuptools import setup

setup(name='findex_common',
      version='0.5.0',
      description='This package contains modules used by different Findex projects.',
      url='http://github.com/skftn/findex-gui',
      author='Sander Ferdinand',
      author_email='sanderf@cedsys.nl',
      license='MIT',
      packages=['findex_common'],
      install_requires=['appdirs'],
      zip_safe=False)
