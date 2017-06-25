# -*- coding: utf-8 -*-

__version__ = '1.2.3'


import regnupg
import sys


_py3 = sys.version_info[0] == 3


if _py3:
    from io import BytesIO as StrIO
    import urllib.request as urllib
    import xmlrpc.client as _xmlrpclib
else:
    from StringIO import StringIO as StrIO
    import urllib2 as urllib
    import xmlrpclib as _xmlrpclib


GzipDecodedResponse = _xmlrpclib.GzipDecodedResponse


class GpgTransport(_xmlrpclib.Transport):
    user_agent = 'pgpxmlrpc v %s' % __version__

    def __init__(self, gpg_homedir, gpg_key, gpg_password, gpg_server_key, gpg_executable='gpg', headers=None,
                 use_datetime=0, encoding='utf8'):
        _xmlrpclib.Transport.__init__(self, use_datetime)
        self.gpg_server_key = gpg_server_key
        self.gpg_key = gpg_key
        self.gpg_password = gpg_password
        self.gpg = regnupg.GnuPG(homedir=gpg_homedir, executable=gpg_executable)
        self.gpg.encoding = encoding
        self.headers = headers or {}

    def send_request(self, connection, handler, request_body, *args, **kwargs):
        return _xmlrpclib.Transport.send_request(
            self,
            connection,
            '{}/{}'.format(handler.rstrip('/'), self.gpg_key),
            request_body,
            *args,
            **kwargs
        )

    def send_content(self, connection, request_body):
        # FIXME: Определять ACCEPT-ENCODING: gzip сервера и сжимать пост
        for header, value in self.headers.items():
            if header not in ('Content-Type', 'Content-Length'):
                connection.putheader(header, value)
        connection.putheader('Content-Type', 'application/pgp-encrypted')
        encrypted = self.gpg.encrypt(request_body, self.gpg_server_key, self.gpg_key,
                                     self.gpg_password, always_trust=True).data.encode('utf-8')
        connection.putheader('Content-Length', str(len(encrypted)))
        connection.endheaders(encrypted)

    def parse_response(self, response):
        if hasattr(response, 'getheader') and response.getheader('Content-Encoding', '') == 'gzip':
            stream = GzipDecodedResponse(response)
        else:
            stream = response

        encrypted = []
        while True:
            data = stream.read(1024)
            if self.verbose:
                print('encrypted body:', data)
            if not data:
                break
            encrypted.append(data)
        encrypted = (b'' if _py3 else '').join(encrypted)

        try:
            decrypted = self.gpg.decrypt(encrypted, self.gpg_password, self.gpg_server_key, always_trust=True).data
            if not decrypted:
                raise RuntimeError('Decryption failed')
            decrypted = decrypted.encode('utf-8')
            return _xmlrpclib.Transport.parse_response(self, StrIO(decrypted))
        except regnupg.Error:
            return _xmlrpclib.Transport.parse_response(self, StrIO(encrypted))


class ProxyGpgTransport(_xmlrpclib.Transport):
    def __init__(self, proxy, gpg_homedir, gpg_key, gpg_password, gpg_server_key, gpg_executable='gpg', headers=None,
                 use_datetime=0, encoding='utf8'):
        _xmlrpclib.Transport.__init__(self, use_datetime)
        self.proxy = {'http': proxy} if proxy else {}
        self.gpg_server_key = gpg_server_key
        self.gpg_key = gpg_key
        self.gpg_password = gpg_password
        self.gpg = regnupg.GnuPG(homedir=gpg_homedir, executable=gpg_executable)
        self.gpg.encoding = encoding
        self.headers = headers or {}

    def request(self, host, handler, request_body, verbose=0):
        self.verbose = verbose

        headers = {header: val for header, val in self.headers.items() if
                   header not in ('Content-Type', 'Content-Length')}
        headers['Content-Type'] = 'application/pgp-encrypted'

        url = 'http://{}{}/{}'.format(host, handler.rstrip('/'), self.gpg_key)
        proxy_handler = urllib.ProxyHandler(self.proxy)
        opener = urllib.build_opener(proxy_handler, urllib.HTTPHandler)

        encrypted = opener.open(
            urllib.Request(
                url,
                self.gpg.encrypt(
                    request_body,
                    self.gpg_server_key,
                    self.gpg_key,
                    self.gpg_password,
                    always_trust=True
                ).data.encode('utf-8'),
                headers
            )
        ).read()

        try:
            return self.parse_response(StrIO(encrypted))
        except _xmlrpclib.Fault:
            raise
        except:
            decrypted = self.gpg.decrypt(encrypted, self.gpg_password, self.gpg_server_key,
                                         always_trust=True).data.encode('utf-8')
            if not decrypted:
                raise RuntimeError('Decryption failed')
            return self.parse_response(StrIO(decrypted))


def Service(uri, service_key, gpg_homedir, gpg_key, gpg_password, gpg_executable='gpg', headers=None, use_datetime=1,
            encoding='utf8'):
    return _xmlrpclib.Server(
        uri=uri if uri.endswith('/') else uri + '/',
        transport=GpgTransport(
            gpg_homedir,
            gpg_key,
            gpg_password,
            gpg_server_key=service_key,
            gpg_executable=gpg_executable,
            headers=headers,
            use_datetime=use_datetime,
            encoding=encoding
        ),
        allow_none=True
    )


def ProxyService(uri, proxy, service_key, gpg_homedir, gpg_key, gpg_password, gpg_executable='gpg', headers=None,
                 use_datetime=1, encoding='utf8'):
    return _xmlrpclib.Server(
        uri=uri if uri.endswith('/') else uri + '/',
        transport=ProxyGpgTransport(
            proxy,
            gpg_homedir,
            gpg_key,
            gpg_password,
            gpg_server_key=service_key,
            gpg_executable=gpg_executable,
            headers=headers,
            use_datetime=use_datetime,
            encoding=encoding
        ),
        allow_none=True
    )
