import requests
import xmltodict


def lista_titulos_cds():
    url = 'https://www.w3schools.com/xml/cd_catalog.xml'

    resposta = requests.get(url)
    dicionario = xmltodict.parse(resposta.content)
    catalogo = dicionario['CATALOG']['CD']

    lista_titulos_cds = [cd['TITLE'] for cd in catalogo]

    return lista_titulos_cds


if __name__ == '__main__':
    print(lista_titulos_cds())
