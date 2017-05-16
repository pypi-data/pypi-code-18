import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='puzcw',
    version='0.0.12',
    author='Brian Wu',
    author_email='brian.george.wu@gmail.com',
    url='https://github.com/bwu/puzcw',
    description='Python API for converting puz files to python objects',
    keywords=['crossword', 'puz'],
    packages=['puzcw'],
    install_requires=['puzpy', 'pillow==3.3.0'],
    include_package_data = True,
    package_data={'static':['*']}
)
