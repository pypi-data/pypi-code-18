import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "git-pythonpath",
    version = "0.1.1",
    author = "Dean Shaff",
    author_email = "dean.shaff@gmail.com",
    description = ("Temporarily add code in a git repo to python path."),
    install_requires=[
    ],
    packages=["git_pythonpath"],
    keywords = "git",
    url = "https://github.com/dean-shaff/git-pythonpath",
    data_files = [("", ["LICENSE"])]
)
