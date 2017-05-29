from setuptools import setup, find_packages

setup(
    name="cocoag",
    packages=find_packages(),
    package_data={'': ['cocoag/configuration/default_cocoag.cfg']},
    include_package_data=True,
    version="1.1.1-beta",
    description="Python utility to generate code coverage badges and append them to README's",
    author="David Cyze",
    author_email="mrcyze@gmail.com",
    url="http://cocoag.org",
    download_url="https://github.com/PrettyCities/cocoag",
    keywords=["automation", "code coverage", "testing"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Documentation",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Utilities"
    ],
    install_requires=[
        "boto3>=1.4.4",
        "coverage>=4.4.1",
        "coverage-badge>=0.2.0",
        "pytest>=3.1.0",
        "pytest-cov>=2.5.1"
    ],
    long_description="""\
    Cocoag
    ------

    Uses a JSON config file to create code coverage badges and append them to README files.

    Badge Characteristics:
        - Uploaded to S3 as publicly accessible SVGs
        - Branch dependent (so, different badges will be generated for each branch the utility is run on)

    This version requires Python 3.

    Installation:
    pip install cocoag
    """,
    scripts=['bin/cocoag']
)