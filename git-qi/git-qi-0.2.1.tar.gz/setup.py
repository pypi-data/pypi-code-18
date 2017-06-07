from setuptools import setup, find_packages

setup(
	name='git-qi',
	version='0.2.1',
	description='Qi prints Git revisions in structured time intervals for later analysis.',
	author='Sage Gerard',
	author_email='sage@sagegerard.com',
	license='MIT',
        download_url='https://github.com/zyrolasting/qi/archive/v0.2.1.tar.gz',
	include_package_data = True,
	packages=find_packages(),
        keywords=['git', 'commit', 'history', 'analysis'],
        install_requires=[
            'python-dateutil'
        ],
	scripts=['bin/qi']
)
