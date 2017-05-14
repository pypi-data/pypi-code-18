#!/usr/bin/env python
# Years till 100
import sys
import optparse
import time
from arjuno.libs import name,version
from arjuno.libs.telebot import main,main_tele
from arjuno.libs.check_serial import serial_ports

def bin():
    parser = optparse.OptionParser()

    parser.add_option('-v', '--version', dest='version', help='version SDK serial',action='store_true')
    parser.add_option('-a', '--available', dest='check_serial', help='check available serial port',action='store_true')
    parser.add_option('-r', '--read', dest='read_serial', help='read data input in serial',action='store_true')
    parser.add_option('-s', '--serialport', dest='serial_port', help='open serial with port')
    parser.add_option('-b', '--baudrate', dest='baudrate', help='baudrate serial port')
    parser.add_option('--run', dest='run', help='run serial over socket',action='store_true')
    parser.add_option('--host', dest='host', help='host socket available',default='localhost:3000')
    parser.add_option('--telegram', dest='telegram', help='run sdk with telegram api',action='store_true')
    parser.add_option('--delay',dest='delay',help='give delay command',default=2)

    (options, args) = parser.parse_args()  

    # if options:
    #     print "please input command example {name} -h".format(name=name())
    if options.version:
        print version

    elif options.check_serial:
        print serial_ports()

    elif options.read_serial:
        if options.serial_port and options.baudrate:
            print main(options.serial_port,options.baudrate)
        else:
            print "please import baudrate and serial port"

    elif options.run:
        print options.host
        #print options.serialport
        while True:
            print "websocket running....."
            time.sleep(1)

    elif options.telegram:

        serial_port = options.serial_port
        baudrate = options.baudrate

        if serial_port and baudrate:
            while True:
                try:
                    # data = main(port=serial_port,baudrate=baudrate)
                    # data = data.split("|")
                    main_tele(port=serial_port,baudrate=baudrate)
                    time.sleep(int(options.delay))
                except Exception as e:
                    print e

        else:
            print "Please insert baudrate and serial port"
