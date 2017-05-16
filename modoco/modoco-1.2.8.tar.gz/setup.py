'''
Install modoco package
'''
from __future__ import print_function
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

# non-foolproof method of protecting against tromping a system MoinMoin
if not hasattr(sys, 'real_prefix'):
    print("This package must be installed in a virtualenv")
    sys.exit(1)

class Install(_install):
    '''
    Custom install command
    '''
    def run(self):

        # * installs MoinMoin
        # * installs any other dependencies
        # * copies data_files to destinations
        _install.run(self)

        # custom post-install configuration of MoinMoin:
        sys.path.insert(0, os.path.join(sys.prefix, 'share/moin')) # put wikiconfig.py on PYTHONPATH
        from modoco.deploy import deploy
        deploy.run()

setup_dir = os.path.abspath(os.path.dirname(__file__))
readme = os.path.join(setup_dir, 'README.rst')
with open(readme) as fh:
    readme_txt = fh.read()

setup(
    # basic info
    name='modoco',
    version='1.2.8',
    packages=find_packages(),

    # install config
    cmdclass={
        'install': Install
    },
    install_requires=[
        'moin>=1.9,<2.0',
    ],
    data_files=[
        ('share/moin', [
            'data_files/wikiconfig.py',
            'data_files/CustomSecurityPolicy.py',
            'data_files/moin.wsgi'])],
    package_data={'modoco':['deploy/moin_package/*']},
    setup_requires=[
        'moin>=1.9,<2.0',
    ],

    # metadata for PyPI
    author='Conrad Leonard',
    author_email='Conrad.Leonard@qimrberghofer.edu.au',
    classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Topic :: Documentation',
            'Topic :: Office/Business :: Groupware',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki',
            ],
    description='MoinMoin wiki configured as document control',
    long_description=readme_txt,
    license='GPLv2',
    url='https://genomeinfo.qimrberghofer.edu.au/svn/genomeinfo/production/modoco',
)
