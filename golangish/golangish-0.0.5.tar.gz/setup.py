from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.5'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


install_requires = ['sphinx', 'flake8'] 
dependency_links = []

setup(
    name='golangish',
    version=__version__,
    description="Port Golang's CSP semantics to Python",
    long_description=long_description,
    url='https://github.com/edouardklein/golangish',
    download_url='https://github.com/edouardklein/golangish/tarball/' + __version__,
    license='AGPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='CSP, Golang, Channel, Coroutine, Select',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Edouard Klein',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='myfirstnamemylastname@mailproviderthatstartswithagfromgoogle'
    '.whyshouldibespammed.letmeinputhateveriwantinthisfieldffs.com'
)
