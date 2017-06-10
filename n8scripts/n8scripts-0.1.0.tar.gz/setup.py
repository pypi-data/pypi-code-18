import re
from setuptools import setup, find_packages

version_regex = re.compile(r'__version__ = [\'\"]v((\d+\.?)+)[\'\"]')
with open('src/n8scripts/__init__.py') as f:
    vlines = f.readlines()
__version__ = next(re.match(version_regex, line).group(1) for line in vlines
                   if re.match(version_regex, line))

setup(
        name="n8scripts",
        version=__version__,
        description="Nate's handy scripts",
        author="Nathan Henrie",
        author_email="nate@n8henrie.com",
        url="https://github.com/n8henrie/n8scripts",
        packages=find_packages('src'),
        package_dir={"": "src"},
        include_package_data=True,
        entry_points = {
            'console_scripts': ['pushover=n8scripts.n8pushover:cli'],
        },
        license="MIT",
        zip_safe=False,
        classifiers=[
            "Natural Language :: English",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6"
            ],
        )
