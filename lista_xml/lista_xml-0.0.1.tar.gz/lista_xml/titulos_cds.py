#!/usr/bin/python3


import requests
from xmltodict import parse as pr


class XMLCD:

    """
        Classe desenvolvida para o Execicio do Pypratico
        python:
        >>> print(XMLCD("https://www.w3schools.com/js/cd_catalog.xml"))
        ---TITULOS DO CATALOGO---
        Empire Burlesque
        Hide your heart
        Greatest Hits
        Still got the blues
        Eros
        One night only
        Sylvias Mother
        Maggie May
        Romanza
        When a man loves a woman
        Black angel
        1999 Grammy Nominees
        For the good times
        Big Willie style
        Tupelo Honey
        Soulsville
        The very best of
        Stop
        Bridge of Spies
        Private Dancer
        Midt om natten
        Pavarotti Gala Concert
        The dock of the bay
        Picture book
        Red
        Unchain my heart 
    
    """

    def __init__(self, url):

        self.url = url
        self.titulos = []
        self.listar_cds()

    def listar_cds(self):

        response = requests.get(self.url)
        dicionario = pr(response.text)
        for title in dicionario['CATALOG']['CD']:
            self.titulos.append(title['TITLE'])

    def __str__(self):

        print('---TITULOS DO CATALOGO---')
        return '\n'.join([x for x in self.titulos])
