from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
import os
import json
import struct
from datetime import datetime
import pytz
from jumper_ble_logger.event_parser_middleware import EventParser
from jumper_ble_logger.ble_logger import change_dictionary_keys_from_str_to_int, GattPeripheralLogger
from jumper_ble_logger.hci_protocol import hci_protocol

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
VALID_CONFIG_FILE = os.path.join(ROOT_DIR, 'events_config.json')
DEFAULT_MAC = 'AA:BB:CC:DD:EE:FF'


def create_packet(timestamp=0, version=1, event_type=2, data_length=1, data=b'\x01'):
    return struct.pack('<BBIB{}s'.format(data_length), version, event_type, timestamp, data_length, data)


def dict_from_config_file(config_file):
    with open(config_file) as fd:
        config_file = change_dictionary_keys_from_str_to_int(json.load(fd))
        return {int(k): v for k, v in config_file.items()}


valid_config = dict_from_config_file(VALID_CONFIG_FILE)
invalid_config = {
    2: {
        "type": "eveny_type",
        "strings": ["value"],
        "data": {
            "value": "H"
        }
    }
}


class EventParserTests(unittest.TestCase):
    def setUp(self):
        self.events_parser = EventParser(valid_config)

    def tearDown(self):
        pass

    def test_invalid_config(self):
        self.assertRaises(ValueError, EventParser, invalid_config)

    def test_sanity(self):
        timestamp = datetime.now(pytz.utc)
        packet = create_packet(timestamp=0)
        event_dict = self.events_parser.parse(DEFAULT_MAC, packet, timestamp)

        expected_dict = dict(timestamp=timestamp, type='ADVERTISING_STATE', is_on=1, device_id=DEFAULT_MAC)
        self.assertDictEqual(expected_dict, event_dict)

    def test_boot_event(self):
        timestamp = datetime.now(pytz.utc)
        data = b'v1.1.2\x00'
        packet = create_packet(timestamp=0, version=1, event_type=0, data_length=len(data), data=data)
        event_dict = self.events_parser.parse(DEFAULT_MAC, packet, timestamp)
        expected_dict = dict(timestamp=timestamp, type='DEVICE_BOOT', version='v1.1.2', device_id=DEFAULT_MAC)
        self.assertDictEqual(expected_dict, event_dict)

    def test_string_event(self):
        timestamp = datetime.now(pytz.utc)
        data = b'HELLO\x00'
        packet = create_packet(timestamp=0, version=1, event_type=5, data_length=len(data), data=data)
        event_dict = self.events_parser.parse(DEFAULT_MAC, packet, timestamp)
        expected_dict = dict(timestamp=timestamp, type='CUSTOM_STRING', custom_string='HELLO', device_id=DEFAULT_MAC)
        self.assertDictEqual(expected_dict, event_dict)


DEFAULT_MAC_ADDRESS = 'aa:bb:cc:dd:ee:ff'
DEFAULT_CONNECTION_HANDLE = 10
# CONNECTION_PACK = hci_protocol.HciPacket.build(
#     dict(
#         type='EVENT_PACKET',
#         payload=dict(
#             event='LE_META_EVENT',
#             payload=dict(
#                 subevent='LE_CONNECTION_COMPLETED',
#                 payload=dict(
#
#                 )
#             )
#         )
#     )
# )

class GattPeripheralLoggerTests(unittest.TestCase):
    def setUp(self):
        self.peripheral_logger = GattPeripheralLogger(DEFAULT_MAC_ADDRESS, DEFAULT_CONNECTION_HANDLE)

    def tearDown(self):
        pass

    def test_first_connection(self):



def main():
    unittest.main()

if __name__ == '__main__':
    main()
