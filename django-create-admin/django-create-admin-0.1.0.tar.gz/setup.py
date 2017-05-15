import os
from setuptools import setup, find_packages


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_description():
    with open('README.rst') as f:
        return f.read()


setup(
    # Package meta-data
    name='django-create-admin',
    version='0.1.0',
    description='Django management commands to create admin users.',
    long_description=get_description(),
    author='Chathan Driehuys',
    author_email='cdriehuys@gmail.com',
    url='https://github.com/cdriehuys/django-create-admin',
    license='MIT',

    # Additional classifiers for PyPI
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Supported versions of Django
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',

        # Supported verrsions of Python
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # Include the actual source code
    packages=find_packages(),

    # Dependencies
    install_requires=['django >= 1.8, < 1.12'],
    )
