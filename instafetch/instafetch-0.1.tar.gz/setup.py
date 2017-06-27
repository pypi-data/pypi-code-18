from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()



version = '0.1'

install_requires = [
    "requests"
]


setup(name='instafetch',
    version=version,
    description="Python package to get instagram data",
    long_description=README,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='Instagram API Python',
    author='Paras Sharmaa',
    author_email='mail2paras.s@gmail.com',
    url='',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['instafetch=instafetch:main']
    }
)

