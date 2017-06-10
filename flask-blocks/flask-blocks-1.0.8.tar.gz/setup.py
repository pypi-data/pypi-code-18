import setuptools


setuptools.setup(
    name="flask-blocks",
    version="1.0.8",
    description="The common blocks which solve common problems encountered "
                "when creating Flask applications.",
    long_description=open("summary.rst", "r", encoding="utf-8").read(),
    author="Arseni Mourzenko",
    author_email="arseni.mourzenko@pelicandd.com",
    url="http://go.pelicandd.com/n/flaskblocks",
    license="MIT",
    keywords="flask",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    # Since it seems that there is no way to include data with `data_files`,
    # this looks like the only way to include the deployment script and other
    # static files. Since the name of the package is mandatory, any name which
    # exists in the project will work.
    package_data={
        "flaskblocks": [
            "../summary.rst"
        ]
    }
)
