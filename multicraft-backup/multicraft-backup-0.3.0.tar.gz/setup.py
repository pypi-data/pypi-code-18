import setuptools

def get_long_description(filename):
	with open(filename) as f:
		return f.read()

setuptools.setup(
	name="multicraft-backup",
	version="0.3.0",
	url="https://github.com/bmintz/multicraft-backup",

	author="Benjamin Mintz",
	author_email="bmintz@protonmail.com",

	description="Backs up your Minecraft servers from hosts that use Multicraft",
	long_description=get_long_description('README.rst'),

	packages=setuptools.find_packages(),

	install_requires=('selenium', 'ftputil',),

	classifiers=[
		'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

		'Development Status :: 2 - Pre-Alpha',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
	],
)
