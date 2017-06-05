from setuptools import setup

setup(
    name='very_basic_sql_builder',
    version='1.0.7',
    packages=['sql_cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        ebsql=sql_cli:main
        vbsql=sql_cli.sql_cli:main
    ''',
)
