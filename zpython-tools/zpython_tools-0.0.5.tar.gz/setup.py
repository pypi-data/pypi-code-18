from setuptools import setup
from setuptools import find_packages

from zpython_tools import __version__


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='zpython_tools',
      version=__version__,
      description='kafka tools with python',
      long_description=readme(),
      keywords='kafka tools built against our env.',
      author='Tony Liu',
      packages=find_packages(exclude=["tests", ]),
      install_required=[
          'kazoo.client'
      ],
      scripts=['scripts/broker-meta-management'],
      classifiers=[
          "Development Status :: 4 - Beta",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "Operating System :: POSIX",
          "Operating System :: MacOS :: MacOS X",
      ],
      include_package_date=True,
      zip_safe=False
      )
