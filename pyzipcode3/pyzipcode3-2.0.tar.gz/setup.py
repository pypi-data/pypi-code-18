from setuptools import setup, find_packages

version = '2.0'

try:
    import sqlite3
except ImportError:
    requires = ['pysqlite']
else:
    requires = []

setup(
    name='pyzipcode3',
    version=version,
    url='https://www.github.com/dvf/pyzipcode3',
    description="Search by ZIP Code, Place and Geo data",
    keywords='zip code distance geo',
    author='Daniel van Flymen',
    author_email='vanflymen@gmail.com',
    license='GPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_data={
        'pyzipcode': ['zipcodes.db', ]
    },
    include_package_data=True,
    download_url='https://www.github.com/dvf/pyzipcode3/archive/2.0.tar.gz',
    zip_safe=False,
    install_requires=requires,
    classifiers=[],
)
