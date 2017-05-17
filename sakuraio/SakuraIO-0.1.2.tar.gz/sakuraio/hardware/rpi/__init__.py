from sakuraio.hardware.base import SAKURAIO_SLAVE_ADDR, SakuraIOBase


class SakuraIOSMBus(SakuraIOBase):

    def __init__(self):
        import smbus
        self.bus = smbus.SMBus(1)

    def start(self, write=True):
        if write:
            self.request = []
            self.response = []
        else:
            if self.request:
                self.bus.write_i2c_block_data(SAKURAIO_SLAVE_ADDR, self.request[0], self.request[1:])
            self.response = self.bus.read_i2c_block_data(SAKURAIO_SLAVE_ADDR, 32)

    def send_byte(self, value):
        self.request.append(value)

    def recv_byte(self):
        value = 0x00
        if self.response:
            value = self.response.pop(0)
        return value


class SakuraIOGPIO(SakuraIOBase):

    def __init__(self, miso=9, mosi=10, clk=11, cs=8):
        from RPi import GPIO
        self.GPIO = GPIO
        self.miso = miso
        self.mosi = mosi
        self.clk = clk
        self.cs = cs
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.miso, GPIO.IN)
        GPIO.setup(self.mosi, GPIO.OUT)
        GPIO.setup(self.clk, GPIO.OUT)
        GPIO.setup(self.cs, GPIO.OUT)

        self.GPIO.output(self.cs, self.GPIO.HIGH)
        self.GPIO.output(self.clk, self.GPIO.LOW)

    def start(self, write=True):
        self.GPIO.output(self.cs, self.GPIO.LOW)

    def end(self):
        self.GPIO.output(self.cs, self.GPIO.HIGH)

    def send_byte(self, value):
        ret = 0x00
        for bit in range(8):

            if value & 0x80:
                self.GPIO.output(self.mosi, self.GPIO.HIGH)
            else:
                self.GPIO.output(self.mosi, self.GPIO.LOW)

            self.GPIO.output(self.clk, self.GPIO.HIGH)

            ret <<= 1
            if self.GPIO.input(self.miso):
                ret |= 0x01

            self.GPIO.output(self.clk, self.GPIO.LOW)

            value <<= 1

        return ret

    def recv_byte(self):
        return self.send_byte(0x00)


class SakuraIOSPI(SakuraIOBase):
    def __init__(self):
        raise NotImplementedError()
