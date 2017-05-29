#!/usr/bin/env python

import sys
from setuptools import setup

install_requires = [
    "easygui"
]

setup(name="bigletters",
      version="0.4.4",
      author="Leo Fitzpatrick",
      author_email="leocfitz@gmail.com",
      description="It makes letters bigger!",
      packages=["bigletters"],
      entry_points={
          "console_scripts": [
              "bigletters=bigletters.main:main"
          ]
      },
      install_requires=install_requires,
      url="https://gliggy.github.io/Gligslife/"
      )
