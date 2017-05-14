
from distutils.core import setup
import pkgutil

import os
from setuptools import setup

with open('requirements.txt') as f:
    reqs = f.read().splitlines()

def getPackages(path="."):
    p = set()
    for importer, modname, ispkg in pkgutil.walk_packages(path=path, onerror=lambda x: None):
	if "." in modname:
	    p.add( modname[:modname.rfind(".")] )
    p.add("lcc/gavo/votable/")
    p.add("lcc/gavo/utils/")
    p.add("lcc/gavo/stc/")
    return p

setup(
  name = 'lcc',
  packages = getPackages(),
  version = '0.9.6',
  description = 'Light Curves Classifier is package for classification stars by using their light curves and metadata',
  author = 'Martin Vo',
  author_email = 'mavrix@seznam.cz',
  url = 'https://github.com/mavrix93/LightCurvesClassifier', 
  download_url = 'https://github.com/mavrix93/LightCurvesClassifier/archive/0.1.tar.gz', 
  install_requires = reqs,
  keywords = ['light curves', 'classifying', 'machine-learning', 'astronomy', 'data-mining'],
  classifiers = [],
)

