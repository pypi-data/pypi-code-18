import os

from setuptools import setup, find_packages

PACKAGE_NAME = "pytoolbelt"
PACKAGE_VERSION = "0.1"

here = os.path.abspath(os.path.dirname(__file__))
# README = open(os.path.join(here, 'README.txt')).read()
# CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    ]

setup(name='pytoolbelt',
      version='0.1.1',
      description='Python library for some commonly usefull tools',
      long_description='Python library for some commonly usefull tools',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pylons",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          ],
      author='',
      author_email='',
      url='',
      keywords='web,tools',
      package_dir={'': 'src'},
      packages=find_packages("src"),
      include_package_data=True,
      zip_safe=False,
      #      test_suite='jhi_tools2',
      install_requires=requires,
      #      entry_points = """\
      #      [paste.app_factory]
      #      main = sportpartner24:main
      #      """,
      namespace_packages=['pytoolbelt'],
      )
