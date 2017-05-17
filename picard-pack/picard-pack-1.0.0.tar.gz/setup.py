from setuptools import setup, find_packages

setup(
    name='picard-pack',
    version='1.0.0',
    packages=find_packages(),
    author='picard_username',
    author_email='picarduser@gmail.com',
    url='https://mystack.picard.io/',
    install_requires=['simplejson==3.6.5','requests==2.5.1','fake-factory>=0.5.3','ipaddress>=1.0.16','Babel>=2.2.0']
)