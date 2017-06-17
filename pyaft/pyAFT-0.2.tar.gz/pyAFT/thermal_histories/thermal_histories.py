import numpy as np

class Thermal_history(object):
    """Class defining a thermal history"""

    def __init__(self, name, time, temperature):
        if len(time) != len(temperature):
            raise "Not the same length"
        self.name = name
        self.time = time
        self.Temperature = temperature
        self.maxT = max(temperature)
        self.minT = min(temperature)
        self.totaltime = max(time) - min(time)
        self.rate = np.diff(self.Temperature) / np.diff(self.time)

    def time_bp(self):
        self.time = abs(self.time - max(self.time))
        self.time.reverse()

wolf1 = Thermal_history("wolf1", [0., 43., 44., 100.],
                        [10., 10., 130., 130.])
wolf2 = Thermal_history("wolf2", [0., 100.], [10., 130])
wolf3 = Thermal_history("wolf3", [0., 19.5, 19., 100.],
                        [10., 10., 60., 60.])
wolf4 = Thermal_history("wolf4", [0., 24., 76., 100.],
                        [10., 60., 60., 100])
wolf5 = Thermal_history("wolf5", [0., 5., 100.], [10., 64., 18.])
