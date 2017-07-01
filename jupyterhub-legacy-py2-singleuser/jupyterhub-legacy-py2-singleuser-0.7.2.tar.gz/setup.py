from __future__ import print_function
from setuptools import setup, find_packages
import sys

v = sys.version_info
if v[:2] != (2, 7):
    print("jupyterhub-legacy-singleuser package is only to be used on Python2.7.\n" + \
          "Use jupyterhub package on Python3.3+", file=sys.stderr)
    sys.exit(1)

setup(
    name='jupyterhub-legacy-py2-singleuser',
    version='0.7.2',
    description='Single-user server for running Jupyter Notebooks (on Python2) with JupyterHub',
    url='https://github.com/yuvipanda/jupyterhub-legacy-singleuser',
    author='Yuvi Panda',
    author_email='yuvipanda@gmail.com',
    license='3 Clause BSD',
    packages=find_packages(),
    scripts=['scripts/jupyterhub-singleuser'],
    install_requires=[
        'traitlets>=4.1',
        'tornado>=4.1',
        'jinja2',
        'notebook>=4.0',
        'requests',
        'monotonic'
    ]
)
