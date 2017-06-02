from setuptools import setup, find_packages

version = '1.2'

try:
    import sqlite3
except ImportError:
    requires = ['pysqlite']
else:
    requires = []

setup(
    name='pyzipcode3',
    version='1.2',
    url='https://www.github.com/dvf/pyzipcode3',
    description="Search by ZIP Code, City and Geo data",
    keywords='zip code distance geo',
    author='Daniel van Flymen',
    author_email='vanflymen@gmail.com',
    license='GPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_data={
        'pyzipcode': ['zipcodes.db', ]
    },
    include_package_data=True,
    download_url='https://www.github.com/dvf/pyzipcode3/archive/1.2.tar.gz',
    zip_safe=False,
    install_requires=requires,
    classifiers=[],
)
