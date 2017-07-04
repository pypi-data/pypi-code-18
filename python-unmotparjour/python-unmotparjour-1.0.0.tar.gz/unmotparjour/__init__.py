# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request


class UnMotParJour(object):
	"""
	{'word': str, 'definition': str}
	"""

	def __str__(self):
		result = UnMotParJour.__get_word()
		return "# %s\n%s" % (result['word'], result['definition'][:-1])

	@staticmethod
	def __get_word():
		url = "http://unmotparjour.fr/random/"

		html_content = urllib.request.urlopen(urllib.request.urlopen(url).url).read()
		soup = BeautifulSoup(html_content, 'html.parser')

		word = soup.find("h1", {"class": "entry-title"}).get_text()
		definition = soup.find("div", {"class": "entry-content"}).get_text()

		return { 'word': word, 'definition': definition }

	@staticmethod
	def get():
		return UnMotParJour.__get_word()
