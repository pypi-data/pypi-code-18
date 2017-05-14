from setuptools import setup
from codecs import open
from os import path


ROOT_DIR = path.abspath(path.dirname(__file__))

with open(path.join(ROOT_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cproto',
    version='0.1.1',
    description='Chrome Debugging Protocol client',
    long_description=long_description,
    url='https://github.com/asyne/cproto',
    author='Evan K.',
    author_email='cproto+asyne.inout@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='chrome debug client',
    packages=['cproto'],
    install_requires=['websocket-client'],
)
