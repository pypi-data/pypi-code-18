#encoding=utf-8
from distutils.core import setup  
setup(name='PortalAuth',  
      version='1.0.2',    
      description='Request websites to use different clients',    
      author='qdyxmas',    
      author_email='qdyxmas@gmail.com',    
      url='https://github.com/qdyxmas/Portal-authentication',keywords='python portal Web Authentication', # 关键字
      install_requires=[
        'requests','requests_toolbelt'
      ],
      platform='linux',
      py_modules=['PortalAuth'],  
)    