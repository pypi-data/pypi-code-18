#!/usr/bin/env python

from setuptools import setup, find_packages

readme = ""
for readme_name in ("README", "README.rst", "README.md"):
    try:
        readme = open(readme_name).read()
    except (OSError, IOError):
        continue
    else:
        break


readme = open("README").read()

version = '0.1'

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
    url = "http://code.epic-man.net",
    entry_points = {"console_scripts":["epic-server = epicserver.server:main",]},
    include_package_data = True,
    package_data = {"":["templates/*.html", 
                        "scripts/*.js", 
                        "images/*.png"]},
    install_requires = ['curio'],
    tests_require = ['pytest', 'pytest-coverage', 'pytest-quickcheck', 'mypy']
)

