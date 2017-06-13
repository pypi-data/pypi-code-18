from setuptools import setup, find_packages

setup(
	name="eventflow",
	version="0.1.dev5",
	author="NIPE-SYSTEMS",
	url = "https://github.com/NIPE-SYSTEMS/eventflow",
	download_url = "https://github.com/NIPE-SYSTEMS/eventflow/archive/0.1.dev3.tar.gz",
	packages=[ "eventflow_cli", "eventflow" ],
	include_package_data=True,
	install_requires=[
		"click", "pydbus==0.6.0", "pygobject"
	],
	entry_points={
		"console_scripts": [
			"eventflow = eventflow_cli.cli:cli"
		]
	}
)
