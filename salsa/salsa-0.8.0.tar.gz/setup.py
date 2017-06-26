from setuptools import setup, find_packages

setup(
    name='salsa',
    version='0.8.0',
    author='Rit Li',
    author_email='get@rit.li',
    packages=find_packages(exclude=['tests']),
    url='https://bitbucket.org/rit/salsa',
    license='MIT',
    description='SQLAlchemy utility',
    long_description=open('README.rst').read(),
    install_requires=[
        "psycopg2==2.7.1",
        "pytz==2017.2",
        "PyYAML==3.12",
        "SQLAlchemy==1.1.11",
        "yargs==0.8.1",
    ],
)
