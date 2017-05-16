from setuptools import setup, find_packages
import os

setup(
    name='awshelpers',
    description='A package containing modules for common AWS SDK tasks.',
    long_description=open('README.rst').read(),
    version="0.0." + os.environ['TRAVIS_BUILD_NUMBER'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='aws ssm s3 python sdk wrapper',
    packages=find_packages(),
    install_requires=[
        'boto3',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    url='https://pypi.python.org/pypi/awshelpers',
    license='MIT',
    author='Travis Dolan',
    author_email='travis.dolan@gmail.com',
    include_package_data=True
)
