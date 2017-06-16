from setuptools import setup, find_packages

setup(
    name='chestymetrics',
    version='0.0.3',
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
