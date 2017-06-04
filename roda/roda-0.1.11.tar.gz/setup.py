from setuptools import setup, find_packages

setup(
    name='roda',
    version='0.1.11',
    packages=find_packages(where='src'),
    package_dir = {'':'src'},
    install_requires=['nose'],
    author='x6doooo',
    author_email='x6doooo@gmail.com',
    description='...',
    license='MIT',
)
