__author__ = 'seanfitz'

from setuptools import setup

setup(
    name = "onyx-parser",
    version = "0.3.0",
    author = "Sean Fitzgerald",
    author_email = "sean@fitzgeralds.me",
    description = ("A text-to-intent parsing framework."),
    license = ("LGPL-3"),
    keywords = "natural language processing",
    url = "https://github.com/OnyxProject/adapt",
    packages = ["adapt", "adapt.tools", "adapt.tools.text"],

    install_requires = [
        "pyee==1.0.1",
        "six==1.10.0"
    ]
)
