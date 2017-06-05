# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open

__version__ = "0.2.0"
__author__ = "SkyLothar"
__email__ = "allothar@gmail.com"
__url__ = "http://github.com/skylothar/ocmd"


with open("requirements.txt", "r", "utf-8") as f:
    requires = f.read()


setup(
    name="ocmd",
    version=__version__,
    description="command-line tools for aliyun-oss",
    author=__author__,
    author_email=__email__,
    url=__url__,
    install_requires=requires,
    packages=find_packages(),
    package_data={
        "": ["LICENSE"]
    },
    include_package_data=True,
    entry_points="""
        [console_scripts]
        ocp=ocmd.ocp:ocp
    """,
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4"
    ]
)
