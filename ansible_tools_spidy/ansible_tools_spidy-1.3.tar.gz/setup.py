from distutils.core import setup
setup(
  name = 'ansible_tools_spidy',
  packages = ['FILE_spidy','Utilities_spidy','constrains_spidy'], # this must be the same as the name above
  version = '1.3',
  description = 'Store ansible inventory & playbooks in mongodb, run ansible by extracting inventory & playbooks from mongo db ; command :- /usr/local/bin/ansible_playbook ; /usr/local/bin/ansible_playbook_load ; /usr/local/bin/ansible_inventory_load',
  author = 'Anish V Tharagar',
  author_email = 'anish.tharagar@gmail.com',
  url = 'https://github.com/anishtharagar/code_repo_public.git', # use the URL to the github repo
  download_url = 'https://github.com/anishtharagar/code_repo_public/packaging/', # I'll explain this in a second
  keywords = ['mongo','ansible', 'playbooks', 'automation'], # arbitrary keywords
  install_requires = [ 'pyaml','pymongo','libmagic', 'termcolor' ],
  classifiers = [],
  data_files=[('/usr/local/bin',['Tools_spidy/ansible_playbook','Tools_spidy/ansible_inventory_load','Tools_spidy/ansible_playbook_load']),
	      ('/etc',['files_repo/mongo_connect.json'])],
  license = 'MIT',
)
