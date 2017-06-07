from distutils.core import setup
setup(
    name='wxyEllen',
    packages=['wxyEllen'],
    version='0.0.2',
    description='some database',
    author='wangxiaoyu',
    author_email='wangxiaoyu.wangxiaoyu@@gmail.com',
    license='MIT',
    install_requires=[
        'pymongo',
        'py2neo',
        'redis-py'
    ],
    url='https://github.com/netsmallfish1977/wxyEllen',
    download_url='https://github.com/netsmallfish1977/wxyEllen/tarball/0.0.2',
    keywords=['wxy', 'Ellen', 'database', 'redis', 'mongo', 'neo4j'],
    classifiers=[],
)
