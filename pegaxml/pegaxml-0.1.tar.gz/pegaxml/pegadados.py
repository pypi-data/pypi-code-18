import requests
import xmltodict


def lista_titulos():
    """Retorna os títulos dos CDs do xml

    :return: list
    """

    xml = requests.get('https://www.w3schools.com/xml/cd_catalog.xml')
    lista = xmltodict.parse(xml.text)
    titulos = []
    for titulo in lista['CATALOG']['CD']:
        titulos.append(titulo['TITLE'])

    return titulos


if __name__ == '__main__':
    print('Total de ', len(lista_titulos()), 'títulos', lista_titulos())

    titulos = lista_titulos()

    for titulo in titulos:
        print(titulo)
