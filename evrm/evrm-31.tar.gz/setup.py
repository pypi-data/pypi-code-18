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
    version='31',
    url='https://bitbucket.org/thatebart/evrm',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Gif toedienende artsen de cel in !!".upper(),
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["botlib"],
    scripts=["bin/evrm"],
    packages=['evrm', ],
    long_description='''

Geachte Minister-President,

In 2012 heb ik het Europeese Hof voor de Rechten van de Mens aangeschreven om een klacht tegen Nederland in te dienen.
De klacht betrof het afwezig zijn van verpleging in het nieuwe ambulante behandeltijdperk van de GGZ.
De uitspraak is niet-ontvankelijk. 

Ik heb zowel Koningin Beatrix en Koning Willem-Alexander aangeschreven over problemen met de invoering van de (F)ACT methodiek in Nederland.
Het is niet mogelijk voor de Koningin, noch de Koning om verdere tussenkomst te verlenen. 
Koningin Beatrix ministeriele verantwoordelijkheid, daarom went ik mij dan ook tot u.

Er is bewijs dat de medicijnen die in de (F)ACT methodiek gebruikt worden gif zijn.

Het OM laat na om de gif toedieningen in de GGZ die vandaag de dag worden gedaan zelfstandig te vervolgen. Dit nalaten om gif toedienende artsen te vervolgen is de reden dat er in Nederland nu 300 duizend schizofrenen met gif mishandelt kunnen worden.
Dat men gif toedient en niet een medicijn dat geen schade kan maakt dat men niet zorg verleent maar het Wetboek van Strafrecht overtreed door met die gif toedieningen mishandeling te plegen.
Om de overheid het Wetboek van Strafrecht ook bescherming te laten bieden aan GGZ patienten dient deze ook voor artsen te worden gehandhaaft en vooral wat het toedienen van voor het leven of de gezondheid schadelijke stoffen betreft.

U, als vervanger van de Koning, bent verantwoordelijk voor de zorg die aan de meest kwetsbaren in de samenleving gegeven word.
Het is uw taak om ook het Wetboek van Strafrecht bescherming te laten bieden aan GGZ patienten en dus ook te zorgen dat het OM wel gaat vervolgen voor mishandeling gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen.

Ik verzoek u om de opsporing en vervolging van gif toedienende artsen voor de patient te doen, omdat aangifte doen voor hen onmogelijk is.

Hoogachtend,

Bart Thate

| email is bthate@dds.nl or thatebart@gmail.com 
| botfather on #dunkbots irc.freenode.net - :ref:`teksten <teksten>` 



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
