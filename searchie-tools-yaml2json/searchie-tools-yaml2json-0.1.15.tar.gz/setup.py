from setuptools import setup, find_packages
from yaml2json.version import __version__ as package_version

setup(
    name="searchie-tools-yaml2json",
    description="Utility to convert YAML files to JSON format",
    version=package_version,
    maintainer="Eugene Krokhalev",
    maintainer_email = "rutsh@searchie.org",
    install_requires=[
        "pyyaml"
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "yaml2json = yaml2json:main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Utilities"
    ]
)
