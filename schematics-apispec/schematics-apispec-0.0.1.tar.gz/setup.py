import re
from setuptools import setup, find_packages


def find_version(filename):
    """
    Attempts to find the version number in the file named filename.
    Raises RuntimeError if not found.
    """

    version = ''

    with open(filename, 'r') as file_:
        regex = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')

        for line in file_:
            match = regex.match(line)

            if match:
                version = match.group(1)
                break

    if not version:
        raise RuntimeError('Cannot find version information')

    return version


__version__ = find_version("schematics_apispec/__init__.py")


def read(filename):
    with open(filename) as file_:
        content = file_.read()
    return content


setup(
    name='schematics-apispec',
    version=__version__,
    description='A schematics plugin for documenting REST APIs with apispec.',
    long_description=read('README.rst'),
    author='Douglas Treadwell',
    author_email='douglas.treadwell@gmail.com',
    url='https://github.com/douglas-treadwell/schematics-apispec',
    packages=find_packages(exclude=('tests', 'examples', 'docs')),
    package_dir={'schematics_apispec': 'schematics_apispec'},
    include_package_data=True,
    install_requires=['apispec', 'schematics'],
    license='MIT',
    keywords='schematics apispec swagger openapi specification documentation spec rest api',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    test_suite='tests'
)
