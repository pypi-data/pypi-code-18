from setuptools import setup, find_packages

with open('requirements.txt') as fs:
    REQUIREMENTS = fs.read().strip().split('\n')

with open('VERSION.txt') as fs:
    VERSION = fs.read().strip()

def readme():
    with open('README.rst') as fs:
        return fs.read()

setup(name='hydrobox',
      version=VERSION,
      license='MIT',
      description='Hydrological toolbox build on top of scipy and pandas',
      long_description=readme(),
      author='Mirko Maelicke',
      author_email='mirko.maelicke@kit.edu',
      install_requires=REQUIREMENTS,
      test_suite='nose.collector',
      tests_require=['nose'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False
)