from distutils.core import setup

"""
In this dist, we obtain several modules:
sorting: normal sorting algrithms
pagerank: pagerank algrithm
"""

setup(
    name         = 'pyalgms',
    version      = '1.0.0',
    py_modules   = ['sorting'],
    author       = 'sky_pp',
    author_email = 'sky_pypi@163.com',
    url          = '',
    description  = 'Common algrithms implemented with python3',
    )
