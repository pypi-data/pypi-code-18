from setuptools import setup, find_packages

from nameko_opentsdb import __version__


setup(
    name='nameko-opentsdb-py',
    version=__version__,
    author='Sergey Suglobov',
    author_email='s.suglobov@gmail.com',
    packages=find_packages(),
    keywords="nameko, opentsdb, tsdb, metrics",
    url='https://github.com/fraglab/nameko-opentsdb-py',
    description='OpenTSDB dependency for Nameko services',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only'
    ],
    install_requires=[
        'setuptools',
        'nameko',
        'opentsdb-py'
    ]
)
