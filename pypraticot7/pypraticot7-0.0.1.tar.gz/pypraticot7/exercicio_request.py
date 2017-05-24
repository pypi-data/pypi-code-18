#!/usr/bin/python3

import requests
import urllib.request as url
import re
from PIL import Image

class Avatar:
    """
        Classe Criada para busca da Url do Usuario
        
        python:
        >>> r = Avatar("renzon")
        >>> print(r.avatar)
        https://avatars0.githubusercontent.com/u/3457115?v=3
    
        @:param user : tipo str, com o usuario para busca de url
        @:return avatar: url com a foto do usuario
    
    """



    def __init__(self,user):
        self.user = user
        self.avatar = self.getAvatar()
        self.end = self.endereco()
        url.urlretrieve(self.end,"imagem.jpg")
        self.image = Image.open("imagem.jpg")
        self.image.show()



    def getAvatar(self):

        try:
            response  = requests.get(f"https://api.github.com/users/{self.user}")
            if response.status_code != 200:
                raise Exception("Erro: %s" % response.status_code)

            return response.json().get("avatar_url")

        except Exception as e:
            return "Erro na busca por Usuario: %s" % e

    def endereco(self):
        numero = re.findall(r'(\d+)(?:\?v\=3)',self.avatar)[0]
        endereco = self.avatar+"/"+numero+".jpg"

        return endereco



if __name__ == "__main__":
    jp = Avatar("joaopauloramos")
    print(jp.avatar)