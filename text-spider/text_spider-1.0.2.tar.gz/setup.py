#   Copyright (c) 2017, Pan Labs (panorbit.in).  
#   This file is licensed under the MIT License.
#   See the LICENSE file.

from setuptools import setup,find_packages

setup(
	name='text_spider',
	version='1.0.2',
	description='text scraping spider',
	url='http://panorbit.in/',
	author="prajwal",
	author_email="labs@panorbit.in",
	license="MIT",
	packages=find_packages(),
        classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
         ],
         install_requires=['requests'],
         scripts=['scripts/text-spider'],

	)
