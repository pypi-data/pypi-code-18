
from setuptools import setup

version = open('VERSION.txt').read()

setup(name='modconf',
        version=version,
        description='pattern for using python modules as configuration files',
        url='http://github.com/chuck1/modconf',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=['modconf'],
        zip_safe=False,
        )

