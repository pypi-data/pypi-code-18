from distutils.core import setup

setup(
    # Application name:
    name="django_framework",

    # Version number (initial):
    version="0.1.2",

    # Application author details:
    author="name surname",
    author_email="name@addr.ess",

    # Packages
    packages=["django_framework"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/MyApplication_v010/",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
    ],
)