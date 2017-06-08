from setuptools import setup

version = '0.1.2'

setup(
    name='musical',
    version=version,
    url='https://github.com/wybiral/python-musical/',
    author='Davy Wybiral',
    author_email='davy.wybiral@gmail.com',
    description='A python library for dealing with sounds and music',
    keywords = 'music audio',
    packages=['musical', 'musical.audio', 'musical.theory'],
    platforms='any',
    install_requires=[
    ],
    classifiers=[
    ],
)
