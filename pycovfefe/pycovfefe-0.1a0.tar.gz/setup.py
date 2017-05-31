import os
from setuptools import setup, find_packages


if os.path.exists('README.rst'):
    long_description = open('README.rst', 'r').read()
else:
    long_description = 'See https://bitbucket.org/petersanchez/pycovfefe/'


setup(
    name='pycovfefe',
    version=__import__('covfefe').get_version(),
    packages=find_packages(),
    description='Python Interface for covfefe caliber content generation.',
    author='Peter Sanchez',
    author_email='petersanchez@gmail.com',
    url='https://bitbucket.org/petersanchez/pycovfefe/',
    long_description=long_description,
    platforms=['any'],
    entry_points={
        'console_scripts': [
            'covfefe = covfefe.covfefe:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    include_package_data=True,
)
