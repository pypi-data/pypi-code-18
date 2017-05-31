from distutils.core import setup

with open("README.rst", 'r') as f:
    long_description = f.read()

setup(
    name='imap_tools',
    version='0.1.3',
    packages=['imap_tools'],
    url='https://github.com/ikvk/imap_tools',
    license='MIT',
    long_description=long_description,
    author='v.kaukin',
    author_email='workkvk@gmail.com',
    description='Tool for work with e-mail messages and not with the imap protocol.',
)
