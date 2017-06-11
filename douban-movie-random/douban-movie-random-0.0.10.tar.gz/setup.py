"""A simple tool for finding random douban moive of your wishes.
"""

from setuptools import setup, find_packages
from pip.req import parse_requirements

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

install_reqs = parse_requirements('./requirements.txt', session=False)

reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="douban-movie-random",

    version="0.0.10",

    description="A simple tool for finding random douban moive of your wishes",

    long_description=long_description,

    url="https://github.com/acwong00/douban-movie-random-py",

    author="acwong",
    author_email="acwong00@gmail.com",

    license="MIT",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],

    keywords="movie douban commandline",

    packages=find_packages(),

    install_requires=reqs,

    entry_points={
        'console_scripts': [
            'dmrandom=dmrandom.index:main',
        ],
    },
)