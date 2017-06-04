from setuptools import setup

setup(
    name='very_basic_sql_builder',
    version='1.0.0',
    py_packages=['sql_cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        vbsql=sql_cli:main
    ''',
)
