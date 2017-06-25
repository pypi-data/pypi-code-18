from setuptools import setup, find_packages

setup(
    name='yargs',
    version='0.8.1',
    author='Rit Li',
    author_email='get@rit.li',
    packages=find_packages(exclude=['*.tests']),
    url='https://bitbucket.org/rit/yargs',
    license='MIT',
    description='Create CLI options from yaml',
    long_description=open('README.rst').read(),
    install_requires=[
        "PyYAML==3.12",
    ],
)
