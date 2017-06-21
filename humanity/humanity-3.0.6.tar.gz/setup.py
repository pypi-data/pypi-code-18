from setuptools import setup, find_packages
from distutils.core import setup
from os.path import join, dirname
import humanity


setup(
    name = 'humanity',
    version = humanity.__version__,
    description='Module for newbies, changes start index from 0 to 1',
    
	author='vlad1777d',
	author_email='naumovvladislav@mail.ru',
	url='https://github.com/vlad1777d/humanity',
    
    long_description = open ('README.md').read(),
    
    test_suite = 'unittest_humanity',
    
    packages=['humanity'],  # packages = find_packages()
)

