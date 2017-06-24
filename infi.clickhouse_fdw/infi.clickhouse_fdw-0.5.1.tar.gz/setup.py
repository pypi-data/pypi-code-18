
SETUP_INFO = dict(
    name = 'infi.clickhouse_fdw',
    version = '0.5.1',
    author = 'Itai Shirav',
    author_email = 'itais@infinidat.com',

    url = 'https://github.com/Infinidat/infi.clickhouse_fdw',
    license = 'BSD',
    description = """A PostgreSQL foreign data wrapper for ClickHouse""",
    long_description = """A PostgreSQL foreign data wrapper for ClickHouse""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'click',
'colorama',
'infi.clickhouse_orm',
'pygments',
'setuptools'
],
    namespace_packages = ['infi'],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [
'generate_clickhouse_fdw = infi.clickhouse_fdw.generate:run'
],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

