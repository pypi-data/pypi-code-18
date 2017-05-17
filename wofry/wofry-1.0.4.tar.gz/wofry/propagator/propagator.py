###################################################################
# DO NOT TOUCH THIS CODE -- BEGIN
###################################################################
import threading

def synchronized_method(method):

    outer_lock = threading.Lock()
    lock_name = "__"+method.__name__+"_lock"+"__"

    def sync_method(self, *args, **kws):
        with outer_lock:
            if not hasattr(self, lock_name): setattr(self, lock_name, threading.Lock())
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

    return sync_method

class Singleton:

    def __init__(self, decorated):
        self._decorated = decorated

    @synchronized_method
    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

###################################################################
# DO NOT TOUCH THIS CODE -- END
###################################################################


from syned.beamline.beamline_element import BeamlineElement

from wofry.propagator.wavefront  import Wavefront, WavefrontDimension
from wofry.propagator.wavefront1D.generic_wavefront import GenericWavefront1D
from wofry.propagator.wavefront2D.generic_wavefront import GenericWavefront2D

class PropagationElements(object):
    def __init__(self):
        self.__propagation_elements = []

    def add_beamline_element(self, beamline_element=BeamlineElement()):
        if beamline_element is None: raise ValueError("Beamline is None")

        self.__propagation_elements.append(beamline_element)

    def add_beamline_elements(self, beamline_elements=[]):
        if beamline_elements is None: raise ValueError("Beamline is None")

        for beamline_element in beamline_elements:
            self.add_beamline_element(beamline_element)

    def get_propagation_elements_number(self):
        return len(self.__propagation_elements)

    def get_propagation_elements(self):
        return self.__propagation_elements

    def get_propagation_element(self, index):
        return self.__propagation_elements[index]

class PropagationParameters(object):
    def __init__(self,
                 wavefront = Wavefront(),
                 propagation_elements = PropagationElements()):
        self._wavefront = wavefront
        self._propagation_elements = propagation_elements
        self._additional_parameters = None

    def get_wavefront(self):
        return self._wavefront

    def get_PropagationElements(self):
        return self._propagation_elements

    def set_additional_parameters(self, key, value):
        if self._additional_parameters is None:
            self._additional_parameters = {key : value}
        else:
            self._additional_parameters[key] = value

    def get_additional_parameter(self, key):
        return self._additional_parameters[key]

    def has_additional_parameter(self, key):
        return key in self._additional_parameters

class AbstractPropagator(object):

    def __init__(self):
        super().__init__()

    def get_dimension(self):
        raise NotImplementedError("This method is abstract")

    def get_handler_name(self):
        raise NotImplementedError("This method is abstract")

    def is_handler(self, handler_name):
        return handler_name == self.get_handler_name()

    def do_propagation(self, parameters=PropagationParameters()):
        raise NotImplementedError("This method is abstract" +
                                  "\n\naccepts " + PropagationParameters.__module__ + "." + PropagationParameters.__name__ +
                                  "\nreturns " + Wavefront.__module__ + "." + Wavefront.__name__)


@Singleton
class PropagationManager(object):

    def __init__(self):
        self.__chains_hashmap = {WavefrontDimension.ONE : [],
                                 WavefrontDimension.TWO : []}

    @synchronized_method
    def add_propagator(self, propagator=AbstractPropagator()):
        if propagator is None: raise ValueError("Given propagator is None")
        if not isinstance(propagator, AbstractPropagator): raise ValueError("Given propagator is not a compatible object")

        dimension = propagator.get_dimension()

        print(dimension)

        if not (dimension == WavefrontDimension.ONE or dimension == WavefrontDimension.TWO):
            raise ValueError("Wrong propagator dimension")

        propagation_chain_of_responsibility = self.__chains_hashmap.get(dimension)

        for existing in propagation_chain_of_responsibility:
            if existing.is_handler(propagator.get_handler_name()):
                raise ValueError("Propagator already in the Chain")

        propagation_chain_of_responsibility.append(propagator)

    def do_propagation(self, propagation_parameters, handler_name):
        for propagator in self.__chains_hashmap.get(propagation_parameters.get_wavefront().get_dimension()):
            if propagator.is_handler(handler_name):
                return propagator.do_propagation(parameters=propagation_parameters)

        raise Exception("Handler not found")

# ---------------------------------------------------------------

class Propagator(AbstractPropagator):

    def do_propagation(self, parameters=PropagationParameters()):
        wavefront = parameters.get_wavefront()

        for element in parameters.get_PropagationElements().get_propagation_elements():
            coordinates = element.get_coordinates()

            if coordinates.p() != 0.0: wavefront = self.do_specific_progation(wavefront, coordinates.p(), parameters)
            wavefront = element.get_optical_element().applyOpticalElement(wavefront)
            if coordinates.q() != 0.0: wavefront = self.do_specific_progation(wavefront, coordinates.q(), parameters)

        return wavefront

    def do_specific_progation(self, wavefront, propagation_distance, parameters):
        raise NotImplementedError("This method is abstract")


class Propagator1D(Propagator):

    def get_dimension(self):
        return WavefrontDimension.ONE

    def do_propagation(self, parameters=PropagationParameters()):
        if not isinstance(parameters.get_wavefront(), GenericWavefront1D):
            raise Exception("wrong wavefront!  it is not" + GenericWavefront1D.__name__)

        return super().do_propagation(parameters)

class Propagator2D(Propagator):

    def get_dimension(self):
        return WavefrontDimension.TWO

    def do_propagation(self, parameters=PropagationParameters()):
        if not isinstance(parameters.get_wavefront(), GenericWavefront2D):
            raise Exception("wrong wavefront!  it is not" + GenericWavefront2D.__name__)

        return super().do_propagation(parameters)

