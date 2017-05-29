"""
A package intended for use with setuptools that determines the package version
number by parsing the commit specifier from a VCS URL in a requirements.txt
file.
This works assuming a convention that the repository will be tagged as the
version number and that URL will have the tag as the specifier.
"""
from requirements import parse

REQFILE = open("requirements.txt")

def get_version(name, reqfile=REQFILE):
    """
    Given the name of the package and requirements file, determine the
    package version.
    """

    requirements = parse(reqfile)

    for requirement in requirements:
        if name == requirement.name:
            return requirement.revision

    return None

