from setuptools import setup

setup(
    name="v-one-sl",
    version="0.2",
    py_modules=['main'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        v-one=main:cli
    '''
)