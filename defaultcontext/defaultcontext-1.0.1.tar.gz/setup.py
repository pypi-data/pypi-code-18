from os import path
from codecs import open
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name = "defaultcontext",
    version = "1.0.1",
    author = "Bogdan Kulynych",
    author_email = "hello@bogdankulynych.me",
    description = "Tiny util for creating tensorflow-like context managers for default instances of classes",
    url = "https://github.com/bogdan-kulynych/defaultcontext",
    license = "MIT",
    keywords = "utils",
    packages=find_packages(exclude=["tests"]),
    long_description=long_description,
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
