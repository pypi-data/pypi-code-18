from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='dots_editor',
    use_scm_version=True,
    description='A six-key brailler emulator written in python.',
    long_description=long_description,
    author='Gail Terman',
    author_email='gterman@gmail.com',
    license='MIT',
    url='https://github.com/Gailbear/dots-editor',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Text Editors',
        'Topic :: Text Editors :: Text Processing',
    ],
    keywords='braile pygame editor',
    packages=find_packages(exclude=['tests']),
    install_requires=['pygame', 'argparse', 'setuptools_scm'],
    package_data={
        'dots_editor': ['FreeMono.ttf'],
    },
    entry_points={
        'console_scripts': [
            'dots_editor=dots_editor.__main__:main',
        ],
    },
)
