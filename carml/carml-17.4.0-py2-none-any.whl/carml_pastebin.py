from __future__ import print_function
import sys
import time
import functools

import zope.interface
from twisted.python import usage, log
from twisted.plugin import IPlugin
from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet.endpoints import serverFromString, clientFromString
from twisted.web.http import HTTPChannel
from twisted.web.static import Data
from twisted.web.resource import Resource
from twisted.web.server import Site

from carml.interface import ICarmlCommand
from carml import util
import txtorcon
from txtorcon import TCPHiddenServiceEndpoint


class _PasteBinHTTPChannel(HTTPChannel):
    def connectionMade(self):
        HTTPChannel.connectionMade(self)
        self.site._got_client()

    def connectionLost(self, reason):
        HTTPChannel.connectionLost(self, reason)
        self.site._lost_client()


class PasteBinSite(Site):
    """
    See https://github.com/habnabit/polecat/blob/master/polecat.py for
    the inspriation behind this.

    This class exists so we can count active connections and support a
    command-line option for serving a particular number of
    requests. We need to wait until pending data is written on any
    valid connections that are still active when we reach our limit.
    """

    protocol = _PasteBinHTTPChannel

    def __init__(self, *args, **kw):
        self.active_clients = 0
        self.active_requests = set()
        self._max_requests = kw['max_requests']
        del kw['max_requests']
        self._request_count = 0
        self._stopping_deferred = None
        Site.__init__(self, *args, **kw)

    def getResourceFor(self, request):
        "Override Site so we can track active requests"
        if request.requestHeaders.hasHeader('user-agent'):
            ua = ' '.join(request.requestHeaders.getRawHeaders('user-agent'))
            print('{}: Serving request to User-Agent "{}".'.format(time.asctime(), ua))
        else:
            print('{}: Serving request with no incoming User-Agent header.'.format(time.asctime()))

        # track requsts currently being serviced, so we can nicely
        # shut them off
        self.active_requests.add(request)
        request.notifyFinish().addBoth(self._forget_request, request)

        # see if we've reached the maximum requests
        self._request_count += 1
        if self._max_requests is not None:
            if self._request_count >= self._max_requests:
                d = self.gracefully_stop()
                d.addBoth(lambda x: reactor.stop())

        # call through to parent
        return Site.getResourceFor(self, request)

    def _forget_request(self, request, _):
        self.active_requests.discard(request)

    def _got_client(self):
        self.active_clients += 1

    def _lost_client(self):
        self.active_clients -= 1
        if self.active_clients <= 0 and self._stopping_deferred:
            self._stopping_deferred.callback(None)
            self._stopping_deferred = None

    def gracefully_stop(self):
        "Returns a Deferred that fires when all clients have disconnected."
        if not self.active_clients:
            return defer.succeed(None)
        for request in self.active_requests:
            request.setHeader('connection', 'close')
        self._stopping_deferred = defer.Deferred()
        return self._stopping_deferred


def _progress(percent, tag, message):
    print(util.pretty_progress(percent), message)


@defer.inlineCallbacks
def run(reactor, cfg, tor, dry_run, once, file, count, keys):
    "ICarmlCommand API"

    to_share = file.read()
    file.close()

    # stealth auth. keys
    authenticators = []
    if keys:
        for x in xrange(keys):
            authenticators.append('carml_%d' % x)

    if len(authenticators):
        print(len(to_share), "bytes to share with",
              len(authenticators), "authenticated clients.")
    else:
        print(len(to_share), "bytes to share.")
    sys.stdout.flush()

    if dry_run:
        print('Not launching a Tor, listening on 8899.')
        ep = serverFromString(reactor, 'tcp:8899:interface=127.0.0.1')
    elif True:  # connection is None:
        print("Launching Tor.")
        ep = TCPHiddenServiceEndpoint.global_tor(reactor, 80)
        txtorcon.IProgressProvider(ep).add_progress_listener(_progress)
        if keys:
            ep.stealth_auth = [
                'user_{}'.format(n)
                for n in range(keys)
            ]
    else:
        config = yield txtorcon.TorConfig.from_connection(connection)
        ep = txtorcon.TCPEphemeralHiddenServiceEndpoint(reactor, config, 80)

    root = Resource()
    data = Data(to_share, 'text/plain')
    root.putChild('', data)

    if once:
        count = 1
    port = yield ep.listen(PasteBinSite(root, max_requests=count))

    if keys == 0:
        clients = None
    else:
        # FIXME
        clients = port.tor_config.hiddenservices[0].clients

    host = port.getHost()
    if dry_run:
        print("Try it locally via http://127.0.0.1:8899")

    elif clients:
        print("You requested stealth authentication.")
        print("Tor has created %d keys; each key should be given to one person." % len(clients))
        print('They can set one using the "HidServAuth" torrc option, like so:')
        print("")
        for client in clients:
            print("  HidServAuth %s %s" % (client[0], client[1]))
        print("")
        print("Alternatively, any Twisted endpoint-aware client can be given")
        print("the following string as an endpoint:")
        print("")
        for client in clients:
            print("  tor:%s:authCookie=%s" % (client[0], client[1]))
        print("")
        print("For example, using carml:")
        print("")
        for client in clients:
            print("  carml copybin --service tor:%s:authCookie=%s" % (client[0], client[1]))

    else:
        print("People using Tor Browser Bundle can find your paste at (once the descriptor uploads):")
        print("\n   http://{0}\n".format(host.onion_uri))
        print("for example:")
        print("   torsocks curl -o data.asc http://{0}\n".format(host.onion_uri))
        if not count:
            print("Type Control-C to stop serving and shut down the Tor we launched.")
        print("If you wish to keep the hidden-service keys, they're in (until we shut down):")
        print(ep.hidden_service_dir)

    reactor.addSystemEventTrigger('before', 'shutdown',
                                  lambda: print(util.colors.red('Shutting down.')))
    # we never callback() on this, so we serve forever
    d = defer.Deferred()
    yield d
