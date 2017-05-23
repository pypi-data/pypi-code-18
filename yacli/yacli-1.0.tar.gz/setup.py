from setuptools import setup

setup(
    name='yacli',
    version='1.0',
    packages=['yacli', 'yacli.commands', 'yacli.scripts', 'yacli.jar'],
    include_package_data=True,
    install_requires=[
        'click',
        'gitpython'
    ],
    entry_points='''
        [console_scripts]
        yacli=yacli.cli:cli
    ''',
)
