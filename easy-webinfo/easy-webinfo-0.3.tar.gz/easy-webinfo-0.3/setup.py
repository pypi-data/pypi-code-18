from setuptools import setup

setup(
name='easy-webinfo',
entry_points={"console_scripts": ['webinfo=webinfo:main',]},
version='0.3',
description="Python command line tool to get some basic info about a website/ip or your pc, using ipinfo.io",
scripts=['webinfo'],
author="Saurabh Chaturvedi",
author_email="saurabh.chaturvedi63@gail.com"
)
