from setuptools import setup, find_packages

setup(
    name='picardapi',
    version='1.0.11',
    packages=find_packages(),
    author='picard_username',
    author_email='brig@trialomics.com',
    url='https://picard.io/',
    install_requires=['simplejson>=3.6.5','requests>=2.5.1','ipaddress>=1.0.16','ujson>=1.35']
)