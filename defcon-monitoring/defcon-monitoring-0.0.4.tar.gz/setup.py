#!/usr/bin/env python
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

def _read(relpath):
    fullpath = os.path.join(os.path.dirname(__file__), relpath)
    with open(fullpath) as f:
        return f.read()


def _read_reqs(relpath):
    fullpath = os.path.join(os.path.dirname(__file__), relpath)
    with open(fullpath) as f:
        return [s.strip() for s in f.readlines()
                if (s.strip() and not s.startswith("#"))]


_REQUIREMENTS_TXT = _read_reqs("requirements.txt")
_TESTS_REQUIREMENTS_TXT = _read_reqs("tests-requirements.txt")
_DEPENDENCY_LINKS = [l for l in _REQUIREMENTS_TXT if "://" in l]
_INSTALL_REQUIRES = [l for l in _REQUIREMENTS_TXT if "://" not in l]
_TEST_REQUIRE = [l for l in _TESTS_REQUIREMENTS_TXT if "://" not in l]

setup(
    name='defcon-monitoring',
    version='0.0.4',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
    install_requires=_INSTALL_REQUIRES,
    dependency_links=_DEPENDENCY_LINKS,
    tests_require=_TEST_REQUIRE,
    description='defcon.',
    long_description=README,
    url='http://github.com/iksaif/defcon',
    author='Corentin Chary',
    author_email='corentin.chary@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
