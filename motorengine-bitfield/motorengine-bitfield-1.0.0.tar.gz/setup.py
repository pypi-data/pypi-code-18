from setuptools import setup
from sys import argv


setup(
    name='motorengine-bitfield',
    version='1.0.0',
    url='https://gitlab.com/wmedlar/motorengine-bitfield',
    author='Will Medlar',
    author_email='',
    description='Custom field type for storing and retrieving bit-packed flags as enums.',
    long_description=open('README.md').read(),
    license='GPLv3',
    platforms='any',
    keywords='motorengine bit-packing enum',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database :: Database Engines/Servers',
    ],
    py_modules=['bitfield'],
    install_requires=['motorengine>=0.9,<1'],
    python_requires='>=3.6',
    # we only want to install pytest-runner on invocations of "python setup.py test"
    setup_requires=['pytest-runner'] if 'test' in argv else [],
    tests_require=['pytest'],
)
