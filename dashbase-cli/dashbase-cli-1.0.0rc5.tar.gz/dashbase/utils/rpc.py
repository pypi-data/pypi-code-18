import urllib3
from urllib3.util import Retry

from dashbase.cli.constants import RPC_BACK_OFF_FACTOR, NUM_TRIES


class RPC():
    def __init__(self, host_port):
        self.url = host_port
        self.init_connection()

    def init_connection(self):
        retries = Retry(connect=NUM_TRIES, backoff_factor=RPC_BACK_OFF_FACTOR)
        self.headers = {"Content-type": "text/plain", "Accept": "application/json"}
        self.conn = urllib3.connection_from_url(self.url, timeout=600, retries=retries)

    def do_get(self, url):
        response = self.conn.request("GET", url)
        return response

    def close(self):
        print("Connection closed.")
        self.conn.close()
