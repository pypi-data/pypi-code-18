import os

from setuptools import setup

PACKAGE = os.path.basename(os.path.dirname(os.path.abspath(__file__))).replace('-', '_')
setup(
    name=PACKAGE,
    version='0.0.1',
    packages=[PACKAGE],
    description = "A python package skeleton/template creator.",
    author="Jason Viloria",
    author_email = "jnvilo@gmail.com",
    url="https://github.com/jnvilo/packageskel",
    download_url = "https://github.com/jnvilo/packageskel/archive/master.zip",
    keywords = ["packaging", "package", "skeleton", "template"],
    test_suite='tests',
    entry_points = {
        'console_scripts': ['packageskel=packageskel.packageskel:make_template']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
    include_package_data=True

)
