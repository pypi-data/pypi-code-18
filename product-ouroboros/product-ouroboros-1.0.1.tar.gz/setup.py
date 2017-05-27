"""Setup file code for the ouroboros library.

"""

from setuptools import setup, find_packages
from setuptools.command.install import install
from os import path

class PostInstallCommand(install):
	def run(self):
		install.run(self)
		import imageio
		imageio.plugins.ffmpeg.download()

here = path.abspath(path.dirname(__file__))

setup(
    name='product-ouroboros',

    version='1.0.0',

    description='A library for simple video editing',

    url='https://github.umn.edu/sebra006/ouroboros',

    author='Product Lab',
    author_email='sebra006@umn.edu',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Topic :: Multimedia :: Video',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='simple video editing',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['moviepy', 'pygame'],
)

#Import imageio after setup installs it via pip.
import imageio
#Install ffmpeg for much of the library functionality
imageio.plugins.ffmpeg.download()
