# from distutils.core import setup
from setuptools import setup
import setuptools

setup(
    name='LaudaDriver',
    version='1.0.0a5',
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*']),  # ['LaudaDriver'],
    url='https://uni.lardner.io/Jurek/Lauda_driver',
    license='License :: OSI Approved :: Universal Permissive License (UPL)',
    author='Jerzy Dziewierz',
    author_email='jerzy.dziewierz@strath.ac.uk',
    description='Simple helper to control the Lauda thermostat',
    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',
    # Indicate who your project is intended for
    'Intended Audience :: Manufacturing',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Topic :: Scientific/Engineering :: Chemistry',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
    'License :: OSI Approved :: Universal Permissive License (UPL)',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3 :: Only'],
    keywords='Lauda thermostat driver helper',
    install_requires=['pyserial']
)
