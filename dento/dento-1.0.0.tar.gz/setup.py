from dento import __version__

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

dependencies = ['docopt', 'termcolor']


def publish():
    os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
    publish()
    sys.exit()

setup(
    name='dento',
    version=".".join(str(x) for x in __version__),
    description='dento for stack graphs',
    long_description=open('README.rst').read(),
    url='https://github.com/Denniskamau/stack',
    license="MIT License",
    author='Dennis Kamau',
    author_email='denniskamau3@gmail.com',
    install_requires=dependencies,
    packages=['dento', ],
    entry_points={
        'console_scripts': [
            'dento=dento.main:start'
        ],
    },
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.5',
    ),
)
