from setuptools import setup

setup(name='liquidcounter',
      version='1.0',
      description='Counter of votes for liquid democracy',
      url='http://github.com/daviortega/liquidcounter',
      author='Davi Ortega',
      author_email='davi.ortega@gmail.com',
      license='CC0',
      packages=['liquidcounter'],
      zip_safe=False,
      tests_require=['pytest'])
