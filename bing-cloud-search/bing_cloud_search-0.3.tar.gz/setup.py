import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "bing_cloud_search",
    version = "0.3",
    author = "Tim Edwards",
    author_email = "timedwards8@gmail.com",
    description = ("A method of turning search terms into wordclouds."),
    license = "BSD",
    url = 'https://github.com/tim-shane/cloudy_search',
    keywords = "wordcloud search Bing",
    packages=['bing_cloud_search'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities"
    ],
    install_requires=[
        'wordcloud',
        'matplotlib',
        'numpy',
        'py_ms_cognitive'
]
)