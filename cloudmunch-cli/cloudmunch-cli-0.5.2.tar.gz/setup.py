from setuptools import setup, find_packages

setup(
    name='cloudmunch-cli',
    version='0.5.2',
    author='Cloudmunch Inc.',
    author_email='info@cloudmunch.com',
    description='CloudMunch CLI is a tool for working with CloudMunch Platform',
    packages= ['cloudmunch', 'cloudmunch.commands', 
               'cloudmunch.commands.configuration',
               'cloudmunch.commands.applications'
              ],# + find_packages(include=['cloudmunch.commands.*']), #TODO: exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Intended Audience :: System Administrators',
      'Programming Language :: Python',
    ],
    include_package_data=True,
    install_requires=[
      'click>=6',
      'requests>=2.9',
      'configobj>=5',
      'pyyaml>=3',
      'jsonschema',
      'enum34',
      'jsonpath-rw>=1.4',
      'ndg-httpsclient>=0.3.2',
      'urllib3>=1.9'
    ],
    entry_points='''
        [console_scripts]
        cloudmunch=cloudmunch.cli:cli
    '''    
)
