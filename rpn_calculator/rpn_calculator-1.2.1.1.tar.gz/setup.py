import glob
import os

import setuptools

import rpn_calculator.rpn

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.rst'), 'r') as f:
    readme = f.read()

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'release.txt'), 'r') as f:
    requires = f.read().split()

setuptools.setup(
    name='rpn_calculator',
    version=rpn_calculator.rpn.__version__,
    description=rpn_calculator.rpn.__doc__.strip(),
    long_description=readme,
    url='https://github.com/massongit/rpn-calculator',
    author='Masaya SUZUKI',
    author_email='suzukimasaya428@gmail.com',
    license='MIT',
    keywords='RPN Calculator',
    packages=setuptools.find_packages(),
    scripts=glob.glob('bin/*'),
    install_requires=requires,
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'
    ],
)
