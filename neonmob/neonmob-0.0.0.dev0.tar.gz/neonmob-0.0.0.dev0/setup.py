from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='neonmob',
        version='0.0.0.dev',
        description='An API client library for NeonMob.com',
        long_description=long_description,
        url='https://github.com/sgerrand/neonmob.py',
        author='Sasha Gerrand',
        author_email='pypi-neonmob@sgerrand.com',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Testing',
            'Topic :: Utilities',
        ],
        keywords='neonmob http api httpclients web',
        packages=find_packages(exclude=['contrib', 'docs', 'tests']),
        install_requires=[],
        extras_require={
            'dev': ['check-manifest'],
            'test': ['coverage'],
        },
)
