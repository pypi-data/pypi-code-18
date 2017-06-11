from setuptools import setup, find_packages

setup(
	name='GRP_sample-app',    # This is the name of your PyPI-package.
	version='0.0.2',                          # Update the version number for new releases
	license='GNU',
	packages=find_packages(exclude=['sample_app.test'])
	)