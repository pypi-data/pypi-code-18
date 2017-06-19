import os
from setuptools import setup, find_packages

requires = [
    'lxml',
]

setup(name='kend',
      version='0.7',
      description='kend',
      long_description='Client package for interacting with the Utopia kend server.',
      classifiers=[
        "Programming Language :: Python",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      install_requires=requires,
      tests_require=requires,
      test_suite="kend",
      )

