from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

import phpmyadmin

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='phpmyadmin',

    version=phpmyadmin.VERSION,

    description='Phpmyadmin docker server',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/iBoneYard/phpmyadmin',

    # Author details
    author='indrajit',
    author_email='eendroroy@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='phpmyadmin docker mysql mariadb',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['docker', 'termcolor'],

    package_data={
        # 'sample': ['package_data.dat'],
    },

    data_files=[
        # ('my_data', ['data/data_file'])
    ],

    entry_points={
        'console_scripts': [
            'pma=phpmyadmin:main',
        ],
    },
)
