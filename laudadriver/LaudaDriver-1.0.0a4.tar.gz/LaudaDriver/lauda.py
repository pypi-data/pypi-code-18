# A small wrapper  / driver / helper to control the Lauda Eco Silver thermostat
# Usage is quite obvious

# Based on Lauda Eco Silver documentation to be found at:
# http://www.lauda-brinkmann.com/downloads/manuals/Eco%20Silver.pdf
# section 8.6, page 61

# Dr Jerzy Dziewierz, Dr Vaclav Svoboda, Dr Andrew Dunn,
# University of Strathclyde 2017

import serial
import time
from enum import Enum


class PumpingSpeed(Enum):
    a_Sedated = 1
    a_Low = 2
    a_Boring = 3
    a_Typical = 4
    a_Nice = 5
    a_Mighty = 6


# TODO: enable selecting a non-default COM port, or even searching for COM ports
ThisLAUDA = serial.Serial('COM9')


def open_com_port():
    """Shortcut to the internal port open.
    Should not normally be needed as the underlying library opens automatically"""
    ThisLAUDA.open()
    ThisLAUDA.read_all()


def close():
    """Shortcut to force the port close
    might be useful when debugging or sharing with external tools
    normally there should be no need to call it as python takes care of it when shutting down
    """
    ThisLAUDA.read_all()
    ThisLAUDA.close()


def set_pumping_speed(new_speed: PumpingSpeed = PumpingSpeed.a_Mighty):
    """Set the pumping speed
    use .PumpingSpeed class as enum
    note that this will not automatically enable the thermostat if it is not separately enabled.
    """
    ThisLAUDA.read_all()
    ThisLAUDA.write(bytes('OUT_SP_01_{:03d}\r\n'.format(new_speed.value), encoding='utf-8', errors='strict'))


def set_temp(new_temp: float = 20.0):
    """Set the set-point temperature for the thermostat to try to achieve.
    note that this will not automatically enable the thermostat if it is not separately enabled.
    """
    ThisLAUDA.read_all()
    ThisLAUDA.write(bytes('OUT_SP_00_{:06.2f}\r\n'.format(new_temp), encoding='utf-8', errors='strict'))


def read_current_temp():
    """ reads the temperature of the channel that routes the currently active control sensor
    Meaning that e.g. external PT100 is connected and configured in the menu, it will use that, 
    otherwise defaults to whatever temperature sensor it can find
    """
    ThisLAUDA.read_all()
    ThisLAUDA.write(b'IN_PV_01\r\n')
    # TODO: Convert from arbitrary time wait to verifying that there is a response
    # using ThisLauda.bytes_available or something similar
    time.sleep(0.3)  # wait for Lauda to have some time to respond.
    txt = ThisLAUDA.read_all()
    val = float(txt)
    return val


def start():
    """Wakes up the thermostat from standby mode - enables pump and heater/chiller module"""
    ThisLAUDA.read_all()
    ThisLAUDA.write(b'START\r\n')


def stop():
    """Puts the Thermostat into standby (idle) mode - stops the pumps"""
    ThisLAUDA.read_all()
    ThisLAUDA.write(b'STOP\r\n')

# =============
# That's all folks!
