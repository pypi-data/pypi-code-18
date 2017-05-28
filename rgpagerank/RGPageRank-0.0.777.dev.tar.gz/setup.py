"""
A setuptools based setup module.
"""

from setuptools import setup, find_packages

setup(
    name='RGPageRank',

    version='0.0.777 dev',

    description='Find the most relevant information from the given collection of data.',

    url='https://github.com/RomaGilyov/PageRank',

    author='Roman Gilyov',

    author_email='rgilyov@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='page rank algorithm',

    packages=find_packages(exclude=['tests']),

    install_requires=['numpy', 'networkx', 'matplotlib']
)

