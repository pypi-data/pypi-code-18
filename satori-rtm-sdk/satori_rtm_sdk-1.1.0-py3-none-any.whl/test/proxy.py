# -*- coding: utf-8 -*-

from __future__ import print_function
import unittest

import satori.rtm.connection as sc
import threading

from test.utils import make_channel_name, get_test_endpoint_and_appkey
from test.utils import print_resource_usage

endpoint, appkey = get_test_endpoint_and_appkey()


class TestConnectionWithProxy(unittest.TestCase):
    def test_write_read(self):
        proxy = ('127.0.0.1', 7711)
        conn = sc.Connection(endpoint, appkey, proxy=proxy)
        conn.start()

        k, v = make_channel_name('write_read'), 'value1'
        mailbox = []
        event = threading.Event()

        def callback(pdu):
            mailbox.append(pdu)
            event.set()

        conn.write(k, v, callback=callback)
        event.wait(10)
        event.clear()

        conn.read(k, callback=callback)
        event.wait(10)
        conn.stop()

        assert len(mailbox) == 2
        write_ack = mailbox[0]
        read_ack = mailbox[1]
        assert write_ack['action'] == 'rtm/write/ok'
        assert read_ack['action'] == 'rtm/read/ok'
        assert read_ack['body']['message'] == v


if __name__ == '__main__':
    unittest.main()
    print_resource_usage()