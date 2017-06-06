import os
from setuptools import setup

if os.path.isfile("README.md"):
    with open("README.md") as readme:
        long_description = readme.read()
else:
    long_description = None


setup(
    name="CodeStats",
    version="1.1.0",
    description="Wrapper around the Code::Stats API",
    long_description=long_description,
    author="Niek Keijzer",
    author_email="info@niekkeijzer.com",
    url="https://www.github.com/niekkeijzer/codestats/",
    download_url="https://github.com/NiekKeijzer/CodeStats/archive/1.1..tar.gz",
    packages=[
        "codestats"
    ],
    install_requires=[
        "requests>=2.17.3"
    ]
)
