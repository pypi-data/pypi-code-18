import os
import sys
from distutils.core import setup
from glob import glob


if 'develop' in sys.argv or any(a.startswith('bdist') for a in sys.argv):
    import setuptools  # NoQA

setup_args = dict(
    name='sqre_labkubespawner',
    scripts=glob(os.path.join('cli_scripts', '*')),
    version='0.0.6',
    packages=['sqre_labkubespawner'],
    author='Project Jupyter',
    author_email='jupyter@googlegroups.com',
    keywords=['jupyterlab', 'jupyterlab extension'],
    include_package_data=True,
    install_requires=[
        'jupyterlab>=0.21.0',
        'requests<3.0.0'
    ]
)

if __name__ == '__main__':
    setup(**setup_args)
