import sys
import unicodedata
import re

def lista_caracteres(numero):
    lista = {}
    for i in range(0,numero):
        try:
            lista[chr(i)] = unicodedata.name(chr(i))
        except Exception:
            continue
    return lista


def buscar(*palavras_chave):

    """ Busca por caracteres que contenham a palavra chave em seu nome.
        Ex:

        >>> from exercicios.buscador import buscar
        >>> for caracter, nome in sorted(buscar('BLACK', 'suit')):
        ...     print(caracter, nome)
        ...
        ♠ BLACK SPADE SUIT
        ♣ BLACK CLUB SUIT
        ♥ BLACK HEART SUIT
        ♦ BLACK DIAMOND SUIT
        >>> for caracter, nome in sorted(buscar('suit')):
        ...     print(caracter, nome)
        ...
        ♠ BLACK SPADE SUIT
        ♡ WHITE HEART SUIT
        ♢ WHITE DIAMOND SUIT
        ♣ BLACK CLUB SUIT
        ♤ WHITE SPADE SUIT
        ♥ BLACK HEART SUIT
        ♦ BLACK DIAMOND SUIT
        ♧ WHITE CLUB SUIT
        🕴 MAN IN BUSINESS SUIT LEVITATING
        >>> dict(buscar('BlAcK', 'suit', 'ClUb'))
        {'♣': 'BLACK CLUB SUIT'}
        >>> for caracter, nome in sorted(buscar('chess', 'king')):
        ...     print(caracter, nome)
        ...
        ♔ WHITE CHESS KING
        ♚ BLACK CHESS KING

        :param palavras_chave: tupla de strings
        :return: generator onde cada elemento é uma tupla. O primeiro elemento da 
        tupla é o caracter e o segundo é seu nome. Assim ele pode ser utilizado no
        construtor de um dicionário
        """
    palavras_chave_upper = [p.upper() for p in palavras_chave]

    lista = lista_caracteres(sys.maxunicode)
    lista_menor = lista
    
    for p in palavras_chave_upper:
        lista_menor = {k: v for k, v in lista_menor.items() if re.findall(r'\b%s\b'%p,v)}

    for k, v in lista_menor.items():
        yield(k,v)

