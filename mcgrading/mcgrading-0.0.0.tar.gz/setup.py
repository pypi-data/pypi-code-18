import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mcgrading",
    version = "0.0.0",
    author = "Juan Barbosa",
    author_email = "js.barbosa10@uniandes.edu.co",
    description = ('Build to serve at UniAndes.'),
    license = "GPL",
    keywords = "example documentation tutorial",
    url = "http://github.com/jsbarbosa/mcgrading",
    packages=['mcgrading'],
    install_requires=['pebble', 'importlib'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
)
