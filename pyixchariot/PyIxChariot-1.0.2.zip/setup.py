#encoding=utf-8
from distutils.core import setup  
setup(name='PyIxChariot',  #需要打包的文件
      version='1.0.2',    #版本号
      description='add class ks in order to configure serial',    #描述信息
      author='qdyxmas',   #作者  
      author_email='qdyxmas@gmail.com',    #作者邮箱
      url='https://github.com/qdyxmas/Portal-authentication',keywords='PyIxChariot Throughput', # 源码链接地址
      platform='Windows7/window8/window10',	#适用平台
      py_modules=['PyIxChariot.kt','PyIxChariot.km','PyIxChariot.kc','PyIxChariot.all'],  #模块名
)    