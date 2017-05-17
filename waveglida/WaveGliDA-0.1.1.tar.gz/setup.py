from setuptools import setup

setup(
    # Application name:
    name="WaveGliDA",

    # Version number (initial):
    version="0.1.1",

    # Application author details:
    author="Luke Gregor",
    author_email="luke.e.gregor@gmail.com",

    # Packages
    packages=["WaveGliDA/", 'WaveGliDA/static', 'WaveGliDA/templates', 'WaveGliDA/data'],

    # Include additional files into the package
    include_package_data=True,

    # this creates a command line thingy
    entry_points={'console_scripts': ['WaveGliDA = WaveGliDA.__main__:main']},

    # Details
    url="http://luke-gregor.github.io",

    #
    # license="LICENSE.txt",
    description="Import and quick plot ocean surface CO2 data from a wave glider",

    long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "click",
        "Flask",
        "itsdangerous",
        "Jinja2",
        "MarkupSafe",
        "numpy",
        "pandas",
        "PyExcelerate",
        "Pygments",
        "python-dateutil",
        "pytz",
        "seawater",
        "six",
        "Werkzeug",
    ],
)
