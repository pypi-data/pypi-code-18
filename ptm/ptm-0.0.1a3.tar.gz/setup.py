from setuptools import setup, find_packages
from os.path import join, dirname

from ptm import __version__ as version

setup(
    name='ptm',
    version=version,
    packages=find_packages(),
    author='acrius',
    author_email='acrius@mail.ru',
    url='https://github.com/acrius/path_to_mordor',
    description='',
    license='MIT',
    keywords='',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    package_data={'templates': ['templates/*', ]},
    entry_points={
        'console_scripts': ['galadriel = ptm.adventure_managment:execute_spell']
    },
    include_packages_data=True,
    install_requires=[
        'beautifulsoup4'
    ]
)
