from setuptools import setup


setup(
	name="who_i",
	description="this about test4",
	version="0.4",
	packages=["who_i"],
	zip_safe=False,
	install_requires=[
		"pyotp",
		]
	)