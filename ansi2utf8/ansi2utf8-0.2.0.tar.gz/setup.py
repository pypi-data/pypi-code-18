# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
from ansi2utf8 import __version__

setup(
    name = 'ansi2utf8',
    version = __version__,
    description = 'ANSI to UTF-8',
    url = 'https://github.com/SmilingXinyi/ansi2utf8',
    author = 'blaite',
    author_email = 'smilingxinyi@gmail.com',
    license = 'MIT',
    keywords = 'a2u ansi2utf8',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'Click',
        'ansicolors'
    ],
    entry_points={
        'console_scripts': [
            'a2u = ansi2utf8.main:entry'
        ]
    }
)