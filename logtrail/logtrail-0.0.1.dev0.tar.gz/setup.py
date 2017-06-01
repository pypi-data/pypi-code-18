from os import path
from codecs import open
from setuptools import setup

from logtrail import VERSION

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def find_packages(*args, **kwargs):
    return ['logtrail']

install_requires = []


tests_require = [
    'nose',
    'coverage',
]

extras_require = {}

setup(
    name='logtrail',
    version=VERSION,
    description="A fancy logger",
    long_description=long_description,
    url='https://github.com/eendroroy/logtrail',
    author='indrajit',
    author_email='eendroroy@gmail.com',
    license='MIT',

    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
        'Topic :: System :: Shells',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    include_package_data=True,
    zip_safe=True,
    packages=find_packages()
)
