#!/usr/bin/python3
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name="argpar",
	  version="1.2.1",
	  description="A simple arugments parser.",
	  long_description=readme(),
	  url="https://github.com/ondra6ak/argpar.git",
	  author="Ondrej Sestak",
	  author_email="ondra6ak@gmail.com",
	  license="BSD",
	  packages=["argpar"],
	  zip_safe=False)