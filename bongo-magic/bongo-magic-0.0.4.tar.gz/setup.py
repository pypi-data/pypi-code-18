
from setuptools import setup
from setuptools import find_packages

setup(
    name="bongo-magic",
    version="0.0.4",

    author="Anthony Pizzimenti",
    author_email="anthony-pizzimenti@uiowa.edu",

    install_requires=[
        "pandas",
        "xlsxwriter"
    ],

    include_package_data=True,

    packages=find_packages(),

    entry_points={
        "console_scripts": ["magic = magic:main"]
    }
)

