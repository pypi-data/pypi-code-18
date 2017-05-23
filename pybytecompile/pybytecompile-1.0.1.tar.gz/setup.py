#!/usr/bin/env python3

from distutils.core import setup

setup(
    description="Wrapper around compileall",
    url="https://github.com/MrWinstead/pybytecompile.git",
    name="pybytecompile",
    version="1.0.1",
    packages=["pybytecompile"],
    scripts=["bin/pybytecompiler.py"],
    author="Mike Winstead",
    author_email="mike@winstead.us"
)
