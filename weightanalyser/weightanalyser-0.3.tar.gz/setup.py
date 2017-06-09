from setuptools import setup, find_packages

setup(name='weightanalyser',
      version='0.3',
      description='Analyse your weight in depth',
      url='https://github.com/finn-christiansen/weightanalyser',
      author='Finn Christiansen',
      author_email='mail@finnchristiansen.com',
      install_requires=['matplotlib', 'scipy', 'PyQt4Enhanced'],
      packages=find_packages(exclude="test"),
      scripts = [
                  'scripts/weightanalyser',
                  'scripts/weightanalyser-gui'
                      ])
