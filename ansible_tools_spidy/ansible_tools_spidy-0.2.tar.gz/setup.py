from distutils.core import setup
setup(
  name = 'ansible_tools_spidy',
  packages = ['FILE_spidy','Utilities_spidy','constrains_spidy'], # this must be the same as the name above
  version = '0.2',
  description = 'ansible_tools_spidy allows you to store and retreive playbooks in mongodb - passwordless auth, Security Wrappers in the next Release',
  author = 'Anish V Tharagar',
  author_email = 'anish.tharagar@gmail.com',
  url = 'https://github.com/anishtharagar/code_repo_public.git', # use the URL to the github repo
  download_url = 'https://github.com/anishtharagar/code_repo_public/packaging/', # I'll explain this in a second
  keywords = ['ansible', 'playbooks', 'automation'], # arbitrary keywords
  install_requires = [ 'pyaml','subprocess','os','sys','json','pymongo','libmagic', 'termcolor' ],
  classifiers = [],
  data_files=[('/usr/local/bin',['./Tools_spidy/ansible_playbook.py','./Tools_spidy/yaml_to_mongo.py'])],
  license = 'MIT',
)
