
from setuptools import setup
from setuptools import find_packages

from magic import *

setup(
    name="bongo-magic",
    version=VERSION,

    author=AUTHOR,
    author_email=AUTHOR_EMAIL,

    install_requires=[
        "pandas",
        "xlsxwriter",
        "termcolor",
        "blessings"
    ],

    include_package_data=True,

    packages=find_packages(),

    entry_points={
        "console_scripts": ["magic = magic:main"]
    }
)
