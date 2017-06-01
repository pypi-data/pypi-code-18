import os
import re
from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('blackfynn/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name = "blackfynn",
    version = version,
    author = "Mark Hollenbeck",
    author_email = "mark@blackfynn.com",
    description = "Python client for the Blackfynn Platform",
    packages=find_packages(),
    package_dir={'blackfynn': 'blackfynn'},
    setup_requires=['cython'],
    install_requires = reqs,
    entry_points = {
        'console_scripts': [
            'bf=blackfynn.cli:blackfynn_cli',
        ]
    },
    license = "",
    keywords = "blackfynn client rest api",
    url = "http://github.com/Blackfynn/blackfynn-py",
    download_url = "https://github.com/Blackfynn/blackfynn-py/archive/v1.6.2.tar.gz",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
