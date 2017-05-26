from setuptools import setup

from firemon import VERSION

setup(
    name='firemon',
    version=VERSION,
    py_modules=['firemon'],
    install_requires=[
        'psutil',
        'python-slugify',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        firemon=firemon:cli
    ''',
)