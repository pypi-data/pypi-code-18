
from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
     name='diu',    # This is the name of your PyPI-package.
    scripts=['diu.py'],                  # The name of your scipt, and also the command you'll be using for calling it
    version = "0.0.4",
    author = "Andrew Carter",
    author_email = "mkoh2016@gmail.com",
    description = ("the description for diu test"),
    license = "buy 1-free-1",
    keywords = "diu",
    url = "https://tinyurl.com/#example",
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
     )
