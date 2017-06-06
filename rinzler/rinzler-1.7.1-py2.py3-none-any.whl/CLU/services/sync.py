import os
from datetime import datetime

from config.settings import DRIVE_API_CONFIG
from models.upload_sync import UploadSync
from .s3 import S3


class Sync(object):
    s3 = S3()
    bucket = None
    storage_path = None
    public_path = None
    __synced_files = list()
    __error_files = list()

    def __init__(self):
        if not os.path.exists(DRIVE_API_CONFIG['storage_path']):
            raise Exception("O path informado em DRIVE_API_CONFIG nao existe ou nao permite leitura/escrita.")
        else:
            self.storage_path = DRIVE_API_CONFIG['storage_path']
            self.public_path = os.path.realpath(DRIVE_API_CONFIG['storage_path'] + '/../public/')

        # Seta o bucket que nos usaremos
        self.s3.set_bucket(DRIVE_API_CONFIG['bucket_env'])

    def run(self):
        files = self.get_files_sync()

        if not self.lock_files_in_progress(files):
            raise Exception("Nao foi possivel travar os registros a serem sincronizados.")

        if len(files) > 0:
            for file in files:
                file_name = file.upload_cod.upload_hash
                data = self.get_file_data(file_name)

                if data:
                    if self.s3.upload_file(file_data=data, file_key=file_name):
                        print("Arquivo {0} sincronizado com sucesso as {1}".format(file_name, datetime.now()))
                        self.process_synced_file(file)
                else:
                    self.process_error_files(file)
                    continue

            print("Fim da execucao do script")
        else:
            print("Nenhuma sincronizacao agendada para o momento. \\o/")

    def process_synced_file(self, sync):
        file_absolute = os.path.realpath(self.storage_path + '/' + sync.upload_cod.upload_hash)
        public_file_absolute = os.path.realpath(self.public_path + '/' + sync.upload_cod.upload_hash)
        # Atualiza as tabelas
        self.update_file_success(sync.upload_cod)
        self.update_sync_success(sync)

        # Remove arquivo do storage
        os.unlink(file_absolute)

        # Remove a copia publica do arquivo
        if os.path.isfile(public_file_absolute):
            os.unlink(public_file_absolute)

        return True

    @staticmethod
    def update_file_success(file):
        file.upload_s3 = 'S'
        file.save()
        return True

    @staticmethod
    def update_sync_success(sync):
        sync.upload_sync = 'C'
        sync.upload_sync_report = "{sucesso: Arquivo enviado com sucesso.}"
        sync.save()
        return True

    def process_error_files(self, sync):
        # Atualiza as tabelas
        self.update_sync_error(sync)

    def update_sync_error(self, sync):
        file_name = sync.upload_cod.upload_hash
        sync.upload_sync = 'F'
        sync.upload_sync_report = str({"error": "file {0}/{1} not found.".format(self.storage_path, file_name)})
        sync.save()
        return True

    def get_file_data(self, file_name):
        storage_path = self.storage_path
        file_absolute = os.path.realpath(storage_path + '/' + file_name)
        if not os.path.isfile(file_absolute):
            print("O arquivo {0} nao existe ou nao pode ser acessado. As {1}".format(file_absolute, datetime.now()))
            return False
        else:
            file = open(file_absolute, 'rb')
            file_data = file.read()
            file.close()
            return file_data

    @staticmethod
    def get_files_sync():
        return UploadSync.objects.filter(upload_sync='A')[:100]

    @staticmethod
    def lock_files_in_progress(files: object):

        for file in files:
            file.upload_sync = 'P'
            file.save()

        return True

    def append_synced_file(self, file):
        self.__synced_files.append(file)
        return self

    def append_error_file(self, file):
        self.__error_files.append(file)
        return self
