from distutils.core import setup
setup(
    name='wxyAlice',
    packages=['wxyAlice'],
    version='0.0.19',
    description='micro service on falcon',
    author='wangxiaoyu',
    author_email='wangxiaoyu.wangxiaoyu@gmail.com',
    license='MIT',
    install_requires=[
        'gevent',
        'falcon',
        'requests'
    ],
    url='https://github.com/netsmallfish1977/wxyAlice',
    download_url='https://github.com/netsmallfish1977/wxyAlice/tarball/0.0.19',
    keywords=['wxy', 'Alice', 'falcon', 'restapi'],
    classifiers=[],
)
