# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.


from random import randint
from thingface import Client


def connection_handler(connected):
    print('connection status %d' % (connected,))


def error_handler(error):
    print('error: %s' % (error,))


def command_handler(sender_type, sender_id, command, args):
    print(
        'command handler, sender_type:%s, sender_id:%s, command:%s, args:%s' %
        (sender_type, sender_id, command, args)
    )


def generate_temp():
    return randint(180, 390) / 10.0


if __name__ == '__main__':
    client = Client()
    client.on_error(error_handler)
    client.on_connection_state(connection_handler)
    client.connect(
        'device ID',
        'device secret key',
        'host'
    )
    client.on_command(command_handler)
    temp = generate_temp()
    client.send_sensor_value('temp101', temp)
    client.disconnect()
    print('Temp: %f' % (temp,))
