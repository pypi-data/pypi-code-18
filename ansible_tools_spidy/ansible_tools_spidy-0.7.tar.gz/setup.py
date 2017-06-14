from distutils.core import setup
setup(
  name = 'ansible_tools_spidy',
  packages = ['FILE_spidy','Utilities_spidy','constrains_spidy','Tools_spidy'], # this must be the same as the name above
  version = '0.7',
  description = 'ansible_tools_spidy allows you to store and retreive playbooks in mongodb using passwordless auth, Security Wrappers in the next Release',
  author = 'Anish V Tharagar',
  author_email = 'anish.tharagar@gmail.com',
  url = 'https://github.com/anishtharagar/code_repo_public.git', # use the URL to the github repo
  download_url = 'https://github.com/anishtharagar/code_repo_public/packaging/', # I'll explain this in a second
  keywords = ['ansible', 'playbooks', 'automation'], # arbitrary keywords
  install_requires = [ 'pyaml','pymongo','libmagic', 'termcolor' ],
  classifiers = [],
  data_files=[('/usr/local/bin',['Tools_spidy/ansible_playbook','Tools_spidy/yaml_to_mongo'])],
  license = 'MIT',
)
