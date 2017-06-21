#!/usr/bin/env python

import os
from setuptools import setup, find_packages

def contents(*names):
    root = os.path.abspath(os.path.dirname(__file__))
    return '\n\n'.join(open(os.path.join(root, name)).read() for name in names)

setup(
    name='zsft.recipe.cmd',
    version='0.4',
    description='Buildout recipe to execute commands via shell or python',
    long_description=contents('README.rst', 'CHANGES.rst'),
    author='Zart Software',
    author_email='project-zsft.recipe.cmd@zartsoft.ru',
    url='https://github.com/zartsoft/zsft.recipe.cmd/',
    keywords='buildout recipe shell',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Framework :: Buildout',
        'Framework :: Buildout :: Recipe',
    ],
    
    package_dir={'': 'src'},
    packages=find_packages('src'),
    namespace_packages=['zsft', 'zsft.recipe', 'zsft.recipe.cmd'],
    zip_safe=True,

    install_requires=['setuptools', 'zc.buildout'],
    
    entry_points={
        'zc.buildout': ['default = zsft.recipe.cmd.shell:ShellRecipe'],
    },
)
