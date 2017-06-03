import os
import pathlib
from setuptools import setup, find_packages

DIR = pathlib.Path(__file__).resolve().parent
os.chdir(DIR)


requires = [
    "miyadaiku"
]

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def list_packages(root):
    yield root
    for dirpath, dirnames, filenames in os.walk(root):
        for d in dirnames:
            if not d.startswith('_'):
                path = os.path.join(dirpath, d).replace(os.path.sep, '.')
                yield path

setup(
    name="miyadaiku.themes.tether",
    version="0.0.1",
    author="Atsuo Ishimoto",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    description='Tether files for miyadaiku static site generator',
    long_description=read('README.rst'),
    packages=list(list_packages('miyadaiku')),
    package_data={
        '': ['*.rst', '*.md', '*.html', '*.css', '*.js', '*.yml', '*.png', '*.jpg', '*.jpeg'],
    },
    install_requires=requires,
    include_package_data=True,
    zip_safe=False
)
