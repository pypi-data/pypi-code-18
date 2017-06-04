import os
from setuptools import setup, find_packages
from sys import version_info


description = "Lightweight, route-based and data-type preserving network protocol framework."
long_description = """
.. image:: https://cloud.githubusercontent.com/assets/9287847/26756438/93c1ff54-48a2-11e7-981e-37aeb7b2383c.png
   :height: 80px
   :align: center

.. class:: center

**highway.py**

.. image:: https://img.shields.io/badge/python-3-green.svg
   :height: 20px
   :width: 70px
   :align: left


.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :height: 20px
   :width: 80px
   :align: left


**highway** is a *lightweight*, *route-based* and *data-type
preserving* network protocol framework built on top of *WebSockets*.
It facilitates routes as a means of data transmission.
"""

setup(
	name="highway.py",
	version="0.1",
	author="Philip Trauner",
	author_email="philip.trauner@aol.com",
	url="https://github.com/PhilipTrauner/highway.py",
	packages=find_packages(),
	description=description,
	long_description=long_description,
	install_requires=["ws4py"],
	license="MIT",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
	],
	keywords=["networking", "asynchronous", "data type preserving"]
)
