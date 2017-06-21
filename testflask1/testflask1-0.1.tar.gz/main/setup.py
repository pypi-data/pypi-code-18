from setuptools import setup

setup(name='knn',
      version='0.1',
      description='knn Model',
      url='https://github.com/pypa/knn',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['main'],
      install_requires=[
          'turicreate','Flask'
      ],
      dependency_links=['https://pypi.apple.com/simple'],
      zip_safe=False)