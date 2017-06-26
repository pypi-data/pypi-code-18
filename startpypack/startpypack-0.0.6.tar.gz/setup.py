from setuptools import setup

setup(name='startpypack',
      version='0.0.6',
      description='Initialize a new python package with python',
      url='https://bitbucket.org/nrw16/startpypack',
      author='Nick Wheeler',
      author_email='nrw16@case.edu',
      license='GPL3',
      packages=['startpypack'],
      package_dir={'startpypack': './startpypack'},
      package_data={'startpypack': ['files/data/*','files/docs/*','README.rst']},
      install_requires=['markdown'],
      include_package_data=True,
      zip_safe=False)
