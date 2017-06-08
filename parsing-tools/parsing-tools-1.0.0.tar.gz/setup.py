import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='parsing-tools',
    version='1.0.0',
    packages=['mimeparser', 'xml2dict',],
    scripts=['bin/walker.py',],
    include_package_data=True,
    license='MIT License',
    description=('A set of utilities to help parse mime types found in '
                 'HTTP headers; Utility to parse XML documents into '
                 'Python objects.'),
    long_description=README,
    url='https://github.com/cnobile2012/python_tools/',
    author='Carl J. Nobile',
    author_email='carl.nobile@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],
    install_requires=[
        'defusedxml',
        'six',
        ],
    )
