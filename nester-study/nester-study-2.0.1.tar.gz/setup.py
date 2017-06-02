#从Python发布工具导入“setup”函数
from distutils.core import setup

setup(
	name = 'nester-study',
	version = '2.0.1',
	py_modules = ['nester-study'],#将模块的元数据nester与setup函数的参数关联。
	anthor = 'ching55',
	author_email = 'ching55@qq.com',
	url = 'http://www.evipshop.com',
	description = 'A simple printer of nested lists',
	)