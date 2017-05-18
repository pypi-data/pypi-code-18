#encoding=utf-8
from distutils.core import setup  
setup(name='ScapyDhcpServer',  #需要打包的文件
      version='1.0.2',    #版本号
      description='use Scapy Simulated DHCP server',    #描述信息
      author='qdyxmas',   #作者  
      author_email='qdyxmas@gmail.com',    #作者邮箱
      url='https://github.com/qdyxmas/scapy-Protocol-conformance',# 源码链接地址
      keywords='scapy dhcpd dhcpserver dhcp-server', 
      install_requires=[	
        'IPy','scapy' #依赖包
      ],
      platform='all',	#适用平台
      py_modules=['ScapyDhcpServer'],  #模块名
)    