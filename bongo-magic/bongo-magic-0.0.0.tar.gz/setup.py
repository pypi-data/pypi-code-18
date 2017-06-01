
from setuptools import setup
from setuptools import find_packages

setup(
    name="bongo-magic",

    author="Anthony Pizzimenti",
    author_email="anthony-pizzimenti@uiowa.edu",

    install_requires=[
        "pandas",
        "xlsxwriter"
    ],

    packages=find_packages(),

    entry_points={
        "console_scripts": ["magic = magic:main"]
    }
)

