from setuptools import setup

from src.roda import __version__

setup(
    name='roda',
    version=__version__,
    packages=['roda'],
    package_dir={'': 'src'},
    install_requires=['nose'],
    author='x6doooo',
    author_email='x6doooo@gmail.com',
    description='...',
    license='MIT',
)
