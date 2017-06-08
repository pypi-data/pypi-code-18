
from operator import attrgetter
from os import path

from pip.req import parse_requirements
from setuptools import setup

def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()


def from_here(relative_path):
    return path.join(path.dirname(__file__), relative_path)


requirements_txt = list(map(str, map(
    attrgetter("req"),
    parse_requirements(from_here("requirements.txt"), session="")
)))

setup(
    name="win10batteryoptimizer",
    version="0.1.1",
    install_requires=requirements_txt,
    packages=["win10batteryoptimizer"],
    license="MIT",
    url="https://github.com/arunkumarpalaniappan/win10batteryoptimizer",
    download_url = 'https://github.com/arunkumarpalaniappan/win10batteryoptimizer/tarball/0.0.1',
    description=(
        "An easy-to-use Python library "
        "for maintaing the optimal battery life for windows 10"
    ),
    include_package_data=True,
    package_data={
        '': ['*.txt']
    },
    long_description=read('README.MD'),
    author="Arunkumar Palaniappan",
    author_email="akrp@live.in",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        'Operating System :: Microsoft',
        'Environment :: Win32 (MS Windows)',
        "License :: OSI Approved :: MIT License",
    ],
)