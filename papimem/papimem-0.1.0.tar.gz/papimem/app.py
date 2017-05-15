import asyncio
import logging
import sys
import multiprocessing

import aiohttp
from aiohttp import web
from mitmproxy import proxy, options
from mitmproxy.proxy.server import ProxyServer

from proxy import ProxyMaster
from storage import get_storage


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
        # start separete process with proxy
        proxy_proc = multiprocessing.Process(target=self.run_proxy)
        proxy_proc.start()

    def run_proxy(self):
        """ Run proxy server """
        opts = options.Options(listen_port=self.proxy_port)
        config = proxy.ProxyConfig(opts)
        server = ProxyServer(config)

        pmaster = ProxyMaster(opts, server, self.storage, self.mock_mode)
        logging.info('Proxy server is running on port %s', self.proxy_port)
        pmaster.run()
