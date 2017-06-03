import os
from setuptools import setup


# Hacky fix for docker builds, need to kill off link
if os.environ.get('PYTHON_BUILD_DOCKER', None) == 'true':
    del os.link

setup(
    name='teem-py',
    version='0.1.0',
    author='Jeff Schenck',
    author_email='jmschenck@gmail.com',
    url='https://github.com/jeffschenck/teem-py',
    download_url='https://github.com/jeffschenck/teem-py',
    description='Collaborative editing with OT in Python Edit',
    license='MIT',
    install_requires=[],
    packages=[
        'teem',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License',
    ],
)
