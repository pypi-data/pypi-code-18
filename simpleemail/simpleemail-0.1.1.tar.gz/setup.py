import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='simpleemail',
    version='0.1.1',
    packages=['simpleemail'],
    url='https://github.com/N-C-C/SimpleEmail',
    license='MIT',
    author='John Glasgow',
    author_email='jglasgow@northampton.edu',
    description="Simple SMTP wrapper for Python's SMTP, supports both HTML and text based emails.",
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Communications :: Email",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython"
    ],
)
