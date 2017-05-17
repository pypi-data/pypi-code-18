from setuptools import *

setup(
    name='pylights',
    version='2.0',
    description='Module used to change the color and brightness of lights to the beat of an udio file',
    author='Nickolas Howell',
    author_email='nickolas.howell@icloud.com',
    packages=['pylights'],
    install_requires=[
        "pyphue",
        "librosa",
        "pygame"
    ]

)
