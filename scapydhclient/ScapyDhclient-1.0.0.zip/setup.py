#encoding=utf-8
from distutils.core import setup  
setup(name='ScapyDhclient',  #需要打包的文件
      version='1.0.0',    #版本号
      description='use Scapy Simulated DHCP dhclient',    #描述信息
      author='qdyxmas',   #作者  
      author_email='qdyxmas@gmail.com',    #作者邮箱
      url='https://github.com/qdyxmas/scapy-Protocol-conformance',# 源码链接地址
      keywords='scapy-dhclient dhclient scapy', 
      install_requires=[
        'scapy' #依赖包
      ],
      platform='all',	#适用平台
      py_modules=['ScapyDhclient'],  #模块名
)    