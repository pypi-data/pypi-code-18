import os
import sys

from distutils.core import setup

def publish():
    """Publish to PyPi"""
    os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
    publish()
    sys.exit()

required = []

setup(
        name='cxyrequests',
        version='0.0.1',
        description='Learn python requests',
        long_description=open('README.rst').read() + '\n\n' +
                         open('HISTORY.rst').read(),
        author='crouchred',
        author_email='crouchred@gmail.com',
        url='https://github.com/crouchred/cxyrequests',
        packages= [
                'cxyrequests',
        ],
        install_requires=required,
        license='ISC',
        classifiers=(
                # 'Development Status :: 5 - Production/Stable',
                'Intended Audience :: Developers',
                'Natural Language :: English',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python',
                # 'Programming Language :: Python :: 2.5',
                'Programming Language :: Python :: 2.6',
                'Programming Language :: Python :: 2.7',
                # 'Programming Language :: Python :: 3.0',
                # 'Programming Language :: Python :: 3.1',
        ),
)
