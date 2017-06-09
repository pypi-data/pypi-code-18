from distutils.core import setup
setup(
    name='wxyAlice',
    packages=['wxyAlice'],
    version='0.0.26',
    description='classes used in micro service on falcon',
    author='wangxiaoyu',
    author_email='wangxiaoyu.wangxiaoyu@gmail.com',
    license='MIT',
    install_requires=[
        'gevent',
        'falcon',
        'pymongo',
        'requests',
        'PyYAML',
        'PyJWT',
        'jsonschema'
    ],
    url='https://github.com/netsmallfish1977/wxyAlice',
    download_url='https://github.com/netsmallfish1977/wxyAlice/tarball/0.0.26',
    keywords=['wxy', 'Alice', 'falcon', 'restapi'],
    classifiers=[],
)
