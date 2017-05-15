import os

import click
from mitmproxy.certs import CertStore

from papimem.app import PapimemApp
from papimem.storage.redis import DEFAULT_DSN


CONFDIR = "~/.mitmproxy"
CERTSTORE_BASENAME = "mitmproxy"


@click.command()
@click.option(
    '--proxy_port', default='8080',
    help='Proxy server http and https port to run on.')
@click.option(
    '--storage_dsn', prompt=True, default=DEFAULT_DSN,
    help='Persistent storage DSN for requests and responses.')
@click.option(
    '--mock_mode/--no-mock_mode', prompt=True, default=False,
    help='Run on mock mode (request are served from storage)'
         ' or pass them to remote host and store.')
def run(proxy_port, storage_dsn, mock_mode):
    """ Python API request-response memorizer """
    # make sure root CA is generated for mitmproxy library
    ca_path = os.path.expanduser(
        os.path.join(CONFDIR, CERTSTORE_BASENAME, "-ca.pem")
    )
    if not os.path.exists(ca_path):
        CertStore.from_store(
            os.path.expanduser(CONFDIR),
            CERTSTORE_BASENAME
        )

    app = PapimemApp(proxy_port, storage_dsn, mock_mode)
    app.run()


if __name__ == '__main__':
    run()
