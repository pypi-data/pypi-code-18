#encoding=utf-8
from distutils.core import setup  
setup(name='PyIxChariot',  #需要打包的文件
      version='1.0',    #版本号
      description='Request websites to use different clients',    #描述信息
      author='qdyxmas',   #作者  
      author_email='qdyxmas@gmail.com',    #作者邮箱
      url='https://github.com/qdyxmas/Portal-authentication',keywords='python portal Web Authentication', # 源码链接地址
      install_requires=[	
        'requests','requests_toolbelt' #依赖包
      ],
      platform='linux',	#适用平台
      py_modules=['PyIxChariot.kt','PyIxChariot.km','PyIxChariot.kc','PyIxChariot.all'],  #模块名
)    