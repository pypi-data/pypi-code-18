from setuptools import setup
from contextlib import contextmanager


@contextmanager
def custom_open(filename):
    f = open(filename)
    try:
        yield f
    finally:
        f.close()


with custom_open('requirements.txt') as f:
    contents = f.read()

with custom_open('requirements.txt') as f:
    long_d = f.read()

setup(
    name='forbesqotd',
    version='1.0',
    description='QOTD on Forbes Welcome page',
    long_description=long_d,
    url='https://github.com/appi147/forbes-qotd',
    author='Arpit Choudhary',
    author_email='arpitkumar147@gmail.com',
    keywords=['forbes', 'qotd'],
    license='MIT',
    packages=['forbesqotd'],
    classifiers=['Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.5',
                 'License :: OSI Approved :: MIT License'],
    install_requires=contents,
    scripts=['bin/qotd']
)
