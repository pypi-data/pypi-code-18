__version__ = '0.0.1'

from pythonwhat.check_syntax import state_dec, Ex
import numpy as np

@state_dec
def check_numpy_array(name, state = None):
    # is defined
    obj = Ex(state).check_object(name)

    # is a numpy array
    obj.is_instance(np.ndarray)

    # same shape
    obj.has_equal_value(expr_code = '{:s}.shape'.format(name))

    # equal contents
    obj.has_equal_value()

    # return object state for chaining
    return obj
