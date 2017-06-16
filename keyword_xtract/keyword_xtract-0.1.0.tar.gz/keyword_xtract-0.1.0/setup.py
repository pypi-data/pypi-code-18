from distutils.core import setup
from setuptools import find_packages

setup(
  name='keyword_xtract',
  packages=find_packages(where="src"),
  package_dir={"": "src"},
  version='0.1.0',
  description='Keyword extraction with RAKE, and keyword ranking using vector representations - created as part'
              'of a toy challenge',
  author='Belal Chaudhary',
  author_email="belalc80@gmail.com",
  url='https://github.com/BelalC/keyword_i2x',
  download_url='https://github.com/peterldowns/mypackage/archive/0.1.tar.gz',
  keywords=['keyword', 'key phrase', 'RAKE', 'word2vec'],
  classifiers=[
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.5"]
)