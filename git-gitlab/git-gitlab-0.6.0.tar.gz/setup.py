#!/usr/bin/env python
import gitgitlab
from setuptools import setup, find_packages

install_requires = ['GitPython>=1.0.1', 'argparse', 'opster==4.1', 'libsaas==0.4', 'libsaas_gitlab==0.3.0.dev0', 'click==6.7']

setup(
    name="git-gitlab",
    scripts=['bin/git-lab'],
    version=gitgitlab.__version__,
    description=gitgitlab.__description__,
    author=gitgitlab.__author__,
    author_email=gitgitlab.__contact__,
    url=gitgitlab.__homepage__,
    platforms=["any"],
    license=gitgitlab.__license__,
    packages=find_packages(),
    install_requires=install_requires,
    zip_safe=False,
    classifiers=[
        # Picked from
        #    http://pypi.python.org/pypi?:action=list_classifiers
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Software Development :: Version Control",
    ]
)
