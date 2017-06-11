from collections import namedtuple

class Scale:
    """
    Base class for all scaling data types. These types can store a value, modify it via some scaling function,
    and then keep the new value.

    Args:
        min_val     (float): minimum value that the scaled value is allowed to take
        max_val     (float): maximum value that the scaled value is allowed to take
        begin_scale (float): starting value of the value to be scaled
    """
    __slots__ = ["min_val", "max_val", "begin_scale"]

    def __init__(self, min_val, max_val, begin_scale):
        self.min_val = min_val
        self.max_val = max_val
        self.begin_scale = begin_scale
        if begin_scale == None:
            self.begin_scale = max_val
        else:
            self.begin_scale = begin_scale

    def new_scale_deriv(self, **kwargs):
        """
        This method must be overridden by derived classes
        """
        pass

    def new_scale(self, count=1):
        """
        The scaling by derived classes is to be done only via this value
        """
        self.new_scale_deriv(count=count)
        self.begin_scale = min(max(self.min_val, self.begin_scale), self.max_val)
        return self.begin_scale

class LinearScale(Scale):
    """
    Type for scaling a given value linearly
    """
    __slots__ = ["incr"]

    def __init__(self, min_val, max_val, incr, begin_scale=None):
        self.incr = incr
        super().__init__(min_val, max_val, begin_scale)

    def new_scale_deriv(self, count=1):
        for i in range(count):
            self.begin_scale += self.incr
        return self.begin_scale

    def get_curr_scale(self):
        return self.begin_scale

    def set_incr(self, new_incr):
        self.incr = new_incr

class MultScale(Scale):
    """
    Type for scaling a given value via multiplication
    """
    __slots__ = ["incr"]

    def __init__(self, min_val, max_val, incr, begin_scale=None):
        self.incr = incr
        super().__init__(min_val, max_val, begin_scale)

    def new_scale_deriv(self, count=1):
        for i in range(count):
            self.begin_scale *= self.incr
        return self.begin_scale

    def get_curr_scale(self):
        return self.begin_scale

    def set_incr(self, new_incr):
        self.incr = new_incr

ScalingStruct = namedtuple("ScalingStruct", ["min_val", "max_val", "incr", "begin_scale", "cls"])
