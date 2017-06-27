from codecs import open
from os import path
from setuptools import setup

from stately import __version__


ROOT_DIR = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(ROOT_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stately',
    version=__version__,
    description='Dignified state transitions for Python',
    long_description=long_description,
    url='https://github.com/folz/stately',
    author='Rodney Folz',
    author_email='pypi@rodneyfolz.com',
    license='MPL-2.0',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='finite state machine transition redux',
    packages=['stately'],
    python_requires='~=3.5',
    install_requires=[],
    extras_require={
        'dev': ['check-manifest', 'twine', 'wheel'],
        'test': ['coverage'],
    },
)
