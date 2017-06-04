import sys
from distutils.core import setup

message = "I don't mean to be pedantic, but you meant to install pydantic!"

argv = lambda x: x in sys.argv

if (argv('install') or  # pip install ..
        (argv('--dist-dir') and argv('bdist_egg'))):  # easy_install
    raise Exception(message)


if argv('bdist_wheel'):  # modern pip install
    raise Exception(message)


setup(
    name='pyandtic',
    version='0.0.1',
    maintainer='Thomas Grainger',
    maintainer_email='pyandtic@graingert.co.uk',
    long_description=message,
    url='https://github.com/samuelcolvin/pydantic',
)
