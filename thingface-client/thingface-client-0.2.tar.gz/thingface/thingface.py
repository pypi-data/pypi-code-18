# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

import json
import re
import os.path
import paho.mqtt.client as mqtt
from time import sleep


def _mqttc_connect_handler(mqttc, userdata, flags, rc):
    # print('connect_handler: %s %s %d' % (userdata, flags, rc))
    if hasattr(mqttc, '_thingface'):
        self = mqttc._thingface
        if rc == 0:
            self._connection_handler(1)
        else:
            self._error_handler(
                'Connection refused - ' +
                [
                    'incorrect protocol version',
                    'invalid client identifier',
                    'server unavailable',
                    'bad username or password',
                    'not authorised',
                ][rc - 1]
            )


def _mqttc_disconnect_handler(mqttc, userdata, rc):
    # print('disconnect_handler: %s %d' % (userdata, rc))
    if hasattr(mqttc, '_thingface'):
        self = mqttc._thingface
        self._connection_handler(0)
        if rc != 0:
            self._error_handler('disconnection was unexpected')


def _mqttc_message_handler(mqttc, userdata, message):
    # print('message.topic: %s' % (message.topic,))
    # print('message.payload: %s' % (message.payload,))
    if hasattr(mqttc, '_thingface'):
        self = mqttc._thingface
        if re.search('^[du]{1}\/c', message.topic):
            payload = json.loads(message.payload)
            groups = re.search(
                '([du]{1})\/c\/([a-zA-Z0-9]+)\/([a-zA-Z0-9]+)',
                message.topic
            ).groups()
            sender_type = groups[0]
            sender_id = groups[1]
            if self._message_handler:
                self._message_handler(
                    sender_type,
                    sender_id,
                    payload['c'],
                    payload['a']
                )


# def _mqttc_publish_handler(mqttc, userdata, mid):
    # print('publish_handler: %s %s' % (userdata, mid))


# def _mqttc_subscribe_handler(mqttc, userdata, mid, granted_qos):
    # print('subscribe_handler: %s %s %s' % (userdata, mid, granted_qos))


# def _mqttc_unsubscribe_handler(mqttc, userdata, mid):
    # print('unsubscribe_handler: %s %s' % (userdata, mid))


# def _mqttc_log_handler(mqttc, userdata, level, buf):
    # print('log_handler: %s %d %s' % (userdata, level, buf))


class Client:
    '''Thingface mqtt client.'''

    def _connection_handler(self, state):
        '''Event handler for connection state change.'''
        pass

    def _error_handler(self, error):
        '''Event handler for errors.'''
        pass

    def _message_handler(self, sender_type, sender_id, command, args):
        '''Event handler for messages.'''
        pass

    def __init__(self):
        '''Default constructor.'''
        self._mqttc = False
        self._ca_cert_path = None
        ca_cert_path = os.path.join(os.path.dirname(__file__), 'ca.crt')
        if os.path.exists(ca_cert_path):
            self.tls_set(ca_cert_path)

    def tls_set(self, ca_cert_path):
        '''Set ca_certs for ssl connections. Used only with port=8883.'''
        self._ca_cert_path = ca_cert_path

    def connect(self, device_id, secret_key, host='localhost', port=8883):
        '''Connect to thingface server.'''
        if not device_id:
            ValueError('A device ID is required.')
        if type(device_id) is not str:
            ValueError('A device ID must be a string.')
        self._device_id = device_id
        if not secret_key:
            ValueError('A secret key is required.')
        if type(secret_key) is not str:
            ValueError('A device secret key must be a string.')
        self._secret_key = secret_key
        self._host = host
        self._port = port
        self._mqttc = mqtt.Client(
            device_id,
            clean_session=True
        )
        self._mqttc._thingface = self
        self._mqttc.on_connect = _mqttc_connect_handler
        self._mqttc.on_disconnect = _mqttc_disconnect_handler
        self._mqttc.on_message = _mqttc_message_handler
        # self._mqttc.on_publish = _mqttc_publish_handler
        # self._mqttc.on_subscribe = _mqttc_subscribe_handler
        # self._mqttc.on_unsubscribe = _mqttc_unsubscribe_handler
        # self._mqttc.on_log = _mqttc_log_handler
        if port == 8883:  # ssl
            if self._ca_cert_path:
                self._mqttc.tls_set(self._ca_cert_path)
            self._mqttc.tls_insecure_set(True)
        self._mqttc.username_pw_set(device_id, secret_key)
        self._mqttc.connect(host, port)
        self._mqttc.loop_start()
        sleep(0.4)

    def disconnect(self):
        '''Disconnect from thingface server'''
        if self._mqttc:
            self._mqttc.loop_stop()
            self._mqttc.disconnect()
            self._mqttc = False

    def is_connected(self):
        '''Check current connection state: True == connected'''
        if self._mqttc:
            return True
        return False

    def on_error(self, callback):
        '''Set event handler for error events.'''
        if not callable(callback):
            ValueError('callback must be a function')
        self._error_handler = callback

    def on_connection_state(self, callback):
        '''Set event handler for connection_state events.'''
        if not callable(callback):
            ValueError('callback must be a function')
        self._connection_handler = callback

    def on_command(self, callback, sender_type='+', sender_id='+'):
        '''Set event handler for message events (subscribe) from thingface.'''
        if not callable(callback):
            ValueError('callback must be a function')
        if not self._mqttc:
            ValueError('Client is disconnected')
        _sender_type = '+'
        _sender_id = '+'
        if type(sender_type) is str and re.search('^[ud]{1}', sender_type):
            _sender_type = sender_type
        if type(sender_id) is str and len(sender_id) <= 30:
            _sender_id = sender_id
        self._message_handler = callback
        self._sub_filter = (
            _sender_type + '/c/' + _sender_id + '/' + self._device_id
        )
        # print('topic: %s' % (self._sub_filter,))
        self._mqttc.subscribe(self._sub_filter)

    def send_sensor_value(self, sensor_id, sensor_value):
        '''Send value (publish) to thingface server.'''
        if not self._mqttc:
            ValueError('client is disconnected')
        if type(sensor_id) is not str:
            ValueError('sensor ID must be a string')
        if len(sensor_id) > 25:
            ValueError('sensor ID is too long')
        if not isinstance(sensor_value, (int, long, float)):  # noqa: E821
            ValueError('sensor value must be a number')
        message = json.dumps({'v': sensor_value})
        self._mqttc.publish(
            'd/d/' + self._device_id + '/' + sensor_id,
            message
        )
