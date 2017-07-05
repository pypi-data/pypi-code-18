from setuptools import setup

setup(
    name='ElasticDeploy',
    version='1.1.0',
    description='Deploy multiple applications/services/websites on a single Elastic Beanstalk environment.',
    keywords='aws elastic beanstalk multi deployment',
    url='https://github.com/tscheiki/ElasticDeploy',
    author='Markus Tscheik',
    author_email='markus.tscheik@gmail.com',
    license='MIT',
    packages=['elasticdeploy'],
    entry_points={
        'console_scripts': ['elasticdeploy=elasticdeploy.main:main'],
    },
    include_package_data=True,
    zip_safe=True
)
