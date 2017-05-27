
from setuptools import setup

setup(
    name='nbrequests',
    author='Kristian Perkins',
    author_email='khperkins@gmail.com',
    version='0.0.6',
    url='http://github.com/kristianperkins/nbrequests',
    py_modules=['nbrequests'],
    packages=['nbrequests'],
    package_data={'': ['templates/*']},
    include_package_data=True,
    description='',
    long_description=open('README.rst').read(),
    license='Apache 2.0',
    install_requires=open('requirements.txt').read().split(),
    classifiers=[
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
	'Topic :: Utilities',
    ],
)
