from setuptools import setup

setup(name='pycbc-azure-binary-lal',
      version='0.0.6',
      description='some shared object files from lalsuite, no gaurantees',
      author='Alex Nitz',
      author_email='alex.nitz@aei.mpg.de',
      install_requires=['pycbc', 'numpy==1.13.0'],
      package_data={'blal': ['*.so*']},
      packages=['lal', 'lalsimulation', 'lalframe', 'blal'],
     )
