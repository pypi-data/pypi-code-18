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
    version='34',
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

DE MEEST KWETSBAREN
###################

Geachte Minister-President,

In 2012 heb ik het Europeese Hof voor de Rechten van de Mens :ref:`aangeschreven <verzoek>` om een klacht tegen Nederland in te dienen.
De :ref:`klacht <greffe>` betrof het afwezig zijn van verpleging in het nieuwe ambulante behandeltijdperk van de GGZ.
De :ref:`uitspraak <uitspraak>` is niet-ontvankelijk. 
Ik heb zowel :ref:`Koningin Beatrix <beuker>` en :ref:`Koning Willem-Alexander <beuker2>` aangeschreven over problemen met de invoering van de :ref:`(F)ACT <fact>` methodiek in Nederland.
Het is niet mogelijk voor de Koningin, noch de Koning om verdere tussenkomst te verlenen. 

Koningin Beatrix vermeld ministeriele verantwoordelijkheid, daarom went ik mij dan ook tot u, verantwoordelijk voor de zorg die aan de meest kwetsbaren in Nederland gegeven word.

| Er is bewijs dat antipsychotica gif zijn, zie hieronder.
| Er is bewijs dat antipsychotica schadelijk zijn voor de hersenen, zie (1).

Zie hier een doodskop met beenderen voor het medicijn clozapine:

.. image:: jpg/bewijsgif3.jpg
    :width: 100%

ZORG
####

Wat de GGZ als zorg levert is geen zorg maar het plegen van misdrijven zoals omschreven in het Wetboek van Strafrecht:

gijzeling
=========

* GGZ patienten zonder schuldig bevinding opsluiten is gijzeling.

282a.1 Hij die opzettelijk iemand wederrechtelijk van de vrijheid berooft of beroofd houdt met het oogmerk een ander te dwingen iets te doen of niet te doen wordt als schuldig aan gijzeling gestraft met gevangenisstraf van ten hoogste vijftien jaren of geldboete van de vijfde categorie.

282a.2 Indien het feit de dood ten gevolge heeft wordt hij gestraft met levenslange gevangenisstraf of tijdelijke van ten hoogste dertig jaren of geldboete van de vijfde categorie.

mishandeling
============

* Antipsychotica blijken gif te zijn.
* Door toediening van antipsychotica krijgt het slachtoffer te maken krijgen met positieve en negatieve symptomen, symptomen van vergiftiging, onthoudingsverschijnselen en ernstige bijwerkingen, zie :ref:`symptomen`.

300.4 Met mishandeling wordt gelijkgesteld opzettelijke benadeling van de gezondheid.

304.3 indien het misdrijf wordt gepleegd door toediening van voor het leven of de gezondheid schadelijke stoffen.

verzwijging
===========

* De arts informeert de patient niet dat het een gif betreft.
* De arts verzwijgt het schadelijk karakter van zijn medicijnen.

174.1 Hij die waren verkoopt, te koop aanbiedt, aflevert of uitdeelt, wetende dat zij voor het leven of de gezondheid schadelijk zijn, en dat schadelijk karakter verzwijgende, wordt gestraft met gevangenisstraf van ten hoogste vijftien jaren of geldboete van de vijfde categorie.

174.2 Indien het feit iemands dood ten gevolge heeft, wordt de schuldige gestraft met levenslange gevangenisstraf of tijdelijke van ten hoogste dertig jaren of geldboete van de vijfde categorie.


tegen het leven gericht
=======================

* Als de medicijnen dodelijke aandoeningen kunnen veroorzaken noem ik het medicijn dodelijk. Dodelijke stof toedienen is een misdrijf tegen het leven gericht.

285.1 Bedreiging met enig misdrijf tegen het leven gericht wordt gestraft met gevangenisstraf van ten hoogste twee jaren of geldboete van de vierde categorie.

287 Hij die opzettelijk een ander van het leven berooft, wordt, als schuldig aan doodslag, gestraft met gevangenisstraf van ten hoogste vijftien jaren of geldboete van de vijfde categorie.

289 Hij die opzettelijk en met voorbedachten rade een ander van het leven berooft, wordt, als schuldig aan moord, gestraft met levenslange gevangenisstraf of tijdelijke van ten hoogste dertig jaren of geldboete van de vijfde categorie.

294.1 Hij die opzettelijk een ander tot zelfdoding aanzet, wordt, indien de zelfdoding volgt, gestraft met een gevangenisstraf van ten hoogste drie jaren of geldboete van de vierde categorie.


DE EISEN
########

U als Minister-President ben verantwoordelijk om zorg te dragen voor de meest kwetsbaren, u dient te zorgen dat deze zorg (de gedwongen zorg) geen plegen van strafbare feiten omvat. 

Ik eis dan ook de volgende maatregelen:

| 1. direct bekend te maken dat deze medicatie gif zijn en ze van de markt af te halen.

| 2. direct een einde te zetten aan de vergiftigingen in de GGZ, gif toedienen is strafbaar.

| 3. direct de politie zelf bloedspiegels laten nemen om daarmee mishandeling bewijzen.

| 4. direct van alle nederlanders de medische dossiers opvragen om toediening van gif te kunnen vaststellen.

| 5. direct de noodzakelijke verpleging die deze slachtoffers van vergiftiging nodig hebben direct te leveren, ook in weekend en avonduren.

De patient heeft recht op zorg/verpleging zonder dat er strafbare feiten gepleegd worden, het slachtoffer heeft recht op vervolging van de gif toedienende arts.


Hoogachtend,


.. raw:: html

    <br>


Bart Thate


.. raw:: html

    <br>

(1) Hersenweefselverlies door Haldol etc. - http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3476840/
(2) De Material Safety Data Sheet toont de classificatie van de soort stof - zie :ref:`hier <bewijsgif>`, :ref:`vervolgen <strafbaar>`.
(3) Europese Chemicals database voor de algemene bekendheid -  https://echa.europa.eu/search-for-chemicals

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
