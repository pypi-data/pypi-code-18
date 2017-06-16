import RPi.GPIO as gpio
import time, math, timeit
from Adafruit_CharLCD import Adafruit_CharLCD as LCD
class AnyElement(object):
    def __init__(self, *args, **kwargs):
        # gpio.setmode(gpio.BOARD)
        # gpio.setwarnings(False)
        pass
class RCAnalog(AnyElement):
    def __init__(self, *args, **kwargs):
        super(RCAnalog, self).__init__()
        if "pin" in kwargs:
            self.pin = kwargs["pin"]
            gpio.setup(self.pin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
            if "drain" in kwargs:
                self.drain = kwargs["drain"]
            else:
                # cases where we are NOT using the opamp
                # we can directly discharge the capacitor
                self.drain = self.pin
        if "kohms" in kwargs:
            self.kohms = kwargs["kohms"]
        if "uF" in kwargs:
            self.uF = kwargs["uF"]
        if "voltrange" in kwargs:
            self.voltrange = kwargs["voltrange"]
        if "opamp_gain" in kwargs:
            self.opamp_gain = kwargs["opamp_gain"]
        self.e =2.71828
        self.gpio_lowest_high =1.34
        self.rc = self.kohms*self.uF/1000000
        self.discharge_time =self.rc*4000 # this is time when we expect98% of the capacitor to be charged or discharged
    def discharge_capc(self, *args, **kwargs):
        """
        Here we drain the capacitor unit
        works for both the drain pin being distinct and the same
        """
        gpio.setup(self.drain, gpio.OUT)
        time.sleep(0.0008) #so that the pin function is assimilated
        gpio.output(self.drain,gpio.LOW)
        time.sleep(self.discharge_time)
    def charge_capc(self):
        def until_pin_up():
            t0=time.clock()
            while gpio.input(self.pin)==0:
                if time.clock()-t0 >3.0:
                    break
                continue
            return
        gpio.setup(self.pin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.drain, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        elapsed=timeit.timeit(until_pin_up, number=1)
        # this would need obvious correction since this is CPU time
        # this is by no means the pure capc charging time.s
        if elapsed >=3.0:
            raise IOError("Waited too long for the capacitor to charge. is it even connected ?")
        actual_time = elapsed/8753.13592
        return actual_time

    def clip_range(self, value):
        if len(self.voltrange)==0:
            return value
        else:
            if value > self.voltrange[1]:
                return self.voltrange[1]
            elif value < self.voltrange[0]:
                return self.voltrange[0]
            else:
                return value
    def plot_on_range(self, value):
        # here we assume that the voltrange is always the ascending values
        if len(self.voltrange)>0:
            return round((value -self.voltrange[0]) /(self.voltrange[1]-self.voltrange[0]), 4)
        else:
            return value
    def measure_supply(self, *args,**kwargs):
        """
        parameter       : description                       : defaults
        accuracy       : digits after decimal - rounding   : 2
        """
        self.discharge_capc() #this woudl also hold the capc at discharged state
        try:
            charge_time = self.charge_capc()
        except IOError as ioe:
            # this is when it has taken too long to measure the charging of the capc
            # this happens when the capc is either not charged at all otr for that matter capc charged to a voltage less than 1.34
            # in any of these cases it would not be able to register a high on the GPIO pin
            return self.gpio_lowest_high
        if charge_time >0:
            time_factor = charge_time/float(self.rc)
            if time_factor >0.0:
                supply=self.gpio_lowest_high/(1-(math.pow(self.e,float(-time_factor))))
                # supply=self.clip_range(supply)
                if "accuracy" in kwargs:
                    return round(supply, kwargs["accuracy"])
                # incase the accuracy is not provided then rounding off takes place for 2 digits aftr decimal
                return round(supply,2)
            else:
                # this is a rare exception and almost otherwise you will not see this happening
                raise Exception("Time calculations indicates negative charge time, please check the connections again")
class Relay(AnyElement):
    def __init__(self, *args, **kwargs):
        super(Relay, self).__init__()
        if "pin" in kwargs and isinstance(kwargs["pin"], int) ==True:
            self.pin =kwargs["pin"]
            gpio.setup(self.pin, gpio.OUT)
            gpio.output(self.pin, gpio.LOW)
    def fire(self, *args, **kwargs):
        if self.pin is not None:
            gpio.output(self.pin,gpio.HIGH)
    def recoil(self, *args, **kwargs):
        if self.pin is not None:
            gpio.output(self.pin,gpio.LOW)
    def state(self):
        # this just lets us know if the relay is in fired or recoiled state
        return (0,1)[gpio.input(self.pin)==gpio.HIGH]
class PushButton(AnyElement):
    def __init__(self, *args, **kwargs):
        super(PushButton, self).__init__()
        if "pin" in kwargs and isinstance(kwargs["pin"], int) ==True:
            self.pin =kwargs["pin"]
            if "pull" in kwargs:
                self.pull =kwargs["pull"]
                if self.pull ==0:
                    gpio.setup(self.pin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
                else:
                    gpio.setup(self.pin, gpio.IN, pull_up_down=gpio.PUD_UP)

    def await_press(self, *args, **kwargs):
        """This routine would return only when the button is pressed. Till then its a synchronous operation.
        """
        if self.pin is not None and self.pull is not None:
            trigger = (gpio.LOW, gpio.HIGH)[self.pull==0]
            while gpio.input(self.pin) != trigger:
                time.sleep(1)
                continue
            return True
    def is_pressed(self, *args, **kwargs):
        """
        this runs one time to see if the button is pressed
        """
        if self.pin is not None and self.pull is not None:
            trigger = (gpio.LOW, gpio.HIGH)[self.pull==0]
            if  gpio.input(self.pin) != trigger:
                return False
            else:
                return True
class LightDiode(AnyElement):
    """
    pin         : is the pin at which you have physically connected the led to the GPIO
    """
    def __init__(self, *args, **kwargs):
        # so that defaults on the GPIO board are started
        super(LightDiode, self ).__init__()
        if "pin" in kwargs and isinstance(kwargs["pin"], int) ==True:
            self.pin =kwargs["pin"]
            # initially the led would be turnedoff..
            gpio.setup(self.pin, gpio.OUT)
            gpio.output(self.pin,gpio.LOW)
    def state(self, *args, **kwargs):
        return (0,1)[gpio.input(self.pin)==gpio.HIGH]
    def on(self, *args, **kwargs):
        if self.pin is not None:
            gpio.output(self.pin,gpio.HIGH)
            return True
        else:
            Exception("Pin for the LED is not saved")
    def off(self, *args, **kwargs):
        if self.pin is not None:
            gpio.output(self.pin,gpio.LOW)
            return True
        else:
            Exception("Pin for the LED is not saved")
    def blink(self, *args, **kwargs):
        # incase the blinks ot

        if self.pin is not None:
            if "blinks" in kwargs:
                if "rate" in kwargs :
                    rate=(0.5,kwargs["rate"])[kwargs["rate"]>0]
                    for b in range(kwargs["blinks"]):
                        self.on()
                        time.sleep(rate)
                        self.off()
                        time.sleep(rate)
                else:
                    # rate is not specified
                    self.on()
            else:
                self.on()
        else:
            raise Exception("Pin for the LED is not saved")
class FruitLCD(AnyElement):
    def __init__(self, *args, **kwargs):
        """
        refer       : https://www.quinapalus.com/hd44780udg.html
        refer       : https://github.com/adafruit/Adafruit_Python_CharLCD/blob/master/Adafruit_CharLCD/Adafruit_CharLCD.py#L284
        """
        self.lcd=LCD(rs=14, en=15, d4=12, d5=16, d6=20, d7=21, cols=16, lines=2)
        # these are the custom defined patterns that we wan to print on the screen
        # from the documentation we can have about 8 patterns stored on locations 0-7 by using lcd.set_char()
        # subsequently we can display the same characters by lcd.message('\x0<location>')
        twinbar_pattern=(0x0,0x1b,0x1b,0x1b,0x1b,0x1b,0x0,0x0)
        nolight_pattern=(0x0,0x0,0xe,0xe,0xe,0x0,0x0,0x0)
        fulllight_pattern=(0x0,0xe,0x1f,0x1f,0x1f,0xe,0x0,0x0)
        heart_pattern=(0x0,0x0,0xa,0x1f,0x1f,0xe,0x4,0x0)
        uparrow_pattern=(0x0,0x0,0x4,0xe,0x1f,0x0,0x0,0x0)
        downarrow_pattern=(0x0,0x0,0x1f,0xe,0x4,0x0,0x0,0x0)
        rightarrow_pattern=(0x0,0x8,0xc,0xe,0xc,0x8,0x0,0x0)
        degcelcius_pattern=(0x18,0x18,0x3,0x4,0x4,0x4,0x3,0x0)
        # smileface_pattern=(0x0,0x0,0xa,0x0,0x11,0xe,0x0,0x0)
        # sadface_pattern=(0x0,0x0,0xa,0x0,0xe,0x11,0x0,0x0)
        # musicnote_pattern=(0x2,0x3,0x2,0x2,0xe,0x1e,0xc,0x0)
        patterns=[heart_pattern, uparrow_pattern, downarrow_pattern, rightarrow_pattern,degcelcius_pattern,twinbar_pattern,nolight_pattern,fulllight_pattern]
        for idx ,p, in enumerate(patterns):
            self.lcd.create_char(location=idx, pattern=p)
    def disp_message(self, message):
        self.lcd.clear()
        self.lcd.message(message)
    def blink_message(self, message, blink_secs=2):
        self.disp_message(message=message)
        time.sleep(blink_secs)
        self.lcd.clear()
    def marquee_message(self, message, left_to_right=True):
        pos=0
        self.lcd.clear()
        self.lcd.message(message)
        while pos <=15:
            pos+=1
            if left_to_right ==True:
                self.lcd.move_right()
            else:
                self.lcd.move_left()
            time.sleep(0.2)
        self.lcd.clear()
        self.lcd.message(message)
    def threshold_emoticon(self,thresh_cent=0.5, value_cent=0.5):
        """
        *-----I----O        : header
        ---I--------        : graph
        is what we are trying to show here on the lcd screen
        thresh_cent         : this is value indication on the header
        value_cent          : actual value on the graph
        parameter values if supplied outside the 0-1.0 range would be normalized
        """
        if thresh_cent < 0.0:
             thresh_cent =0.0
        elif thresh_cent >1.0:
             thresh_cent =1.0
        if value_cent <0.0:
            value_cent =0.0
        elif value_cent >1.0:
            value_cent =1.0
        self.lcd.clear()
        header="\x06"+"-"*13+"\x07"
        # now fit the threshold symbolin the header
        pos=int(thresh_cent*16)
        header =header[0:pos]+"\x00"+header[pos:16]
        self.lcd.set_cursor(0,0)
        self.lcd.message(header)
        graph="-"*15
        pos=int(value_cent*16)
        graph=graph[0:pos]+"\x05"+graph[pos:16]
        self.lcd.set_cursor(0,1)
        self.lcd.message(graph)
        return
    def clean(self):
        self.lcd.clear()
