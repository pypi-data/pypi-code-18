from setuptools import setup

setup(
    name='firemon',
    version='0.4.0',
    py_modules=['firemon'],
    install_requires=[
        'psutil',
        'python-slugify'
    ],
    entry_points='''
        [console_scripts]
        firemon=firemon:cli
    ''',
)