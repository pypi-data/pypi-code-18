"""A setuptools based setup module."""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='dynamight',
    version='0.1.0',

    description='Dynamic Strong Typing',
    long_description='A quick and dirty use of Python function annotations to apply strong typing to functions and methods at runtime. If inputs or outputs of a function do not match the type specified in the function annotation, a type error will be thrown. This strong typing is applied to individual functions/classes through a decorator. More documentation is available at the project homepage.',

    # The project's main homepage.
    url='https://github.com/rachel-sharp/dynamight',
    download_url='https://github.com/rachel-sharp/dynamight/archive/0.1.tar.gz',

    # Author details
    author='Rachel Sharp',
    author_email='rachelsharp.dev@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='strong typing dynamic',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # packages=find_packages(exclude=['tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    py_modules=["dynamight"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    extras_require={
        'test': ['pytest'],
    },
)
