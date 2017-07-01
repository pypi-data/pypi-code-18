
import re
from setuptools import setup


# reading package version (same way the sqlalchemy does)
with open('beautiful_ansi.py') as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)

setup(
    name="beautiful_ansi",
    version=package_version,
    author="Mohammad Hasanzadeh",
    author_email="mohammad@carrene.com",
    py_modules=['beautiful_ansi'],
    description='ANSI escape code library',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python :: 3.6'
    ],

    keywords='ANSI escape code library',
    python_requires='>=3.6'
)
