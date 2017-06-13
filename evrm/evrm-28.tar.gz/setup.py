#!/usr/bin/env python3
#
#

import os
import sys
import os.path

def j(*args):
    if not args: return
    todo = list(map(str, filter(None, args)))
    return os.path.join(*todo)

if sys.version_info.major < 3:
    print("you need to run evrm with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

target = "evrm"
upload = []

def uploadfiles(dir):
    upl = []
    if not os.path.isdir(dir):
        print("%s does not exist" % dir)
        os._exit(1)
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if not os.path.isdir(d):
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl

def uploadlist(dir):
    upl = []

    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)

    return upl

setup(
    name='evrm',
    version='28',
    url='https://bitbucket.org/thatebart/evrm',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="En dat schadelijk karakter verzwijgende !!".upper(),
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["botlib"],
    scripts=["bin/evrm"],
    packages=['evrm', ],
    long_description='''

WET
###

174.1 Hij die waren verkoopt, te koop aanbiedt, aflevert of uitdeelt, wetende dat zij voor het leven of de gezondheid schadelijk zijn, en dat schadelijk karakter verzwijgende, wordt gestraft met gevangenisstraf van ten hoogste vijftien jaren of geldboete van de vijfde categorie.

174.2 Indien het feit iemands dood ten gevolge heeft, wordt de schuldige gestraft met levenslange gevangenisstraf of tijdelijke van ten hoogste dertig jaren of geldboete van de vijfde categorie.

285.1 Bedreiging met enig misdrijf tegen het leven gericht wordt gestraft met gevangenisstraf van ten hoogste twee jaren of geldboete van de vierde categorie.

287   Hij die opzettelijk een ander van het leven berooft, wordt, als schuldig aan doodslag, gestraft met gevangenisstraf van ten hoogste vijftien jaren of geldboete van de vijfde categorie.

289   Hij die opzettelijk en met voorbedachten rade een ander van het leven berooft, wordt, als schuldig aan moord, gestraft met levenslange gevangenisstraf of tijdelijke van ten hoogste dertig jaren of geldboete van de vijfde categorie.

294.1 Hij die opzettelijk een ander tot zelfdoding aanzet, wordt, indien de zelfdoding volgt, gestraft met een gevangenisstraf van ten hoogste drie jaren of geldboete van de vierde categorie.

300.4 Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid.

304.3 indien het misdrijf wordt gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen.

EMAIL
#####

| Bartholomeus Henricus Julius (Bart) Thate`
| botfather on #dunkbots irc.freenode.net 
| email is bthate@dds.nl, thatebart@gmail.com 

''',
   data_files=[("docs", ["docs/conf.py","docs/index.rst"]),
               (j('docs', 'jpg'), uploadlist(j("docs","jpg"))),
               (j('docs', 'txt'), uploadlist(j("docs", "txt"))),
               (j('docs', '_templates'), uploadlist(j("docs", "_templates")))
              ],
   package_data={'': ["*.crt"],
                 },
   classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
