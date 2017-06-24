"""
Build tnseq_yeast.
"""
import sys
from setuptools import setup, Extension

if sys.version_info < (2, 6):
     sys.stdout.write("At least Python 2.6 is required.\n")
     sys.exit(1)

requirements = [line.strip() for line in open('requirements.txt')]

setup(
    name = 'tnseq_yeast',
    version = '0.5.1', #versioneer.get_version(),
    author = 'Jim Chu',
    author_email = 'biojxz@163.com',
    url = 'https://tnseq_yeast.readthedocs.io/',
    description = 'trim adapters from high-throughput sequencing reads',
    license = 'MIT',
    #cmdclass = cmdclass,
    #ext_modules = extensions,
    packages = ['tnseq_yeast'], # 'tnseq_yeast.scripts'],
    scripts = ['bin/tnseqy'],
    install_requires = requirements,
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)
