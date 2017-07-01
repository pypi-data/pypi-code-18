
import sys
import re
from setuptools import setup


# reading package version (same way the sqlalchemy does)
with open('beautiful_ansi.py') as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)


def readme():
    def open_file(filename):
        return open(filename, encoding='UTF-8') if sys.version_info >= (3,) else open(filename)

    with open_file('README.rst') as f:
        return f.read()


setup(
    name="beautiful-ansi",
    version=package_version,
    author="Mohammad Hasanzadeh",
    author_email="mohammad@carrene.com",
    py_modules=['beautiful_ansi'],
    description='ANSI escape code library',
    long_description=readme(),
    url='https://github.com/Carrene/beautiful-ansi',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Terminals'

    ],

    keywords='ANSI escape code library',
    python_requires='>=3.6'
)
