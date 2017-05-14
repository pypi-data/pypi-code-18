from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md")) as readme:
    long_description = readme.read()

classifiers = [
    # Development status
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',
    # Intended users
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    # License
    'License :: OSI Approved :: MIT License',
    # Supported Python version(s)
    'Programming Language :: Python :: 3.5',
]

setup(
    name="plinq",
    version="0.2",
    packages=["plinq"],
    url="https://bitbucket.org/herf/plinq",
    license="MIT",
    author="Rudolf Heszele",
    author_email="heszele@gmail.com",
    description="LINQ implementation for Python",
    long_description=long_description,
    classifiers=classifiers,
    keywords="linq python"
)
