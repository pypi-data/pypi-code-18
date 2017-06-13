import setuptools
from setuptools import setup, find_packages
from setuptools.command.install import install
import os
from os.path import isfile, isdir, join, dirname
import pollux
version = pollux.__version__
try:
    import objc
except ImportError:
    pass

# extras
env_deps = ['tabview>=1.4.0',
            'matplotlib>=1.4.3',
            'blessings>=1.6',
            'tables']
            
app_deps = ["Flask>=0.12.1",
            "flask-Bootstrap>=3.3.7.1",
            "flask-WTF",
            "rumps",
            "pyobjc"]

mac_app_deps = ["Flask>=0.12.1",
                "flask-Bootstrap>=3.3.7.1",
                "flask-WTF"]

dev_deps = list(set(env_deps + app_deps + mac_app_deps + ['cx_Freeze']))
all_deps = list(set(env_deps + app_deps + mac_app_deps + ['cx_Freeze']))

class CustomInstallCommand(install):
    """
    Customized setuptools install command, which installs
    some NLTK data automatically
    """
    def run(self):
        from setuptools.command.install import install
        install.run(self)
        # since nltk may have just been installed
        # we need to update our PYTHONPATH
        import site
        try:
            reload(site)
        except NameError:
            pass
        # Now we can import nltk
        import nltk
        # install these three resources and add them to path
        install_d = {'tokenizers': 'punkt',
                     'corpora': 'wordnet',
                     'taggers': 'averaged_perceptron_tagger'}
        
        path_to_nltk_f = nltk.__file__
        nltkpath = dirname(path_to_nltk_f)
        for path, name in install_d.items():
            pat = join(nltkpath, path)
            if not isfile(join(pat, '%s.zip' % name)) \
                and not isdir(join(pat, name)):
                nltk.download(name, download_dir=nltkpath)

        nltk.data.path.append(nltkpath)

        # do not require hdf5
        import pip
        try:
            import tables
            print("PYTABLES ALREADY INSTALLED")
        except ImportError:
            try:
                pip.main(['install', 'tables'])
                print("INSTALLED PYTABLES SUCCESSFULLY")
            except:
                print("FAILED TO INSTALL PYTABLES: HDF5 NOT FOUND")
                pass

setup(name='pollux',
      version=version,
      description='Sophisticated corpus linguistics',
      url='http://github.com/interrogator/pollux',
      author='Daniel McDonald',
      include_package_data=True,
      zip_safe=False,
      packages=['corpkit', 'corpkit.download', 'pollux'],
      scripts=['corpkit/new_project', 'pollux/scripts/pollux-parse',
               'pollux/scripts/pollux-install-corenlp', 'pollux/scripts/pollux',
               'pollux/scripts/pollux-build', 'pollux/scripts/pollux-add', 'pollux/scripts/pollux-quickstart',
               'corpkit/corpkit', 'corpkit/corpkit.1'],
      package_dir={'corpkit': 'corpkit', 'pollux': 'pollux'},
      package_data={'corpkit': ['*.jar', 'corpkit/*.jar', '*.sh', 'corpkit/*.sh', 
                                '*.ipynb', 'corpkit/*.ipynb', '*.p', 'dictionaries/*.p',
                                '*.py', 'dictionaries/*.py', '*.properties', 'langprops/*.properties']},
      author_email='mcddjx@gmail.com',
      license='MIT',
      cmdclass={'install': CustomInstallCommand},
      keywords=['corpus', 'linguistics', 'nlp'],
      install_requires=[#"matplotlib>=1.4.3",
                        "nltk>=3.0.0",
                        "joblib",
                        "pandas>=0.19.2",
                        "requests",
                        "tabview>=1.4.0",
                        "chardet",
                        "blessings>=1.6",
                        "tqdm>=4.11.2",
                        "numpy>=1.12.0",
                        "traitlets>=4.1.0"],

      extras_require={'app': app_deps,
                      'mac_app': mac_app_deps,
                      'all': all_deps,
                      'env': env_deps,
                      'dev': dev_deps},

      dependency_links=['git+https://github.com/interrogator/tabview.git#egg=tabview-1.4.0',
                        'git+https://github.com/interrogator/tqdm.git#egg=tqdm-4.11.2',
                        'git+https://github.com/interrogator/rumps.git#egg=rumps-0.2.2'])
