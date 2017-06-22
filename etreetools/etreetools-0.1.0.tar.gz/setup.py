from setuptools import setup, find_packages
pkg = "etreetools"
ver = '0.1.0'
setup(
    name             = pkg,
    version          = ver,
    description      = "ElementTree utilities",
    author           = "jikan@cock.li",
    author_email     = "jikan@cock.li",
    license          = "LGPLv3",
    url              = "https://hydra.bacontoast.org/f/etreetools/",
    packages         = find_packages(),
    install_requires = [],
    classifiers      = ["Programming Language :: Python :: 3 :: Only"])
