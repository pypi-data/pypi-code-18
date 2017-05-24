try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Python NGINX Plus Status Wrapper',
    'author': 'Eric',
    'url': 'https://github.com/0snug0/ngxPy',
    'download_url': 'https://github.com/0snug0/ngxPy/archive/master.zip',
    'author_email': 'elugo25111@gmail.com',
    'version': '0.2.2',
    'install_requires': ['requests>=2.3.0'],
    'packages': ['ngxpy'],
    'name': 'ngxPy',
}

setup(**config)