from .message import (
    Message,
    MessageOpcode,
    MessageSerializer,
    MessageDeserializer
)

import json
import socket
import ssl
import struct
import time

class HeurisClient:
    HOST = 'hmp.heuris.io'
    PORT = 21099

    def __init__(self, username, token, **kwargs):
        self._username = username
        self._token = token
        self._parse_options(kwargs)
        self._reset_backoff()
        self._start()

    def send_measurement(self, entries, **kwargs):
        begin = self._utcnow()
        measurement = self._create_measurement_message(entries)
        self._send_measurement(measurement)
        self._sleep_if_needed(begin, kwargs)

    def _parse_options(self, kwargs):
        self._auto_reconnect = True
        if 'auto_reconnect' in kwargs:
            self._auto_reconnect = kwargs['auto_reconnect']

    def _reset_backoff(self):
        self._backoff = 100

    def _start(self):
        if self._auto_reconnect is True:
            self._start_with_auto_reconnect()
        else:
            self._start_without_auto_reconnect()

    def _start_with_auto_reconnect(self):
        while True:
            try:
                self._start_without_auto_reconnect()
                self._reset_backoff()
                break
            except (ConnectionRefusedError, ssl.SSLEOFError):
                self._sleep(self._backoff)
                self._backoff *= 2

    def _start_without_auto_reconnect(self):
        self._socket = self._create_secure_socket()
        self._connect()
        self._login()

    def _create_secure_socket(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        return context.wrap_socket(
            socket.socket(),
            server_hostname = self.HOST)

    def _login(self):
        msg = self._create_login_message()
        self._send_message(msg)
        self._handle_response()

    def _connect(self):
        self._socket.connect((self.HOST, self.PORT))

    def _create_login_message(self):
        msg = Message(MessageOpcode.LOGIN)
        msg.entries['username'] = self._username
        msg.entries['token'] = self._token
        return msg

    def _send_message(self, msg):
        data = MessageSerializer.serialize(msg)
        self._socket.send(struct.pack('>I', len(data)))
        self._socket.send(data)

    def _handle_response(self):
        reply = self._read_message()
        if reply.opcode == MessageOpcode.ERROR:
            raise Exception(reply.entries['message'])

    def _read_message(self):
        length = self._read_message_length()
        return self._read_message_payload(length)

    def _read_message_length(self):
        header = self._socket.recv(4)
        return struct.unpack('>I', header)[0]

    def _read_message_payload(self, length):
        payload = self._socket.recv(length)
        return MessageDeserializer.deserialize(payload)

    def _create_measurement_message(self, entries):
        measurement = Message(MessageOpcode.MEASUREMENT)
        measurement.entries = entries
        self._add_time_if_needed(measurement)
        return measurement

    def _add_time_if_needed(self, measurement):
        if 'time' not in measurement.entries:
            measurement.entries['time'] = self._utcnow()

    def _utcnow(self):
        return int(round(time.time() * 1000))

    def _send_measurement(self, measurement):
        if self._auto_reconnect is True:
            self._send_measurement_with_auto_reconnect(measurement)
        else:
            self._send_measurement_without_auto_reconnect(measurement)

    def _send_measurement_with_auto_reconnect(self, measurement):
        while True:
            try:
                self._send_measurement_without_auto_reconnect(measurement)
                break
            except struct.error:
                self._start()

    def _send_measurement_without_auto_reconnect(self, measurement):
        self._send_message(measurement)
        self._handle_response()

    def _sleep_if_needed(self, begin, kwargs):
        if 'period' in kwargs:
            self._sleep(max(0, kwargs['period'] - (self._utcnow() - begin)))
        if 'wait' in kwargs:
            self._sleep(kwargs['wait'])

    def _sleep(self, milliseconds):
        time.sleep(milliseconds / 1000.0)
