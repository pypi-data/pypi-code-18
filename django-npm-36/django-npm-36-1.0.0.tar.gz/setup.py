from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from os import path

here = path.abspath(path.dirname(__file__))

try:
    from collections import OrderedDict
    requirements = []
except ImportError:
    requirements = ['ordereddict']

setup(
    name='django-npm-36',
    version='1.0.0',
    description='A temp compat. version of django-npm',
    url='https://github.com/pattyjogal/django-npm',
    author='Patrick Gallagher',
    author_email='patrickj@cpgallagher.compile',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='django npm staticfiles',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=requirements,
    extras_require={
        'test': ['pytest'],
    },
)
