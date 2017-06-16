from setuptools import find_packages, setup

from pytrivia import __version__

setup(
    name='Python-Trivia-API',
    packages=find_packages(),
    version=__version__,
    install_requires=[
        'aiohttp',
        'async-timeout',
        'certifi',
        'chardet',
        'idna',
        'multidict',
        'requests',
        'urllib3',
        'yarl'
    ],
    url='https://github.com/MaT1g3R/Python-Trivia-API',
    license='MIT',
    author='MaT1g3R',
    author_email='mat1g3r@gmail.com',
    description='An API wrapper for opentdb',
    keywords=['api', 'trivia', 'opentdb'],
)
