import os
from setuptools import setup

# Utility function to read the README file.  
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

#def read(fname):
#    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "tkPopup",
    version = "0.0.9",
    author = "Franz Beck",
    author_email = "fbeck@intekom.co.za",
    description = "extension to Tkinter: 3 popup classes for user interaction",
    license = "BSD",
    keywords = "tkinter popup user-interaction",
    url = "http://packages.python.org/tkPopup",
#    packages=['tkPopup'],
    py_modules=["tkPopup"],
    long_description="""
The package contains 3 classes, each a pop-up window based on Tkinter.
Purpose is to simplify user-interaction.
Classes **WindowOptions** and **WindowButtons** are multiple choice pop-ups,
Class **WindowEntries** is a multiple parameter input popup
    """,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License"
    ],
)
