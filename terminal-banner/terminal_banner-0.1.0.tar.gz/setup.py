from setuptools import setup
import re


VERSION_FILE = "terminal_banner/_version.py"
version_text = open(VERSION_FILE, "rt").read()
VERSION_REGEX = r"^__version__ = ['\"]([^'\"]*)['\"]"
version_match = re.search(VERSION_REGEX, version_text, re.M)
if version_match:
    version_string = version_match.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSION_FILE,))

setup(
    name='terminal_banner',
    version=version_string,
    description='Text Banner for Terminals',
    url='https://github.com/martincyoung/terminal_banner',
    packages=['terminal_banner'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    author='Martin Young',
    author_email='martin.young@cantab.net'
)
