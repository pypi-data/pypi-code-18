from setuptools import setup
import os

mypackage_root_dir = os.path.dirname(__file__)
with open(os.path.join(mypackage_root_dir, 'requirements.txt')) as requirements_file:
    requirements = requirements_file.read().splitlines()

with open(os.path.join(mypackage_root_dir, 'frange/VERSION')) as version_file:
    version = version_file.read().strip()


setup(name='frange',
      version=version,
      description='Python package with frange data type for storing large arrays of equally separated data',
      author='Ashley Setter',
      author_email='A.Setter@soton.ac.uk',
      url="https://github.com/AshleySetter/frange",
      download_url="https://github.com/AshleySetter/frange/archive/{}.tar.gz".format(version),
      include_package_data=True,
      packages=['frange',
      ],
      install_requires=requirements,
)
