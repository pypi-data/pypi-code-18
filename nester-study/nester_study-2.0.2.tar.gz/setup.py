#从Python发布工具导入“setup”函数
from distutils.core import setup

setup(
	name = 'nester_study',
	version = '2.0.2',
	py_modules = ['nester_study'],#将模块的元数据nester与setup函数的参数关联。
	anthor = 'ching55',
	author_email = 'ching55@qq.com',
	url = 'http://www.evipshop.com',
	description = 'A simple printer of nested lists',
	)
'''
setup(
	#Metadata-Version= 1.0,
	Name= 'nester_study',
	Version='2.0.1',
	Summary='A simple printer of nested lists',
	Home-page='http://www.evipshop.com',
	Author='ching55',
	Author-email='ching55@qq.com',
	License='MIT License',
	Description='A simple printer of nested lists',
	Platform='https://pypi.python.org/pypi'
	)

setup(
    name = 'ListTest',
    version = '0.0.1',
    keywords = ('list', 'test'),
    description = 'just a simple test',
    license = 'MIT License',
    install_requires = ['ListTest>=1.1'],

    author = 'ching55',
    author_email = 'ching55@qq.com',
    
    packages = find_packages(),
    platforms = 'any',
)
'''