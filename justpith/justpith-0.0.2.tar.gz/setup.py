from setuptools import setup

setup(
    name = "justpith",
    version = "0.0.2",
    author = "Antonio Carisita",
    author_email = "a.caristia@gmail.com",
    description = ("Core code for justpith infrastructure"),
    license = "GPL",
    keywords = "justpith's core",
    url = "http://packages.python.org/justpith",
    packages=['rabbit'],
    install_requires=[
          'pika',
    ],
    zip_safe=False
)
