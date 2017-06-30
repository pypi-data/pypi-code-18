import os
import sys

from codecs import open

from setuptools import setup, find_packages


VERSION = '0.9'


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


requires = list()
with open(os.path.join(ROOT, 'requirements.txt'), 'r') as f:
    requires = f.read().split('\n')


with open(os.path.join(ROOT, 'README.md'), 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name='pyVirtualize',
    version=VERSION,
    description='VMware vSphere API helper.',
    long_description=readme,
    author='Rocky Ramchandani',
    author_email='riverdale1109@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
)
