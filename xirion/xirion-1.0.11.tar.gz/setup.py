import sys
import asciinema
import codelynx
from setuptools import setup

if sys.version_info[0] < 3:
    sys.exit('Python < 3 is unsupported.')

# url_template = 'https://github.com/asciinema/asciinema/archive/v%s.tar.gz'
requirements = []

setup(
    name='xirion',
    version=codelynx.__version__,
    packages=[
        'asciinema', 'asciinema.commands',
        'codelynx', 'codelynx.commands'
    ],
    license='GNU GPLv3',
    description='Terminal session recorder',
    author=codelynx.__author__,
    author_email='trieu@codelynx.io',
    url='http://codelynx.io',
    # download_url=(url_template % asciinema.__version__),
    entry_points={
        'console_scripts': [
            # 'codelynx = codelynx.__main__:main',
            'xirion = asciinema.__main__:main',
        ],
    },
    install_requires=requirements,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Shells',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
)
