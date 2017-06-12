from setuptools import setup

setup(name='jinja2_utilities',
      author='Emmanuel Mayssat',
      author_email='emmanuel.mayssat@aya.yale.edu',
      description='Jinja2 utilities',
      install_requires=[
          'jinja2',
      ],
      license='MIT',
      packages=[
          'jinja2_utilities',
      ],
      scripts=[
          'bin/jjrender',
      ],
      url='http://github.com/emayssat/jjrender',
      version='0.1',
      zip_safe=False,
      )
