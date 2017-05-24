from distutils.core import setup

setup(
	name ="arpalm",
	packages = ["arpalm"],
	version = "0.1",
	description = "ARPA Language Model file builder and parser using CMU Language Modeling Toolkit",
	author = "Igor Bichara",
	author_email = "igor.coutinho@tvglobo.com.br",
	url = "https://github.com/ibichara/arpalm",
	download_url = "https://github.com/ibichara/arpalm/archive/0.1.tar.gz",
	keywords = ['nlp', 'language model'],
	install_requires = ['numpy'],
	classifiers = [])
