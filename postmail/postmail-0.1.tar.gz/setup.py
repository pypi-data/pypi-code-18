from setuptools import setup


setup(name='postmail',
      description='Quickly send an email through a POST request',
      version='0.1',
      py_modules=['postmail'],
      install_requires=open('requirements.txt').readlines(),
      author='Mark Steve Samson',
      author_email='hello@marksteve.com',
      license='MIT')
