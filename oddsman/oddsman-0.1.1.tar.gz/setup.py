from setuptools import setup, find_packages
with open('README.md') as f:
        readme = f.read()

setup(
        name             = 'oddsman',
        version          = '0.1.1',
        description      = 'this module extracts odds(rate) of hourse race held today ',
        license          = 'MIT',
        author           = 'phayate',
        long_description = readme,
        author_email     = 'pinqphayat@gmail.com',
        url              = 'https://github.com/PinkPhayate/OddsWatcher',
        keywords         = 'hourse race odds',
        packages         = find_packages(),
        install_requires = ['bs4>=0.0.1', 'request>=0.0.13']
        )
