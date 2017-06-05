from setuptools import find_packages, setup
from django_hstore import __version__

setup(
    name='django_admin_hstore',
    version=__version__,
    url='https://bitbucket.org/deusesprl/django_hstore',
    author='Maxime Deuse',
    author_email='m.deuse@deuse.be',
    description='An admin widget for the Hstore, this widget usefulness is to have dynamic fields for a given model.',
    license='MIT',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=1.11.0',
    ],
)
