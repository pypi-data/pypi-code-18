
import os

from setuptools import setup

os.environ['TRAVIS_CI'] = 'True'

try:
    from setuptools import setup

    setup_kwargs = {'entry_points': {'console_scripts': ['landsat=cloudsat.cloudsat:__main__']}}
except ImportError:
    from distutils.core import setup

    setup_kwargs = {'scripts': ['bin/cloudsat']}

tag = '0.0.1'

setup(name='CloudCRMSat',
      version=tag,
      description='Plugin Modificado para permitir download direto da Scena',
      setup_requires=['nose>=1.0'],
      py_modules=['cloudsat'],
      keywords='landsat download',
      author='Gustavo Junior',
      author_email='gustavorgjunior@gmail.com',
      platforms='Posix; MacOS X; Windows',
      packages=['cloudsat'],
      download_url='https://github.com/{}/{}/archive/{}.tar.gz'.format('brackbk', 'CloudCRMSat', tag),
      url='https://github.com/dgketchum',
      install_requires=['lxml==3.7.3', 'numpy==1.12.1', 'pandas==0.19.2',
                                                             'python-dateutil==2.6.0', 'pytz==2017.2',
                                                             'requests==2.13.0', 'six==1.10.0'],
      **setup_kwargs)

# ============= EOF ==============================================================
