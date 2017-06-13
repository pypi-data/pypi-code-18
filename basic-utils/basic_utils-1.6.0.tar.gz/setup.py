from codecs import open
from itertools import chain
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

test_requirements = [
    'pytest',
    'pytest-cov',
]

dev_requirements = [
    'yapf',
    'flake8',
    'isort',
    'mypy',
    'sphinx',
    'sphinx-autobuild',
    'sphinx_autodoc_typehints',
    'sphinx_rtd_theme',
]

setup(
    name='basic_utils',
    version='1.6.0',
    description='A simple set of Python utils',
    long_description=long_description,
    url='https://github.com/Jackevansevo/basic-utils',
    author='Jack Evans',
    author_email='jack@evans.gb.net',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='utils utilities',
    packages=['basic_utils'],
    setup_requires=['pytest-runner'],
    tests_require=test_requirements,
    extras_require={
        'dev': list(chain(dev_requirements, test_requirements)),
        'test': test_requirements,
    })
