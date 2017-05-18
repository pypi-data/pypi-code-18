import logging
import sys
import multiprocessing

from mitmproxy import proxy, options
from mitmproxy.proxy.server import ProxyServer

from papimem.proxy import ProxyMaster
from papimem.storage import get_storage
from papimem.web import webapp


WEB_SERVER_NAME = 'localhost:8090'


class PapimemApp:
    """ Main application class. """

    def __init__(self, proxy_port, storage_dsn, mock_mode):
        self.proxy_port = int(proxy_port)
        self.storage_dsn = storage_dsn
        self.storage = get_storage(storage_dsn)
        self.mock_mode = mock_mode

        logging.root.setLevel(logging.INFO)
        logging.root.addHandler(logging.StreamHandler(sys.stdout))

    def run(self):
        """ Start proxy server and web explorer app. """
        # start separete process with proxy
        proxy_proc = multiprocessing.Process(target=self.run_proxy)
        proxy_proc.start()

        # start web explorer in main process
        webapp.config.update(dict(
            STORAGE_DSN=self.storage_dsn,
            SERVER_NAME=WEB_SERVER_NAME,
        ))
        webapp.run()

    def run_proxy(self):
        """ Run proxy server """
        opts = options.Options(listen_port=self.proxy_port)
        config = proxy.ProxyConfig(opts)
        server = ProxyServer(config)

        pmaster = ProxyMaster(opts, server, self.storage, self.mock_mode)
        logging.info('Proxy server is running on port %s', self.proxy_port)
        pmaster.run()
