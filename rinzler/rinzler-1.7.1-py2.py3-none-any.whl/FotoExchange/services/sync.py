import base64
import os
from datetime import datetime
import hashlib

from config.settings import SOCIAL_API_CONFIG
from config.settings import URL_DRIVE_API
from models.pf_foto import PfFoto
from services.log import Log
from onyxerp.drive_service import DriveService
from services.authenticate import Authenticate

class Sync(object):

    __synced_files = list()
    __error_files = list()
    storage_path = str()
    public_path = str()
    jwt = str()
    log = object
    drive_service = object
    authenticate = object

    def __init__(self):
        if not os.path.exists(SOCIAL_API_CONFIG['storage_path']):
            raise Exception("O path informado em SOCIAL_API_CONFIG não existe ou não permite leitura/escrita.")
        else:
            self.storage_path = SOCIAL_API_CONFIG['storage_path']
            self.public_path = os.path.realpath(SOCIAL_API_CONFIG['storage_path'] + '/../public/')

        self.log = Log()
        self.drive_service = DriveService(URL_DRIVE_API)
        self.authenticate = Authenticate()

    def run(self):
        files = self.get_files_sync()

        if len(files) > 0:

            self.jwt = self.get_jwt()

            for file in files:

                file_name = file.pf_foto_hash

                data = self.get_file_data(file_name)

                if data:
                    envio = self.send_file_drive(file.pf_cod.pf_cod, file.pf_foto_nome, file.pf_foto_mime, data)
                    if envio:
                        print("Arquivo {0} sincronizado com sucesso as {1}".format(file_name, datetime.now()))
                        self.log.register("Arquivo {0} sincronizado com sucesso as {1}".format(file_name, datetime.now()))
                        self.process_synced_file(file)
                    else:
                        print("Erro: {0}".format(envio))

                token_valido = self.authenticate.verifica_jwt(self.jwt)

                if token_valido is not True:
                    self.jwt = token_valido

                continue

            print("Fim da execução do script")
            self.log.register("Fim da execução do script\n")
        else:
            print("Nenhuma a ser migrada no momento. \\o/")
            self.log.register("Nenhuma a ser migrada no momento. \\o/")

    def send_file_drive(self, pf_cod, foto_nome, foto_mime, data):
        sha_obj = hashlib.sha1(data)
        payload = {
            "name": foto_nome,
            "mime-type": foto_mime,
            "sha1": sha_obj.hexdigest(),
            "upload_tipo_cod": "11",
            "data": data.decode('utf-8'),
            "device": self.get_device_data()
        }

        response = self.drive_service.set_jwt(self.jwt).set_payload(payload).upload_files(pf_cod, 9)

        if type(response) is dict:
            self.log.register("Erro: {0}".format(response))
            return False
        else:
            return True

    @staticmethod
    def get_device_data():
        """
        Retorna os dados do device para ser logado na API
        @param self: self
        @return: Resposta decodificada da API em caso de sucesso, False otherwise
        """
        return {
            "id": "7df0723b4c86ab59711ea26c66642c47",
            "log": {
                "lat": -7.9839111,
                "lon": -34.8387671,
                "ip": "127.0.0.0"
            }
        }

    def get_jwt(self):
        return self.authenticate.get_jwt()

    def process_synced_file(self, pf_foto):
        file_absolute = os.path.realpath(self.storage_path + '/' + pf_foto.pf_foto_hash)
        public_file_absolute = os.path.realpath(self.public_path + '/' + pf_foto.pf_foto_hash)

        # Atualiza as tabelas
        self.update_file_success(pf_foto)

        # Remove arquivo do storage
        os.unlink(file_absolute)

        # Remove a copia publica do arquivo
        if os.path.isfile(public_file_absolute):
            os.unlink(public_file_absolute)

        self.log.register("Arquivo {0} processado com sucesso.".format(pf_foto))

        return True

    @staticmethod
    def update_file_success(pf_foto):
        pf_foto.pf_foto_status = 'I'
        pf_foto.save()
        return True

    def get_file_data(self, file_name):
        storage_path = self.storage_path
        file_absolute = os.path.realpath(storage_path + '/' + file_name)
        if not os.path.isfile(file_absolute):
            print("O arquivo {0} não existe ou não pôde ser acessado. Às {1}".format(file_absolute, datetime.now()))
            self.log.register("O arquivo {0} não existe ou não pôde ser acessado. Às {1}".format(file_absolute, datetime.now()))
            return False
        else:
            file = open(file_absolute, 'rb')
            file_data = file.read()
            file.close()
            return base64.b64encode(file_data)

    @staticmethod
    def get_files_sync():
        max = 100 if 'max_rows' not in SOCIAL_API_CONFIG else SOCIAL_API_CONFIG['max_rows']
        return PfFoto.objects.filter(pf_foto_status='A')[:max]

    def append_synced_file(self, file):
        self.__synced_files.append(file)
        return self

    def append_error_file(self, file):
        self.__error_files.append(file)
        return self
