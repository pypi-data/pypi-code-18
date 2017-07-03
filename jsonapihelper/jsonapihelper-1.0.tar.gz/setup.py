from setuptools import setup
import re

with open("jsonapihelper/__init__.py") as f:
	version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


readme = ''
with open('README.md') as f:
    readme = f.read()


setup(
   name='jsonapihelper',
   version=version,
   description='Package that will convert a api json into a dict',
   author='Kippage',
   longdescription=readme,
   author_email='noop@programmer.net',
   packages=['jsonapihelper'],  #same as name
   install_requires=['requests'], #external packages as dependencies
   classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]

)