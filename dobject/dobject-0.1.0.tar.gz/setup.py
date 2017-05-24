import os
import sys

from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import find_packages

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# reading requirements
install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]
sys.path.insert(0, os.path.dirname(__file__))
version = '0.1.0'
setup(
    name='dobject',
    author='cyriac',
    author_email='me@cyriacthomas.com',
    version=version,
    packages=find_packages(),
    install_requires=reqs,
    include_package_data=True,
    license='MIT',
    description='Dictionary to object tools',
    keywords = ['dobject', 'dictionary', 'object'],
    url='https://github.com/cyriac/dobject',
    download_url = 'https://github.com/cyriac/dobject/archive/v{version}.tar.gz'.format(version=version)
)
