import sys

import requests
import pytest

from mock import patch

import shutil
import six
import os
import tempfile
import re

from six.moves.http_client import HTTPSConnection, HTTPConnection

from io import BytesIO


# ============================================================================
@pytest.fixture(params=['http', 'https'])
def scheme(request):
    return request.param


@pytest.fixture(params=['ws', 'wss'])
def ws_scheme(request):
    return request.param


# ============================================================================
class BaseWSGIProx(object):
    @classmethod
    def setup_class(cls):
        cls.test_ca_dir = tempfile.mkdtemp()
        cls.root_ca_file = os.path.join(cls.test_ca_dir, 'wsgiprox-ca-test.pem')

        from .fixture_app import make_application
        cls.app = make_application(cls.root_ca_file)

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.test_ca_dir)

    @classmethod
    def proxy_dict(cls, port, host='localhost'):
        return {'http': 'http://{0}:{1}'.format(host, port),
                'https': 'https://{0}:{1}'.format(host, port)
               }

    def test_non_chunked(self, scheme):
        res = requests.get('{0}://example.com/path/file?foo=bar&addproxyhost=true'.format(scheme),
                           proxies=self.proxies,
                           verify=self.root_ca_file)

        assert(res.headers['Content-Length'] != '')
        assert(res.text == 'Requested Url: /prefix/{0}://example.com/path/file?foo=bar&addproxyhost=true Proxy Host: wsgiprox'.format(scheme))

    def test_non_chunked_custom_port(self, scheme):
        res = requests.get('{0}://example.com:123/path/file?foo=bar&addproxyhost=true'.format(scheme),
                           proxies=self.proxies,
                           verify=self.root_ca_file)

        assert(res.headers['Content-Length'] != '')
        assert(res.text == 'Requested Url: /prefix/{0}://example.com:123/path/file?foo=bar&addproxyhost=true Proxy Host: wsgiprox'.format(scheme))

    @pytest.mark.skipif(sys.version_info >= (3,0) and sys.version_info < (3,4),
                        reason='Not supported in py3.3')
    def test_with_sni(self):
        import ssl
        conn = SNIHTTPSConnection('localhost', self.port, context=ssl.create_default_context(cafile=self.root_ca_file))
        # set CONNECT host:port
        conn.set_tunnel('93.184.216.34', 443)
        # set actual hostname
        conn._server_hostname = 'example.com'
        conn.request('GET', '/path/file?foo=bar&addproxyhost=true')
        res = conn.getresponse()
        text = res.read().decode('utf-8')
        conn.close()

        assert(res.getheader('Content-Length') != '')
        assert(text == 'Requested Url: /prefix/https://example.com/path/file?foo=bar&addproxyhost=true Proxy Host: wsgiprox')


    def test_chunked(self, scheme):
        res = requests.get('{0}://example.com/path/file?foo=bar&chunked=true'.format(scheme),
                           proxies=self.proxies,
                           verify=self.root_ca_file)

        #if not (self.server_type == 'uwsgi' and scheme == 'http'):
        #    assert(res.headers['Transfer-Encoding'] == 'chunked')
        assert(res.headers.get('Content-Length') == None)
        assert(res.text == 'Requested Url: /prefix/{0}://example.com/path/file?foo=bar&chunked=true'.format(scheme))

    @patch('six.moves.http_client.HTTPConnection._http_vsn', 10)
    @patch('six.moves.http_client.HTTPConnection._http_vsn_str', 'HTTP/1.0')
    def test_chunked_force_http10_buffer(self, scheme):
        res = requests.get('{0}://example.com/path/file?foo=bar&chunked=true'.format(scheme),
                           proxies=self.proxies,
                           verify=self.root_ca_file)

        assert(res.headers.get('Transfer-Encoding') == None)

        # https, must buffer and set content-length to avoid breaking CONNECT envelope
        # for http, up-to wsgi server if buffering
        if scheme == 'https':
            assert(res.headers['Content-Length'] != '')
        assert(res.text == 'Requested Url: /prefix/{0}://example.com/path/file?foo=bar&chunked=true'.format(scheme))

    def test_write_callable(self, scheme):
        res = requests.get('{0}://example.com/path/file?foo=bar&write=true'.format(scheme),
                           proxies=self.proxies,
                           verify=self.root_ca_file)

        assert(res.text == 'Requested Url: /prefix/{0}://example.com/path/file?foo=bar&write=true'.format(scheme))

    def test_post(self, scheme):
        res = requests.post('{0}://example.com/path/post'.format(scheme), data=BytesIO(b'ABC=1&xyz=2'),
                            proxies=self.proxies,
                            verify=self.root_ca_file)

        assert(res.text == 'Requested Url: /prefix/{0}://example.com/path/post Post Data: ABC=1&xyz=2'.format(scheme))

    def test_fixed_host(self, scheme):
        res = requests.get('{0}://wsgiprox/path/file?foo=bar'.format(scheme),
                           proxies=self.proxies,
                           verify=self.root_ca_file)

        assert(res.text == 'Requested Url: /path/file?foo=bar')

    def test_alt_host(self, scheme):
        res = requests.get('{0}://proxy-alias/path/file?foo=bar&addproxyhost=true'.format(scheme),
                           proxies=self.proxies,
                           verify=self.root_ca_file)

        assert(res.text == 'Requested Url: /path/file?foo=bar&addproxyhost=true Proxy Host: proxy-alias')

    def test_proxy_app(self, scheme):
        res = requests.get('{0}://proxy-app-1/path/file'.format(scheme),
                           proxies=self.proxies,
                           verify=self.root_ca_file)

        assert(res.text == 'Custom App: proxy-app-1 req to /path/file')

    def test_download_pem(self, scheme):
        res = requests.get('{0}://wsgiprox/download/pem'.format(scheme),
                           proxies=self.proxies,
                           verify=self.root_ca_file)

        assert res.headers['content-type'] == 'application/x-x509-ca-cert'

    def test_download_pkcs12(self, scheme):
        res = requests.get('{0}://wsgiprox/download/p12'.format(scheme),
                           proxies=self.proxies,
                           verify=self.root_ca_file)

        assert res.headers['content-type'] == 'application/x-pkcs12'

    def test_non_proxy_passthrough(self):
        res = requests.get('http://localhost:' + str(self.port) + '/path/file?foo=bar')
        assert(res.text == 'Requested Url: /path/file?foo=bar')


# ============================================================================
class SNIHTTPSConnection(HTTPSConnection):
    def connect(self):
        HTTPConnection.connect(self)

        server_hostname = self._server_hostname

        self.sock = self._context.wrap_socket(self.sock,
                                              server_hostname=self._server_hostname)


