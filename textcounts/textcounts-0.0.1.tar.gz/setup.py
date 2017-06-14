from setuptools import setup

setup(name='textcounts',
      version='0.0.1',
      description='Frequency and proportion counts for series of search strings',
      url='http://github.com/staeiou/textcounts',
      author='Stuart Geiger',
      author_email='stuart@stuartgeiger.com',
      license='MIT',
      packages=['textcounts'],
      install_requires=['pandas'],
      zip_safe=False)
