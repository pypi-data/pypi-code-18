
from distutils.core import setup

setup(
    name='thinker',
    description='Rethinkdb wrapper for asyncio',
    version="1.1.1",
    author="Mehmet Kose",
    author_email="mehmet@linux.com",
    install_requires=['rethinkdb'],
    url='https://github.com/mehmetkose/thinker',
    keywords='asyncio rethinkdb layer'.split(),
    packages=['thinker'],
    license='MIT',
    platforms=('Any'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Utilities",
    ],
)
