#!/usr/bin/env python

from setuptools import setup

setup(name="pyparsec",
      version="0.5",
      description="Parsec From Haskell Python 3 Portable",
      long_description="""
Parsec is a Haskell combinator library, PyParsec is a parsec library for python 3+
""",
      author="marsliu",
      author_email="mars.liu@outlook.com",
      url="https://github.com/Dwarfartisan/pyparsec",
      license="MIT",
      packages=["parsec", "test"],
      package_dir={
          "parsec": "src/parsec",
          "test": "src/tests"
      },
      classifiers=[
         "Topic :: Utilities",
         "License :: OSI Approved :: MIT License"
      ]
)
