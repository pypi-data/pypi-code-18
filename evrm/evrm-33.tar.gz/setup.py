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
    version='33',
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

In 2012 heb ik het Europeese Hof voor de Rechten van de Mens :ref:`aangeschreven <verzoek>` om een klacht tegen Nederland in te dienen.
De klacht betrof het afwezig zijn van verpleging in het nieuwe ambulante behandeltijdperk van de GGZ.
De uitspraak is niet-ontvankelijk. 
Ik heb zowel Koningin Beatrix en Koning Willem-Alexander aangeschreven over problemen met de invoering van de (F)ACT methodiek in Nederland.
Het is niet mogelijk voor de Koningin, noch de Koning om verdere tussenkomst te verlenen. 

Koningin Beatrix vermeld ministeriele verantwoordelijkheid, daarom went ik mij dan ook tot u, verantwoordelijk voor de zorg die aan de meest kwetsbaren in Nederland gegeven word.

Er is bewijs dat antipsychotica gif zijn en schadelijk voor de hersenen (1).
Toedienen van gif in plaats van een medicijn maakt dat men mishandeling pleegt i.p.v behandeling, iets waarvoor direct optreden vereist om daar een einde aan te maken. 
Om de overheid het Wetboek van Strafrecht ook bescherming te laten bieden aan GGZ patienten dient deze ook voor artsen te worden gehandhaaft.
Bescherming voor patienten voor wie het niet mogelijk is om door middel van aangifte bij de politie een vergiftigende arts te doen laten stoppen.
De politie zou zelf bloedspiegelwaardes moeten meten om mishandeling te bewijzen en daarmee direct een halt toe te roepen aan de mishandeling van de patient die anders voor de rest van zijn leven voortduurt.

Minister-President, u dient op te treden voor de meest kwetsbare in Nederland, zij die geen aangifte kunnen doen, door het leveren van zorg die strafbare feiten omvat dan ook daadwerkelijk te gaan vervolgen.

Ik verwacht dat u uw verantwoordelijkheid in deze dan ook voortvarend ter hand neemt.

Hoogachtend,


Bart Thate

(1) Hersenweefselverlies - http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3476840/
(2) Bij de behandeling met antipsychotica krijgt een patient door toediening van antipsychotica te maken krijgen met positieve en negatieve symptomen, symptomen van vergiftiging, onthoudingsverschijnselen en ernstige bijwerkingen, zie :ref:`symptomen`.

| email is bthate@dds.nl or thatebart@gmail.com 
| botfather on #dunkbots irc.freenode.net 



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
