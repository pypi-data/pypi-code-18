#!/usr/bin/env python

from setuptools import setup, find_packages

readme = open('README.rst').read()

version = '0.1.1'

setup(
    name = "epicserver",
    version = version,
    packages = ["epicserver"],
    author = "Da_Blitz",
    author_email = "epiccode@epic-man.net",
    description = "Online Persistent game infrastructure",
    long_description = readme,
    license = "MIT BSD",
    keywords = "game mmo rpg asyncio",
#    url = "http://code.epic-man.net",
    url = "http://blitz.works/epic/epic-server",
    entry_points = {"console_scripts":["epic-server = epicserver.server:main",]},
    include_package_data = True,
    package_data = {"":["templates/*.html", 
                        "scripts/*.js", 
                        "images/*.png"]},
    install_requires = ['curio'],
    tests_require = ['pytest', 'pytest-coverage', 'mypy', 'hypothesis']
)

