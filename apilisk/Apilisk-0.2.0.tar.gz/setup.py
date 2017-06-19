"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Apilisk',
    version='0.2.0',
    description='Remote test runner for Apiwatcher platform',
    long_description=long_description,
    url='https://github.com/apiwatcher/apilisk',
    author='Karel Jakubec',
    author_email='karel@jakubec.name',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Networking :: Monitoring'
    ],
    keywords='http client apiwatcher apilisk',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Apiwatcher-Pyclient>=0.1.2',
        'pycurl',
        'Jinja2',
        'jsonschema',
        'junit-xml',
        'Pygments',
        'pytz'
    ],
    extras_require={
        'dev': ['setuptools'],
        'test': [''],
    },
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
            'apilisk=apilisk.command_line:main'
        ]
    }
)
