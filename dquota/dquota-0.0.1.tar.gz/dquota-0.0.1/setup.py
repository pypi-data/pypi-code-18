from setuptools import setup
from setuptools import find_packages

setup(
    name = 'dquota',
    version = '0.0.1',
    description = 'Handle quota notifications using generic netlink',
    url = 'https://github.com/ton31337/dquot-python',
    download_url = 'https://github.com/ton31337/dquot-python/tarball/0.0.1',
    packages = find_packages(),
    install_requires = [
        'pika',
        'redis',
        'json',
    ]
)

