from distutils.core import setup

from setuptools import find_packages

from metadata import Metadata


if __name__ == "__main__":
    setup(
        name=Metadata.name,
        version=Metadata.version,
        description=Metadata.description,
        author=Metadata.author,
        author_email=Metadata.author_email,
        license=Metadata.license,
        url=Metadata.repository_url,
        download_url=Metadata.download_url,
        keywords=Metadata.keywords,
        requires=Metadata.requires,
        packages=find_packages()
    )
