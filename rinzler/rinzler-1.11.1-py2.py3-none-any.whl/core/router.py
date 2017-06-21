from collections import OrderedDict

from django.http.request import HttpRequest
from django.views.generic import TemplateView

from onyxerp.core.services.jwt_service import JwtService
from rinzler.core.response import Response

from storage_api.services.lista_upload_service import ListaUploadService
from storage_api.settings import CONFIG
from storage_api.services.upload_service import UploadService


class DriveController(TemplateView):

    jwt_service = JwtService(CONFIG)

    def connect(self, app: dict()):

        router = app['router']

        router.post("/{ref_cod}/modulo/{app_mod_cod}/", self.upload)
        router.get("/{ref_cod}/modulo/{app_mod_cod}/", self.lista_arquivo_upload)
        router.get("/lista/", self.lista_tipos_arquivos)
        router.get("/acompanhamento/{data_hora}/", self.get_acompanhamento)

        return app

    @staticmethod
    def get_acompanhamento(request: HttpRequest, app: dict(), **params: dict):

        data_hora = params['data_hora']
        service = ListaUploadService()

        resultado = service.get_acompanhamento(data_hora)

        response = OrderedDict({
            "status": True,
            "data": {
                "total": resultado
            }
        })

        return Response(response, content_type="application/json")

    @staticmethod
    def lista_tipos_arquivos(request: HttpRequest, app: dict(), **params: dict):

        service = ListaUploadService()

        resultado = service.get_lista_tipos()

        response = OrderedDict({
            "status": True,
            "data": resultado
        })

        if 'status' in resultado and resultado['status'] == False:
            response['status'] = False
            return Response(response, content_type="application/json", status=500)
        else:
            return Response(response, content_type="application/json")

    @staticmethod
    def lista_arquivo_upload(request: HttpRequest, app: dict(), **params: dict):

        ref_cod = params['ref_cod']
        app_mod_cod = params['app_mod_cod']

        service = ListaUploadService()

        resultado = service.get_arquivos(ref_cod, app_mod_cod)

        response = OrderedDict({
            "status": True,
            "data": resultado
        })

        if 'status' in resultado and resultado['status'] == False:
            response['status'] = False
            return Response(response, content_type="application/json", status=500)
        else:
            return Response(response, content_type="application/json")

    @staticmethod
    def upload(request: HttpRequest, app: dict(), **params: dict):

        token = app['auth_data']['token']
        jwt_data = app['auth_data']['data']

        payload = request.body.decode("utf-8")

        service = UploadService()
        service.set_jwt(token).set_jwt_data(jwt_data['data']).set_payload(payload)

        ref_cod = params['ref_cod']
        app_mod_cod = params['app_mod_cod']

        resultado = service.upload(ref_cod, app_mod_cod)

        response = OrderedDict({
            "status": True,
            "data": resultado
        })

        if 'status' in resultado and resultado['status'] == False:
            response['status'] = False
            return Response(response, content_type="application/json", status=500)
        else:
            return Response(response, content_type="application/json")
