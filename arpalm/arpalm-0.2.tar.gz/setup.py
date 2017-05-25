from distutils.core import setup

setup(
	name ="arpalm",
	packages = ["arpalm"],
	version = "0.2",
	description = "ARPA Language Model file builder and parser using CMU Language Modeling Toolkit",
	author = "Igor Bichara",
	author_email = "igor.coutinho@tvglobo.com.br",
	url = "https://github.com/ibichara/arpalm",
	download_url = "https://github.com/ibichara/arpalm/archive/0.2.tar.gz",
	keywords = ['nlp', 'language model'],
	install_requires = ['numpy'],
	classifiers = [])
