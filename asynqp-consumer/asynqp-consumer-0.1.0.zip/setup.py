from setuptools import setup, find_packages


setup(
    name='asynqp-consumer',
    version='0.1.0',
    author='Timofey Kukushkin',
    author_email='tima@kukushkin.me',
    description='Consumer utility for asyncqp',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'asynqp >= 0.5.1',
    ],
    extras_require={
        'test': [
            'pycodestyle',
            'pylint',
            'pytest==3.0.7',
            'pytest-asyncio==0.5.0',
            'pytest-cov==2.5.1',
            'pytest-mock==1.6.0',
        ],
    },
)
