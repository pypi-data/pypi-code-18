import os
import io
import re

from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))


def read(*names, **kwargs):
    with io.open(
        os.path.join(here, *names),
        encoding=kwargs.get('encoding', 'utf-8')
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('unable to find version string')


def get_requirements(*file_paths):
    return read(*file_paths).splitlines()


setup(
    name='timera',
    version=find_version('timera', '__init__.py'),
    description='Store metrics in InfluxDB.',
    long_description=read('README.rst'),
    keywords='influxdb system network monitoring',
    author='Nathan Jennings',
    author_email='natej.git@gmail.com',
    url='https://github.com/natej/timera',
    license=read('LICENSE.txt'),
    packages=find_packages(exclude=('.cache', 'build', 'contrib', 'dist', 'docs', 'tests', '.tox')),
    entry_points={
        'console_scripts': [
            'timera = timera.main:main'
        ]
    },
    install_requires=get_requirements('requirements.txt'),
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Database',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
    ],
)
