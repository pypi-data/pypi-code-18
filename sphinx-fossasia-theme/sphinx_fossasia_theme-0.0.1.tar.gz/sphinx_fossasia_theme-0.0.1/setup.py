from setuptools import setup
import os.path
import sys

readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
if sys.hexversion < 0x03000000:
    readme = open(readme_path).read()
else:
    readme = open(readme_path, encoding='utf-8').read()

setup(
    name = 'sphinx_fossasia_theme',
    version = '0.0.1',
    author = 'Ujjwal Bhardwaj',
    author_email = 'ujjwalb1996@gmail.com',
    url = 'https://github.com/fossasia/sphinx_fossasia_theme',
    license = 'GNU',
    description = 'A Sphinx theme specific to FOSSASIA\'s Projects',
    packages = ['fossasia_theme'],
    include_package_data = True,
    entry_points = {
        'sphinx.html_themes': [
            'name_of_theme = sphinx_fossasia_theme'
        ]
    },
    install_requires = ['sphinx>=1.3'],
  	platforms = 'any',
  	classifiers = [
    	"Framework :: Sphinx :: Extension",
    	"Framework :: Sphinx :: Theme",
    	"Intended Audience :: Developers",
    	"Operating System :: OS Independent",
    	"Topic :: Documentation :: Sphinx",
    	"Topic :: Software Development :: Documentation",
  	],
  	long_description = readme,
)