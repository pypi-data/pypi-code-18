from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dcapi',
    version='0.0.5',
    description='Wrapper for dcapi',
    long_description=long_description,
    url='https://github.com/lethargilistic/dcapi-wrap',
    author='Mike Overby',
    author_email='mikeoverby@outlook.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=['api'],
    packages=find_packages(),
    install_requires=['requests==2.17.3',
                      'wheel==0.29.0'],
)
