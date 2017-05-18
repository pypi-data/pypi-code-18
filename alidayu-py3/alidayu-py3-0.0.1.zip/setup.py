import os
import sys
from distutils.core import setup


def read(fname):
    """
    define 'read' func to read long_description from 'README.txt'
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='alidayu-py3',
    version='0.0.1',
    author='songtao',
    author_email='songtao@kicen.com',
    url='https://pypi.python.org/pypi?:action=display&name=alidayu-py3',
    license='MIT',
    description='aldayu api for python3.x',
    long_description=read('README.txt'),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords='alidayu',
    packages=['top']
)

# command: python setup.py register sdist upload
