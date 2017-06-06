"""
Created on Feb 13, 2017

@author: root
"""
import sys
from datetime import datetime

from onyxerp.auth_service import AuthService
from onyxerp.login_service import LoginService
from onyxerp.jwt_service import JwtService

from config.settings import URL_AUTH_API
from config.settings import URL_ACCOUNT_API
from config.settings import URL_JWT_API

from services.log import Log

class Authenticate(object):
    apiKey = "NTdjOTc0ZjM3YzRmOA=="
    user = "teste@braconsultoria.com.br"
    passwd = "betabeta"
    inicio = datetime.now()
    jwt = str()
    log = Log()

    def get_jwt(self):
        auth_jwt = self.get_jwt_auth()
        jwt_login = self.get_jwt_login(auth_jwt)
        return jwt_login

    def get_jwt_auth(self):
        service = AuthService(URL_AUTH_API)
        response = service.set_payload({"apikey": self.apiKey}).auth()

        if type(response) is str:
            print("App Authenticated.")
            return response
        else:
            print("FATAL ERROR: Nao possivel obter o token da app. resposta da API " + response.getContent())
            sys.exit(1)

    def get_jwt_login(self, auth_jwt):
        service = LoginService(URL_ACCOUNT_API)
        payload = {'login': self.user, 'password': self.passwd}
        response = service.set_jwt(auth_jwt).set_payload(payload).login()

        if type(response) is str:
            print("User Authenticated.")
            return response
        else:
            print("FATAL ERROR: Nao foi possivel obter o token de usuario. resposta da API " + response.getContent())
            sys.exit(2)

    def verifica_jwt(self, jwt):
        """
        Verifica se o JWT ainda está valido.
        @param self: self
        :return: str
        :param jwt:
        """
        self.jwt = jwt
        now = datetime.now()
        diff = now - self.inicio

        if diff.seconds >= 28800:
            return self.renova_jwt()
        else:
            return True

    def renova_jwt(self):
        """
        Solicita a renovação do token à JwtApi, quando necessário
        @param self: self
        @return: bool True
        """

        print("Solicitando novo JWT as {0}...".format(str(datetime.now())))

        service = JwtService(URL_JWT_API)
        service.set_jwt(self.jwt)

        response = service.renew()

        if type(response) is str:
            print("JWT renovado...")
            self.log.register("JWT renovado as {0}.".format(str(datetime.now())))
            self.inicio = datetime.now()
            self.jwt = response
            return response
        else:
            print("Falha na renovação do JWT!")
            self.log.register("Falha ao renovar JWT: {0}.".format(str(response)))
            sys.exit(4)
