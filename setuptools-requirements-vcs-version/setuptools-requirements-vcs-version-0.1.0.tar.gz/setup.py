from setuptools import (
    find_packages,
    setup
)

setup(
    author="Daniel Brownridge",
    author_email="daniel@freshnewpage.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    description="Extract package version from requirements.txt VCS URLs",
    install_requires=[
        "requirements-parser",
        "semantic_version",
    ],
    license="MIT",
    name="setuptools-requirements-vcs-version",
    packages=find_packages("src"),
    package_dir={"":"src"},
    url="https://github.com/danielbrownridge/setuptools-requirements-vcs-version",
    version="0.1.0",
)
