import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()

setup(
    name='pykemon2.0',
    version='1.0.0',
    description='A Python wrapper for PokeAPI',
    long_description=readme,
    author='JustMaffie',
    author_email='jorivanee@hotmail.com',
    url='https://github.com/justmaffie/pykemon2.0',
    packages=[
        'pykemon2.0',
    ],
    package_dir={'pykemon2.0': 'pykemon2.0'},
    include_package_data=True,
    install_requires=[
        'requests==2.10.0', 'simplejson==3.3.1', 'beckett==0.4.0'
    ],
    license="BSD",
    zip_safe=False,
    keywords='pykemon',
    test_suite='tests',
)