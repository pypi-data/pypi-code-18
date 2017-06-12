name = 'j1m.ravenzconfig'
version = '0.1.1'

install_requires = ['setuptools', 'raven', 'ZConfig']
extras_require = dict(test=['manuel', 'mock', 'zope.testing'])

entry_points = """
"""

from setuptools import setup

def read(path):
    with open(path) as f:
        return f.read()

long_description = read('README.rst') + '\n\n' + read('CHANGES.rst')

classifiers = """\
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Microsoft :: Windows
Operating System :: Unix
""".strip().split('\n')

setup(
    author = 'Jim Fulton',
    author_email = 'jim@jimfulton.info',
    license = 'MIT',
    url="https://github.com/jimfulton/j1m.ravenzconfig",

    name = name, version = version,
    long_description = long_description,
    description = long_description.strip().split('\n')[1],
    packages = [name.split('.')[0], name],
    namespace_packages = [name.split('.')[0]],
    package_dir = {'': 'src'},
    install_requires = install_requires,
    zip_safe = False,
    entry_points=entry_points,
    package_data = {name: ['*.txt', '*.test', '*.html', '*.xml']},
    extras_require = extras_require,
    tests_require = extras_require['test'],
    test_suite = name+'.tests.test_suite',
    keywords=['raven', 'zconfig', 'sentry'],
    classifiers=classifiers,
    )
