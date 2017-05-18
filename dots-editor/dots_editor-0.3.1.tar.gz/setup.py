from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='dots_editor',
    version='0.3.1',
    description='A python-based six-key braille emulator',
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
    packages=find_packages(),
    install_requires=['pygame', 'argparse'],
    package_data={
        'dots_editor': ['FreeMono.ttf'],
    },
    entry_points={
        'console_scripts': [
            'dots_editor=dots_editor.__main__:main',
        ],
    },
)
