from setuptools import setup, find_packages

setup(
    name='wechatSpider',
    version=0.1,
    keyword=('wechat', 'spider', 'sogou', 'subscription'),
    description='WeChat subscription search by lshxiao',
    license='http://web.pxuexiao.com',

    url='http://py.pxuexiao.com/wechat_spider',
    author='lshxiao',
    author_email='lshxiao@163.com',

    packages=find_packages(),
    include_package_data=True,
    platforms='python 2.7',
    install_requires=['requests', 'lxml']
)
