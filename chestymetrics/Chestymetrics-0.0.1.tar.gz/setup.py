from setuptools import setup, find_packages

setup(
    name='Chestymetrics',
    version='0.0.1',
    packages=find_packages(),
    url='http://www.google.com',
    license='GPLv3',
    author='max',
    author_email='max@max.com',
    description='foo',
    requires=[
        'pika',
        'click',
        'psutil',
        'cassandra_driver',
        'riemann_client'
    ],
    entry_points=
    '''
    [console_scripts]
    chestymetrics=chestymetrics.__init__:cli
    '''
)
