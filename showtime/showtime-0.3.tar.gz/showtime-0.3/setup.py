
from setuptools import setup

setup(name="showtime",
	  version="0.3",
	  description="Stream movies/seasons directly to your vlc. Visit https://github.com/rahulxxarora/showtime for docs",
	  url="https://github.com/rahulxxarora/showtime",
	  author="Rahul Arora",
	  author_email="coderahul94@gmail.com",
	  license='MIT',
	  packages=["showtime"],
	  scripts=["bin/showtime"],
	  install_requires=[
		  'BeautifulSoup4',
		  'requests'],
	  zip_safe=False)
