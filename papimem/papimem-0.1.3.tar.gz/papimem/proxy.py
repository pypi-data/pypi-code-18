import os
import logging

from mitmproxy import controller, master, options, http
from mitmproxy.proxy.server import ProxyServer

from papimem.storage.base import ReqRes


class ProxyMaster(master.Master):
    """ Main proxy class """

    def __init__(self, opts, server, storage, mock_mode=False):
        master.Master.__init__(self, opts, server)
        self.storage = storage
        self.mock_mode = mock_mode

    def run(self):
        """ Run proxy server """
        try:
            return master.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    @controller.handler
    def request(self, flow):
        """ Request handler. """
        key = self.storage.generate_key(flow.request)
        if not self.mock_mode:
            logging.info("Proxy request to remote host: %s", key)
            return flow.reply

        # if mock_mode is enabled then return previously saved response
        reqres = self.storage.get(key)
        if reqres:
            logging.info("Serving stored response for: %s", key)
            flow.response = http.HTTPResponse.make(
                reqres.response.status_code,
                reqres.response.content,
                dict(reqres.response.headers)
            )
            return

        logging.error("Can't find response in storage for: %s", key)
        return flow.reply.kill()

    @controller.handler
    def response(self, flow):
        """ Response handler """
        if self.mock_mode:
            return

        # save response object
        key = self.storage.generate_key(flow.request)
        self.storage.save(key, ReqRes(flow.request, flow.response))
        return flow.reply
