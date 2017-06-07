from setuptools import setup, find_packages

setup(
	name='git-qi',
	version='0.1.3',
	description='Qi is a search algorithm used to find Git revisions in structured time intervals for later analysis.',
	author='Sage Gerard',
	author_email='sage@sagegerard.com',
	license='MIT',
        download_url='https://github.com/zyrolasting/qi/archive/v0.1.3.tar.gz',
	include_package_data = True,
	packages=find_packages(),
        keywords=['git', 'commit', 'history', 'analysis'],
        install_requires=[
            'python-dateutil'
        ],
	scripts=['bin/qi']
)
