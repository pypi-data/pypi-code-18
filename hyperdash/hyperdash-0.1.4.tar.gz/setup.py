from setuptools import setup


version = "0.1.4"

setup(
    name='hyperdash',
    packages=['hyperdash'],
    install_requires=[
        'ws4py',
        'six'
    ],
    entry_points={
        'console_scripts': ['hyperdash = hyperdash_cli.cli:main']
    },
    version=version,
    description='Hyperdash.io CLI and SDK',
    author='Hyperdash',
    author_email='support@hyperdash.io',
    url='https://hyperdash.io',
)
