from setuptools import setup

setup(name='yaml_utilities',
      author='Emmanuel Mayssat',
      author_email='emmanuel.mayssat@aya.yale.edu',
      description='YAML utilities',
      install_requires=[
          'pyyaml',
      ],
      license='MIT',
      packages=[
          'yaml_utilities',
      ],
      scripts=[
          'bin/yaml_extract',
          'bin/yaml_get',
          'bin/yaml_merge',
          'bin/yaml_prune',
          'bin/yaml_put',
          'bin/yaml_rename',
          'bin/yaml_transform',
          'bin/yaml_validate',
          'bin/yaml_walk',
      ],
      url='http://github.com/emayssat/yaml_utilities',
      version='0.1',
      zip_safe=False,
      )
