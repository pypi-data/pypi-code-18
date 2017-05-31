from setuptools import setup

setup(
    name='pdfsort',
    version='0.1.1',
    py_modules=['idk'],
    install_requires=[
        'Click',
        'PyPDF2',
    ],
    entry_points='''
        [console_scripts]
        pdfsort=pdfsort:cli
        kedsort=pdfsort:kedsort
    ''',
)
