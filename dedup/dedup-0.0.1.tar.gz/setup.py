# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup

version = "0.0.1"

setup(
    name="dedup",
    packages=["dedup"],
    entry_points={
        "console_scripts": ['dedup = dedup.dedup:main']
    },
    version=version,
    description="dedup",
    long_description="dedup-long",
    author="Ben",
    url="https://github.com/bchiang2/dedup",
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    install_requires=['fire'],
)
