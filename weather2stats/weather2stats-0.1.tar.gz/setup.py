from distutils.core import setup
setup(
    name='weather2stats',
    packages=['weather2stats'],
    version='0.1',
    description='Convert stats websites to influx data',
    author='Felix Richter',
    license='WTFPL',
    author_email='github@syntax-fehler.de',
    url='https://github.com/makefu/weather2stats',
    install_requires = [
        'requests',
        'pytz',
        'beautifulsoup4',
        'docopt',
        'influxdb'
    ],
    keywords=['api'],
)
