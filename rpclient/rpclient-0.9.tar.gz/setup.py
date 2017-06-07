from setuptools import setup

setup(name='rpclient',
      version='0.9',
      description='The RabbitMQ Server\'s RPC Client',
      keywords='rpc rpclient rpcclient rabbitmq pika',
      url='http://infinite.mn/',
      author='Infinite Solutions LLC',
      author_email='ganzorig@infinite.mn',
      license='GNU',
      packages=['rpclient'],
      install_requires=[
          'pika',
      ],
      data_files=[('/etc', ['cfg/rpclient.ini'])],
      zip_safe=False)
