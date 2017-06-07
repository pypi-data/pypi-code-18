
import time
from .baro import Barometer
from .temperature import TemperatureSensor
from .imu import Accelerometer, Magnetometer, Gyroscope
from .rgb_ir import RgbIrSensor
from .uva import UvaSensor
from .rtc import RealTimeClock
from .leds import Leds
from .arducam import Camera

barometer = Barometer(None, 0x76)
bottom_thermometer = TemperatureSensor(None, 0x48)
top_thermometer = TemperatureSensor(None, 0x49)
accelerometer = Accelerometer(None, 0x1D)
magnetometer = Magnetometer(None, 0x1D)
gyroscope = Gyroscope(None, 0x6b)
rgb_ir_sensor = RgbIrSensor(None, 0x52)
uva_sensor = UvaSensor(None, 0x38)
real_time_clock = RealTimeClock(None, 0x51)

sensors = [
    barometer,
    bottom_thermometer,
    top_thermometer,
    accelerometer,
    gyroscope,
    rgb_ir_sensor,
    uva_sensor,
    real_time_clock
]

for sensor in sensors:
    sensor.configure({})

leds = Leds()
camera = Camera()


__all__ = (
    'barometer',
    'bottom_thermometer',
    'top_thermometer',
    'accelerometer',
    'gyroscope',
    'magnetometer',
    'rgb_ir_sensor',
    'uva_sensor',
    'real_time_clock',
    'leds',
    'camera'
)


def test():
    print("RUNNING TEST...")
    try:

        print(barometer.measure())
        print(bottom_thermometer.measure())
        print(top_thermometer.measure())
        print(accelerometer.measure())
        print(rgb_ir_sensor.measure())
        print(uva_sensor.measure())
        print(real_time_clock.measure())
        leds.set_blue("off")
        leds.set_green("off")
        leds.set_red("off")
        leds.set_led1("off")
        leds.set_led2("off")
        time.sleep(0.25)
        leds.set_led1("on")
        time.sleep(0.25)
        leds.set_led1("off")
        leds.set_led2("on")
        time.sleep(0.25)
        leds.set_led2("off")
        leds.set_red("on")
        time.sleep(0.25)
        leds.set_red("off")
        leds.set_green("on")
        time.sleep(0.25)
        leds.set_green("off")
        leds.set_blue("on")
        time.sleep(0.25)
        leds.set_blue("off")
    except:
        print("ERROR")
        return
    print("PASS")






