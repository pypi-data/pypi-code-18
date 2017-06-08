__all__ = ['Notifier']

# #############################################################################
# ########## Libraries #############
# ##################################
# standard library
from ctypes import *

# 3rd party module
from win10toast import ToastNotifier

# ############################################################################
# ########### Classes ##############
# ##################################
class PowerClass(Structure):
    """Defining Field Strings for Power Class"""
    _fields_ = [('ACLineStatus', c_byte),
                ('BatteryFlag', c_byte),
                ('BatteryLifePercent', c_byte),
                ('Reserved1', c_byte),
                ('BatteryLifeTime', c_ulong),
                ('BatteryFullLifeTime', c_ulong)]

class Notifier():
    @staticmethod
    def get_battery_level():
        """Extends PowerClass and returns Battery Level"""
        powerclass = PowerClass()
        windll.kernel32.GetSystemPowerStatus(byref(powerclass))
        return powerclass.BatteryLifePercent

    @staticmethod
    def get_battery_line():
        """Extends PowerClass and returns Battery AC Line Status"""
        powerclass = PowerClass()
        windll.kernel32.GetSystemPowerStatus(byref(powerclass))
        return powerclass.ACLineStatus

    @staticmethod
    def create_plug_out_toast():
        """Throws PlugOut Toast for 10 seconds"""
        toaster = ToastNotifier()
        toaster.show_toast("Battery Charged",
                "To maintain the optimal  battery life,kindly unplug the charger now!!",
                duration=10)
        return None

    @staticmethod
    def create_plug_in_toast():
        """Throws PlugIn Toast for 10 seconds"""
        toaster = ToastNotifier()
        toaster.show_toast("Low Battery",
                "To maintain the optimal battery life,kindly plug in the charger now!!",
                duration=10)
        return None
