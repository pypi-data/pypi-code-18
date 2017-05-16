r"""Implements all of the Libaudioverse API.

This is the only module that should be used.  All other modules are private."""
from __future__ import absolute_import
from . import _lav
from . import _libaudioverse
import weakref
import collections
import ctypes
import enum
import functools
import threading
import logging
import six.moves
import glob
import os.path
import numbers
import math
import operator
import contextlib

def find_datafiles():
    import platform
    if platform.system() != 'Windows':
        return []
    dlls = glob.glob(os.path.join(__path__[0], '*.dll'))
    return [('libaudioverse', dlls)]


#Everything below here might need the important enums, namely Lav_OBJECT_TYPES:
class BiquadTypes(enum.IntEnum):
    """Indicates a biquad filter type, used with the :class:`BiquadNode` and in a few other places."""
    allpass = 4
    """Indicates an allpass filter."""
    bandpass = 2
    """Indicates a bandpass filter."""
    highpass = 1
    """Indicates a highpass filter."""
    highshelf = 7
    """Indicates a highshelf filter."""
    identity = 8
    """This filter does nothing."""
    lowpass = 0
    """Indicates a lowpass filter."""
    lowshelf = 6
    """Indicates a lowshelf filter."""
    notch = 3
    """Indicates a notch filter."""
    peaking = 5
    """Indicates a peaking filter."""
class BiquadTypes(enum.IntEnum):
    """Indicates a biquad filter type, used with the :class:`BiquadNode` and in a few other places."""
    allpass = 4
    """Indicates an allpass filter."""
    bandpass = 2
    """Indicates a bandpass filter."""
    highpass = 1
    """Indicates a highpass filter."""
    highshelf = 7
    """Indicates a highshelf filter."""
    identity = 8
    """This filter does nothing."""
    lowpass = 0
    """Indicates a lowpass filter."""
    lowshelf = 6
    """Indicates a lowshelf filter."""
    notch = 3
    """Indicates a notch filter."""
    peaking = 5
    """Indicates a peaking filter."""
class ChannelInterpretations(enum.IntEnum):
    """Specifies how to treat inputs to this node for upmixing and downmixing."""
    discrete = 0
    """If channel counts mismatch, don't apply mixing matrices. Either drop or fill with zeros as appropriate."""
    speakers = 1
    """Apply mixing matrices if needed."""
class DistanceModels(enum.IntEnum):
    """used in the 3D components of this library.
Indicates how sound should become quieter as objects move away from the listener.

Libaudioverse computes the distance from the center of the source to the listener, then subtracts the size.
In the following, ``distance`` refers to this distance.
Libaudioverse also computes a second value called ``distancePercent``; specifically, ``distancePercent = distance/maxDistance``."""
    inverse = 1
    """Sounds fall off as ``1/(1+315*distancePercent)``.  Just before ``maxDistance``, the gain of the sound will be approximately -25 DB.  This distance model emphasizes distance changes when sounds are close, but treats distance changes of further away sources more subtly.  For full benefit of the effect of close sounds, this distance model must be used with fairly large values for ``maxDistance``, usually around 300."""
    inverse_square = 2
    """Sounds fall off as ``1.0/(1+315*distancePercent*distancePercent)``.  This is a standard inverse square law, modified such that the sound volume just before ``maxDistance`` is about -25 DB.  Of the available distance models, this is the closest to an accurate simulation of large, wide-open places such as fields and stadiums."""
    linear = 0
    """Sound falls off as ``1-distancePercent``."""
class DistanceModels(enum.IntEnum):
    """used in the 3D components of this library.
Indicates how sound should become quieter as objects move away from the listener.

Libaudioverse computes the distance from the center of the source to the listener, then subtracts the size.
In the following, ``distance`` refers to this distance.
Libaudioverse also computes a second value called ``distancePercent``; specifically, ``distancePercent = distance/maxDistance``."""
    inverse = 1
    """Sounds fall off as ``1/(1+315*distancePercent)``.  Just before ``maxDistance``, the gain of the sound will be approximately -25 DB.  This distance model emphasizes distance changes when sounds are close, but treats distance changes of further away sources more subtly.  For full benefit of the effect of close sounds, this distance model must be used with fairly large values for ``maxDistance``, usually around 300."""
    inverse_square = 2
    """Sounds fall off as ``1.0/(1+315*distancePercent*distancePercent)``.  This is a standard inverse square law, modified such that the sound volume just before ``maxDistance`` is about -25 DB.  Of the available distance models, this is the closest to an accurate simulation of large, wide-open places such as fields and stadiums."""
    linear = 0
    """Sound falls off as ``1-distancePercent``."""
class FdnFilterTypes(enum.IntEnum):
    """Possible filter types for a feedback delay network's feedback path."""
    disabled = 0
    """Don't insert filters on the feedback path."""
    highpass = 2
    """Insert highpass filters on the FDN's feedback path."""
    lowpass = 1
    """Insert lowpass filters on the FDN's feedback path."""
class LoggingLevels(enum.IntEnum):
    """Possible levels for logging."""
    critical = 10
    """Logs critical messages such as failures to initialize and error conditions."""
    debug = 30
    """Logs everything possible."""
    info = 20
    """Logs informative messages."""
    off = 40
    """No log messages will be generated."""
class NodeStates(enum.IntEnum):
    """used to indicate the state of a node.
This is the value of the node's state property and determins how the node is processed."""
    always_playing = 2
    """This node advances always."""
    paused = 0
    """This node is paused."""
    playing = 1
    """This node advances if other nodes need audio from it."""
class NoiseTypes(enum.IntEnum):
    """Specifies types of noise."""
    brown = 2
    """Brown noise.  Brown noise decreases at 6 DB per octave."""
    pink = 1
    """Pink noise.  Pink noise falls off at 3 DB per octave."""
    white = 0
    """gaussian white noise."""
class ObjectTypes(enum.IntEnum):
    
    additive_saw_node = 20
    
    additive_square_node = 18
    
    additive_triangle_node = 19
    
    allpass_node = 36
    
    amplitude_panner_node = 10
    
    biquad_node = 12
    
    blit_node = 38
    
    buffer = 1
    
    buffer_node = 26
    
    buffer_timeline_node = 27
    
    channel_merger_node = 25
    
    channel_splitter_node = 24
    
    convolver_node = 29
    
    crossfader_node = 33
    
    crossfading_delay_node = 8
    
    dc_blocker_node = 39
    
    dopplering_delay_node = 9
    
    environment_node = 3
    
    fdn_reverb_node = 37
    
    feedback_delay_network_node = 17
    
    fft_convolver_node = 30
    
    file_streamer_node = 41
    
    filtered_delay_node = 32
    
    first_order_filter_node = 35
    
    gain_node = 23
    
    generic_node = 2
    
    graph_listener_node = 14
    
    hard_limiter_node = 7
    
    hrtf_node = 5
    
    iir_node = 22
    
    leaky_integrator_node = 40
    
    multipanner_node = 16
    
    noise_node = 21
    
    one_pole_filter_node = 34
    
    pull_node = 13
    
    push_node = 11
    
    recorder_node = 28
    
    ringmod_node = 15
    
    server = 0
    
    sine_node = 6
    
    source_node = 4
    
    three_band_eq_node = 31
    
class PanningStrategies(enum.IntEnum):
    """Indicates a strategy to use for panning.
This is mostly for the :class:`MultipannerNode` and the 3D components of this library."""
    hrtf = 0
    """Indicates HRTF panning."""
    stereo = 1
    """Indicates stereo panning."""
    surround40 = 2
    """Indicates 4.0 surround sound (quadraphonic) panning."""
    surround51 = 3
    """Indicates 5.1 surround sound panning."""
    surround71 = 4
    """Indicates 7.1 surround sound panning."""
class PanningStrategies(enum.IntEnum):
    """Indicates a strategy to use for panning.
This is mostly for the :class:`MultipannerNode` and the 3D components of this library."""
    hrtf = 0
    """Indicates HRTF panning."""
    stereo = 1
    """Indicates stereo panning."""
    surround40 = 2
    """Indicates 4.0 surround sound (quadraphonic) panning."""
    surround51 = 3
    """Indicates 5.1 surround sound panning."""
    surround71 = 4
    """Indicates 7.1 surround sound panning."""
class PanningStrategies(enum.IntEnum):
    """Indicates a strategy to use for panning.
This is mostly for the :class:`MultipannerNode` and the 3D components of this library."""
    hrtf = 0
    """Indicates HRTF panning."""
    stereo = 1
    """Indicates stereo panning."""
    surround40 = 2
    """Indicates 4.0 surround sound (quadraphonic) panning."""
    surround51 = 3
    """Indicates 5.1 surround sound panning."""
    surround71 = 4
    """Indicates 7.1 surround sound panning."""
class PropertyTypes(enum.IntEnum):
    """Indicates the type of a property."""
    buffer = 8
    """Property holds a handle to a buffer."""
    double = 2
    """Property holds a 64-bit double."""
    float = 1
    """Property holds a 32-bit floating point value."""
    float3 = 4
    """Property holds a float3, a vector of 3 floats."""
    float6 = 5
    """Property holds a float6, a vector of 6 floats."""
    float_array = 6
    """Property is an array of floats."""
    int = 0
    """Property holds a 32-bit integer."""
    int_array = 7
    """Property is an array of ints."""
    string = 3
    """Property holds a string."""

#registry of classes to be resurrected if we see a handle and don't already have one.
_types_to_classes = dict()

#Instances that already exist.
_weak_handle_lookup = weakref.WeakValueDictionary()
#Holds a mapping of handles to states.
_object_states = dict()
#This has to be recursive.
#We could be in the middle of an operation that causes resurrection and/or initialization.
#Then the gc collects a _HandleBox, a refcount goes to 0, and we see _handle_destroyed in the same thread.
_object_states_lock = threading.RLock()

#magically resurrect an object from a handle.
def _resurrect(handle):
    obj = _weak_handle_lookup.get(handle, None)
    if obj is None:
        cls = _types_to_classes[ObjectTypes(_lav.handle_get_type(handle))]
        obj = cls.__new__(cls)
        obj.init_with_handle(handle)
    _weak_handle_lookup[handle] = obj
    return obj

#This is the callback for handle destruction.
#This can only be called after both sides have no more references to the object in question.
def _handle_destroyed(handle):
    with _object_states_lock:
        if handle in _object_states:
            #If we gc here and the user is using the server as a context manager, then
            #We block until they finish.
            #If they do anything that needs the lock we're holding, lock inversion.
            #This variable holds the dict until after the function ends.
            #Note that this is an integer, not a _HandleBox
            ensure_gc_later = _object_states[handle]
            del _object_states[handle]

_handle_destroyed_callback=_libaudioverse.LavHandleDestroyedCallback(_handle_destroyed)
_libaudioverse.Lav_setHandleDestroyedCallback(_handle_destroyed_callback)

#build and register all the error classes.
class GenericError(Exception):
    r"""Base for all libaudioverse errors."""

    def __init__(self):
        self.file = _lav.error_get_file()
        self.line = _lav.error_get_line()
        self.message = _lav.error_get_message()
        super(GenericError, self).__init__("{} ({}:{})".format(self.message, self.file, self.line))

class BufferInUseError(GenericError):
    r"""Indicates an attempt to modify a buffer while something is reading its data."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_BUFFER_IN_USE, BufferInUseError)

class CannotConnectToPropertyError(GenericError):
    r"""Attempt to connect a node to a property which cannot be automated."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_CANNOT_CONNECT_TO_PROPERTY, CannotConnectToPropertyError)

class CannotCrossServersError(GenericError):
    r"""An attempt was made to relate two objects from different servers. This could be assigning to buffer properties, connecting nodes, or any other such condition."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_CANNOT_CROSS_SERVERS, CannotCrossServersError)

class CannotInitAudioError(GenericError):
    r"""The audio subsystem could not be initialized."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_CANNOT_INIT_AUDIO, CannotInitAudioError)

class CausesCycleError(GenericError):
    r"""The requested operation would cause a cycle in the graph of nodes that need processing."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_CAUSES_CYCLE, CausesCycleError)

class FileError(GenericError):
    r"""Represents a miscelaneous file error."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_FILE, FileError)

class FileNotFoundError(GenericError):
    r"""Libaudioverse could not find a specified file."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_FILE_NOT_FOUND, FileNotFoundError)

class HrtfInvalidError(GenericError):
    r"""An attempt to use an invalid HRTF database."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_HRTF_INVALID, HrtfInvalidError)

class InternalError(GenericError):
    r"""If you see this error, it's a bug."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_INTERNAL, InternalError)

class InvalidHandleError(GenericError):
    r"""A value passed in as a handle is not currently a handle which is valid."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_INVALID_HANDLE, InvalidHandleError)

class InvalidPointerError(GenericError):
    r"""Attempt to free a pointer that Libaudioverse doesn't know about."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_INVALID_POINTER, InvalidPointerError)

class InvalidPropertyError(GenericError):
    r"""An attempt to access a property which does not exist on the specified node."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_INVALID_PROPERTY, InvalidPropertyError)

class MemoryError(GenericError):
    r"""Libaudioverse triedd to allocate a pointer, but could not."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_MEMORY, MemoryError)

class NoSuchDeviceError(GenericError):
    r"""Attempt to use an I/O device that doesn't exist.  In addition to being caused by your code, this can happen if the user unplugs the device."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_NO_SUCH_DEVICE, NoSuchDeviceError)

class NotInitializedError(GenericError):
    r"""Failure to call ``Lav_initialized``."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_NOT_INITIALIZED, NotInitializedError)

class NullPointerError(GenericError):
    r"""You passed a null pointer into Libaudioverse in a context where null pointers are not allowed."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_NULL_POINTER, NullPointerError)

class OverlappingAutomatorsError(GenericError):
    r"""An attempt to schedule an automator within the duration of another."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_OVERLAPPING_AUTOMATORS, OverlappingAutomatorsError)

class PropertyIsReadOnlyError(GenericError):
    r"""Attempt to set a read-only property."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_PROPERTY_IS_READ_ONLY, PropertyIsReadOnlyError)

class RangeError(GenericError):
    r"""A function parameter is not within a valid range.  This could be setting property values outside their range, accessing inputs and outputs that do not exist, or any of a variety of other range error conditions."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_RANGE, RangeError)

class TypeMismatchError(GenericError):
    r"""Indicates an attempt to manipulate a property through a function that does not work with that property's type."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_TYPE_MISMATCH, TypeMismatchError)

class UnknownError(GenericError):
    r"""Something went wrong.  This error indicates that we couldn't figure out what."""
    pass
_lav.bindings_register_exception(_libaudioverse.Lav_ERROR_UNKNOWN, UnknownError)


#logging infrastructure
def _logging_callback(level, message):
    l=logging.getLogger("libaudioverse")
    if level == LoggingLevels.critical:
        l.critical(message)
    elif level == LoggingLevels.info:
        l.info(message)
    elif level == LoggingLevels.debug:
        l.debug(message)

_logging_callback_ctypes = _libaudioverse.LavLoggingCallback(_logging_callback)
_lav.set_logging_callback(_logging_callback_ctypes)
_lav.set_logging_level(int(LoggingLevels.debug))

#library initialization and termination.

_initialized = False
def initialize():
    r"""Corresponds to Lav_initialize, plus binding specific setup.
    
    Call this before using anything from Libaudioverse."""
    global _initialized
    _lav.initialize()
    _initialized = True

def shutdown():
    r"""Corresponds to Lav_shutdown.
    
    Call this at the end of your application.
    You must call it before the interpreter shuts down. Failure to do so will allow Libaudioverse to call your code during Python's shutdown procedures."""
    global _initialized
    _initialized = False
    _lav.shutdown()

@contextlib.contextmanager
def InitializationManager():
    """Use this with a with block to manage Libaudioverse initialization and shutdown.

The advantage of this function is that Libaudioverse will shutdown properly in all cases that involve Python exceptions. While segfaulting the interpreter will not cause a shutdown, exceptions unrelated to Libaudioverse will.
Since failure to call shutdown can cause crashes, this is the preferred method of initialization in production applications; it will prevent many types of crashes in your app from turning into Libaudioverse crashes."""
    initialize()
    yield
    shutdown()

class _CallbackWrapper(object):

    def __init__(self, for_object, cb, additional_args, additional_kwargs, remove_from_set = None):
        self.additional_args = additional_args if additional_args is not None else ()
        self.additional_kwargs = additional_kwargs if additional_kwargs is not None else dict()
        self.cb = cb
        self.object_handle = for_object.handle.handle
        self.remove_from_set = remove_from_set

    def __call__(self, *args):
        needed_args = (_resurrect(_lav._HandleBox(self.object_handle)), )+args[1:-1]+self.additional_args #be sure to eliminate userdata, which is always the last argument.
        retval = self.cb(*needed_args, **self.additional_kwargs)
        if self.remove_from_set:
            self.remove_from_set.remove(self)

class DeviceInfo(object):
    r"""Represents info on a audio device.
    
    Channels is the number of channels for the device.  Name is a unicode string containing a human-readable name.  Identifier should be used with Server.set_output_device.
    
    The caveat from the Libaudioverse manual should be  summarized here:
    channels is not reliable, and your application should default to stereo while providing the user the option to change it."""

    def __init__(self, channels, identifier, name):
        self.channels = channels
        self.name = name
        self.identifier = identifier

def enumerate_devices():
    r"""Returns a list of DeviceInfo representing the devices on the system."""
    max_index = _lav.device_get_count()
    infos = []
    for i in six.moves.range(max_index):
        info = DeviceInfo(identifier = _lav.device_get_identifier_string(i),
        channels = _lav.device_get_channels(i),
        name = _lav.device_get_name(i))
        infos.append(info)
    return infos

@functools.total_ordering
class _HandleComparer(object):

    def __eq__(self, other):
        if not isinstance(other, _HandleComparer): return False
        return self.handle == other.handle

    def __lt__(self, other):
        #Things that aren't subclasses are less than us.
        if not isinstance(other, _HandleComparer): return True
        return self.handle < other.handle

    def __hash__(self):
        #We need to return the handle itself.  The box could be unique.
        return self.handle.handle

    def _to_handle(self):
        return self.handle.handle

class Server(_HandleComparer):
    r"""Represents a server.  All libaudioverse nodes must be passed a server at creation time as the first argument to their constructor and cannot migrate between them.  Furthermore, it is an error to try to connect objects from different servers.

Instances of this class are context managers.  Using the with statement on an instance of this class invoke's Libaudioverse's atomic block support.

For full details of this class, see the Libaudioverse manual."""

    def __init__(self, sample_rate = 44100, block_size = 1024):
        handle = _lav.create_server(sample_rate, block_size)
        self.init_with_handle(handle)
        _weak_handle_lookup[self.handle] = self

    def init_with_handle(self, handle):
        with _object_states_lock:
            if handle.handle not in _object_states:
                _object_states[handle.handle] = dict()
                _object_states[handle.handle]['lock'] = threading.Lock()
                _object_states[handle.handle]['block_callback'] = None
                _object_states[handle.handle]['scheduled_callbacks'] = set()
            self._state = _object_states[handle.handle]
            self.handle = handle
            self._lock = self._state['lock']

    def set_output_device(self, identifier = "default", channels=2, mixahead = 2):
        r"""Sets the output device.
        Use -1 for default system audio. 0 and greater are specific audio devices.
        To enumerate devices, use enumerate_devices."""
        _lav.server_set_output_device(self, identifier, channels, mixahead)

    def clear_output_device(self):
        r"""Clears the output device, stopping audio and allowing use of get_block again."""
        _lav.server_clear_output_device(self)

    def get_block(self, channels, may_apply_mixing_matrix = True):
        r"""Returns a block of data.
        
        This function wraps Lav_getBlock.  Note that calling this on a server configured to output audio is an error.
        
        If may_apply_mixing_matrix is True, audio will be automatically converted to the output channel type.  If it is false, channels are either dropped or padded with zeros."""
        with self._lock:
            length = _lav.server_get_block_size(self.handle)*channels
            buff = (ctypes.c_float*length)()
            #circumvent automatic conversion of iterables.
            buff_ptr = ctypes.POINTER(ctypes.c_float)()
            buff_ptr.contents = buff
            _lav.server_get_block(self.handle, channels, may_apply_mixing_matrix, buff_ptr)
            return list(buff)

    #context manager support.
    def __enter__(self):
        r"""Lock the server."""
        _lav.server_lock(self.handle)

    def __exit__(self, type, value, traceback):
        r"""Unlock the server."""
        _lav.server_unlock(self.handle)

    def set_block_callback(self, callback, additional_args=None, additional_kwargs=None):
        r"""Set a callback to be called every block.
        
        This callback is called as though inside a with block, and takes two positional argguments: the server and the servers' time.
        
        Wraps lav_serverSetBlockCallback."""
        with self._lock:
            if callback is not None:
                wrapper = _CallbackWrapper(self, callback, additional_args, additional_kwargs)
                ctypes_callback=_libaudioverse.LavTimeCallback(wrapper)
                _lav.server_set_block_callback(self, ctypes_callback, None)
                self._state['block_callback'] = (callback, wrapper, ctypes_callback)
            else:
                _lav.server_set_block_callback(self, _libaudioverse.LavTimeCallback(0), None)
                self._state['block_callback'] = None

    def get_block_callback(self):
        r"""The Python bindings provide the ability to retrieve callback objects.  This function retrieves the set block callback, if any."""
        with self._lock:
            return self._state['block_callback'][0]

    def call_in(self, when, callback, extra_args = None, extra_kwargs = None, in_audio_thread = False):
        r"""Schedule a fucntion to run in the future.
        
        If in_audio_thread is false, it is safe to call the Libaudioverse API.
        
        Wraps Lav_serverCallIn."""
        with self._lock:
            wrapped = _CallbackWrapper(self, callback, extra_args, extra_kwargs, self._state['scheduled_callbacks'])
            ct = _libaudioverse.LavTimeCallback(wrapped)
            wrapped.ctypes = ct #Ugly, but works and everything else was worse than this at time of writing.
            _lav.server_call_in(self.handle, when, in_audio_thread, ct, None)
            self._state['scheduled_callbacks'].add(wrapped)

    def write_file(self, path, channels, duration, may_apply_mixing_matrix=True):
        r"""Write blocks of data to a file.
        
        This function wraps Lav_serverWriteFile."""
        _lav.server_write_file(self, path, channels, duration, may_apply_mixing_matrix)

    @property
    def threads(self):
        r"""The number of threads the server is using for processing.
        
        This wraps Lav_serverGetThreads and Lav_serverSetThreads."""
        return _lav.server_get_threads(self)
        
    @threads.setter
    def threads(self, value):
        _lav.server_set_threads(self, value)

_types_to_classes[ObjectTypes.server] = Server

#Buffer objects.
class Buffer(_HandleComparer):
    r"""An audio buffer.

Use load_from_file to read a file or load_from_array to load an iterable."""

    def __init__(self, server):
        handle=_lav.create_buffer(server)
        self.init_with_handle(handle)
        _weak_handle_lookup[self.handle] = self

    def init_with_handle(self, handle):
        with _object_states_lock:
            if handle.handle not in _object_states:
                _object_states[handle.handle] = dict()
                _object_states[handle.handle]['lock'] = threading.Lock()
                _object_states[handle.handle]['server'] = _resurrect(_lav.buffer_get_server(handle))
            self._state=_object_states[handle.handle]
            self._lock = self._state['lock']
            self.handle = handle

    def load_from_file(self, path):
        r"""Load an audio file.
        
        Wraps Lav_bufferLoadFromFile."""
        _lav.buffer_load_from_file(self, path)

    def load_from_array(self, sr, channels, frames, data):
        r"""Load from an array of interleaved floats.
        
        Wraps Lav_bufferLoadFromArray."""
        _lav.buffer_load_from_array(self, sr, channels, frames, data)

    def decode_from_array(self, array):
        r"""Takes an encoded array of audio data and decodes it.

Wraps Lav_bufferDecodeFromArray.  Array must be a string, bytes, or iterable of bytes.  DO not give unicode to this function.  Objects which do not support the ctypes buffer interface will process unusably slowly."""
        _lav.buffer_decode_from_array(self, array, len(array))

    def get_duration(self):
        r"""Get the duration of the buffer in seconds.
        
        Wraps Lav_bufferGetDuration."""
        return _lav.buffer_get_duration(self)

    def get_length_in_samples(self):
        r"""Returns the length of the buffer in samples.
        
        Wraps Lav_bufferGetLengthInSamples."""
        return _lav.buffer_get_length_in_samples(self)

    def normalize(self):
        r"""Normalizes the buffer.
        
        Wraps Lav_bufferNormalize."""
        _lav.buffer_normalize(self)

_types_to_classes[ObjectTypes.buffer] = Buffer

#the following classes implement properties:








def _extract_value(v):
    if isinstance(v, LibaudioverseProperty):
        return v.value
    return v


class LibaudioverseProperty(object):
    r"""Proxy to Libaudioverse properties.
    
    All properties support resetting and type query."""

    def __init__(self, handle, slot, getter, setter, converter = lambda x: x):
        self._handle = handle
        self._slot = slot
        self._getter=getter
        self._setter = setter
        self._converter = converter

    @property
    def value(self):
        return self._getter(self._handle, self._slot)

    @value.setter
    def value(self, val):
        return self._setter(self._handle, self._slot, self._converter(val))

    def reset(self):
        _lav.node_reset_property(self._handle, self._slot)

    @property
    def type(self):
        """The property's type."""
        return PropertyTypes(_lav.node_get_property_type(self._handle, self._slot))

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.value)

# We don't want to type implementations for __bool__ and __nonzero__ over and over.
# But we can't put them on all the properties.
class _BooleanMixin(object):

    def __bool__(self):
        return bool(self.value)

    __nonzero__ = __bool__

class BooleanProperty(LibaudioverseProperty, _BooleanMixin):
    r"""Represents a boolean property.
    
    Note that boolean properties show up as int properties when their type is queried.
    This class adds extra marshalling to make sure that boolean properties show up as booleans on the Python side, as the C API does not distinguish between boolean properties and int properties with range [0, 1]."""
    
    def __init__(self, handle, slot):
        super(BooleanProperty, self).__init__(handle = handle, slot = slot, getter =_lav.node_get_int_property, setter = _lav.node_set_int_property, converter = bool)

    @LibaudioverseProperty.value.getter
    def value(self):
        return bool(self._getter(self._handle, self._slot))


class IntProperty(LibaudioverseProperty, numbers.Integral, _BooleanMixin):
    r"""Proxy to an integer property."""

    def __init__(self, handle, slot):
        super(IntProperty, self).__init__(handle = handle, slot = slot, getter = _lav.node_get_int_property, setter = _lav.node_set_int_property, converter = int)


    def __add__(self, other):
        other = _extract_value(other)
        return operator.add(self.value, other)

    def __radd__(self, other):
        other = _extract_value(other)
        return operator.add(other, self.value)

    def __iadd__(self, other):
        other = _extract_value(other)
        self.value = operator.add(self.value, other)
        return self

    def __sub__(self, other):
        other = _extract_value(other)
        return operator.sub(self.value, other)

    def __rsub__(self, other):
        other = _extract_value(other)
        return operator.sub(other, self.value)

    def __isub__(self, other):
        other = _extract_value(other)
        self.value = operator.sub(self.value, other)
        return self

    def __mul__(self, other):
        other = _extract_value(other)
        return operator.mul(self.value, other)

    def __rmul__(self, other):
        other = _extract_value(other)
        return operator.mul(other, self.value)

    def __imul__(self, other):
        other = _extract_value(other)
        self.value = operator.mul(self.value, other)
        return self

    def __floordiv__(self, other):
        other = _extract_value(other)
        return operator.floordiv(self.value, other)

    def __rfloordiv__(self, other):
        other = _extract_value(other)
        return operator.floordiv(other, self.value)

    def __ifloordiv__(self, other):
        other = _extract_value(other)
        self.value = operator.floordiv(self.value, other)
        return self

    def __mod__(self, other):
        other = _extract_value(other)
        return operator.mod(self.value, other)

    def __rmod__(self, other):
        other = _extract_value(other)
        return operator.mod(other, self.value)

    def __imod__(self, other):
        other = _extract_value(other)
        self.value = operator.mod(self.value, other)
        return self

    def __divmod__(self, other):
        other = _extract_value(other)
        return operator.divmod(self.value, other)

    def __rdivmod__(self, other):
        other = _extract_value(other)
        return operator.divmod(other, self.value)

    def __idivmod__(self, other):
        other = _extract_value(other)
        self.value = operator.divmod(self.value, other)
        return self

    def __div__(self, other):
        other = _extract_value(other)
        return operator.div(self.value, other)

    def __rdiv__(self, other):
        other = _extract_value(other)
        return operator.div(other, self.value)

    def __idiv__(self, other):
        other = _extract_value(other)
        self.value = operator.div(self.value, other)
        return self

    def __truediv__(self, other):
        other = _extract_value(other)
        return operator.truediv(self.value, other)

    def __rtruediv__(self, other):
        other = _extract_value(other)
        return operator.truediv(other, self.value)

    def __itruediv__(self, other):
        other = _extract_value(other)
        self.value = operator.truediv(self.value, other)
        return self

    def __lshift__(self, other):
        other = _extract_value(other)
        return operator.lshift(self.value, other)

    def __rlshift__(self, other):
        other = _extract_value(other)
        return operator.lshift(other, self.value)

    def __ilshift__(self, other):
        other = _extract_value(other)
        self.value = operator.lshift(self.value, other)
        return self

    def __rshift__(self, other):
        other = _extract_value(other)
        return operator.rshift(self.value, other)

    def __rrshift__(self, other):
        other = _extract_value(other)
        return operator.rshift(other, self.value)

    def __irshift__(self, other):
        other = _extract_value(other)
        self.value = operator.rshift(self.value, other)
        return self

    def __and__(self, other):
        other = _extract_value(other)
        return operator.and_(self.value, other)

    def __rand__(self, other):
        other = _extract_value(other)
        return operator.and_(other, self.value)

    def __iand__(self, other):
        other = _extract_value(other)
        self.value = operator.and_(self.value, other)
        return self

    def __xor__(self, other):
        other = _extract_value(other)
        return operator.xor(self.value, other)

    def __rxor__(self, other):
        other = _extract_value(other)
        return operator.xor(other, self.value)

    def __ixor__(self, other):
        other = _extract_value(other)
        self.value = operator.xor(self.value, other)
        return self

    def __or__(self, other):
        other = _extract_value(other)
        return operator.or_(self.value, other)

    def __ror__(self, other):
        other = _extract_value(other)
        return operator.or_(other, self.value)

    def __ior__(self, other):
        other = _extract_value(other)
        self.value = operator.or_(self.value, other)
        return self

    def __neg__(self):
        return operator.neg(self.value)
    def __pos__(self):
        return operator.pos(self.value)
    def __abs__(self):
        return operator.abs(self.value)
    def __invert__(self):
        return operator.invert(self.value)

    def __pow__(self, other, modulus = None):
        other = _extract_value(other)
        if modulus:
            modulus = _extract_value(modulus)
        if modulus:
            return pow(self.value, other, modulus)
        else:
            return pow(self.value, other)

    def __ipow__(self, other, modulus = None):
        self.value = self.__pow__(other, modulus)
        return self

    def __rpow__(self, other):
        return self.__pow__(other, self.value)

    def __complex__(self):
        return complex(self.value)
    def __long__(self):
        return long(self.value)
    def __int__(self):
        return int(self.value)
    def __float__(self):
        return float(self.value)

    def __eq__(self, other):
        return operator.eq(self.value, _extract_value(other))
    def __lt__(self, other):
        return operator.lt(self.value, _extract_value(other))
    def __gt__(self, other):
        return operator.gt(self.value, _extract_value(other))
    def __ne__(self, other):
        return operator.ne(self.value, _extract_value(other))
    def __le__(self, other):
        return operator.le(self.value, _extract_value(other))
    def __ge__(self, other):
        return operator.ge(self.value, _extract_value(other))

    def __ceil__(self):
        return math.ceil(self.value)

    def __floor__(self):
        return math.floor(self.value)

    def __round__(self, n = None):
        if n:
            return round(self.value, n)
        else:
            return round(self.value)

    def __trunc__(self):
        return math.trunc(self.value)


    def __oct__(self):
        return oct(self.value)

    def __hex__(self):
        return hex(self.value)

class EnumProperty(LibaudioverseProperty, _BooleanMixin):
    r"""Proxy to an integer property taking an enum.

This class is like IntProperty, but it will error if you try to yuse the wrong enum or a regular integer constant.
In the C API, the distinction between these classes does not exist: both use Lav_nodeGetIntProperty and Lav_nodeSetIntProperty."""

    def __init__(self, handle, slot, enum):
        super(EnumProperty, self).__init__(handle = handle, slot = slot, getter = None, setter = None)
        self._enum = enum

    @property
    def value(self):
        return self._enum(_lav.node_get_int_property(self._handle, self._slot))

    @value.setter
    def value(self, val):
        if not isinstance(val, self._enum):
            raise TypeError("Value must be a {} member.".format(self._enum.__name__))
        _lav.node_set_int_property(self._handle, self._slot, int(val))

    def __repr__(self):
        return "<{} {}.{}>".format(self.__class__.__name__, self._enum.__name__, self.value.name)

class AutomatedProperty(LibaudioverseProperty):
    r"""A property that supports automation and node connection."""

    def linear_ramp_to_value(self, time, value):
        """Schedule a linear automator.
        
        The property's value will change to the specified value by the specified time, starting at the end of the previous automator
        
        This function wraps Lav_automationLinearRampToValue."""
        _lav.automation_linear_ramp_to_value(self._handle, self._slot, float(time), float(value))

    def envelope(self, time, duration, values):
        r"""Run an envelope.
        
        The property's value will stay where it was after the last automator until the specified time is reached, whereupon it will follow the envelope until time+duration.
        
        This function wraps Lav_automationEnvelope."""
        values_length = len(values)
        _lav.automation_envelope(self._handle, self._slot, time, duration, values_length, values)

    def set(self, time, value):
        r"""Sets the property's value to a specific value at a specific time.
        
        Wraps Lav_automationSet."""
        _lav.automation_set(self._handle, self._slot, float(time), float(value))

    def cancel_automators(self, time):
        r"""Cancel all automators scheduled to start after time.
        
        Wraps Lav_automationCancelAutomators."""
        _lav.automation_cancel_automators(self._handle, self._slot, float(time))


class FloatProperty(AutomatedProperty, numbers.Real, _BooleanMixin):
    r"""Proxy to a float property."""

    def __init__(self, handle, slot):
        super(FloatProperty, self).__init__(handle = handle, slot = slot, getter = _lav.node_get_float_property, setter = _lav.node_set_float_property, converter = float)


    def __add__(self, other):
        other = _extract_value(other)
        return operator.add(self.value, other)

    def __radd__(self, other):
        other = _extract_value(other)
        return operator.add(other, self.value)

    def __iadd__(self, other):
        other = _extract_value(other)
        self.value = operator.add(self.value, other)
        return self

    def __sub__(self, other):
        other = _extract_value(other)
        return operator.sub(self.value, other)

    def __rsub__(self, other):
        other = _extract_value(other)
        return operator.sub(other, self.value)

    def __isub__(self, other):
        other = _extract_value(other)
        self.value = operator.sub(self.value, other)
        return self

    def __mul__(self, other):
        other = _extract_value(other)
        return operator.mul(self.value, other)

    def __rmul__(self, other):
        other = _extract_value(other)
        return operator.mul(other, self.value)

    def __imul__(self, other):
        other = _extract_value(other)
        self.value = operator.mul(self.value, other)
        return self

    def __floordiv__(self, other):
        other = _extract_value(other)
        return operator.floordiv(self.value, other)

    def __rfloordiv__(self, other):
        other = _extract_value(other)
        return operator.floordiv(other, self.value)

    def __ifloordiv__(self, other):
        other = _extract_value(other)
        self.value = operator.floordiv(self.value, other)
        return self

    def __mod__(self, other):
        other = _extract_value(other)
        return operator.mod(self.value, other)

    def __rmod__(self, other):
        other = _extract_value(other)
        return operator.mod(other, self.value)

    def __imod__(self, other):
        other = _extract_value(other)
        self.value = operator.mod(self.value, other)
        return self

    def __divmod__(self, other):
        other = _extract_value(other)
        return operator.divmod(self.value, other)

    def __rdivmod__(self, other):
        other = _extract_value(other)
        return operator.divmod(other, self.value)

    def __idivmod__(self, other):
        other = _extract_value(other)
        self.value = operator.divmod(self.value, other)
        return self

    def __div__(self, other):
        other = _extract_value(other)
        return operator.div(self.value, other)

    def __rdiv__(self, other):
        other = _extract_value(other)
        return operator.div(other, self.value)

    def __idiv__(self, other):
        other = _extract_value(other)
        self.value = operator.div(self.value, other)
        return self

    def __truediv__(self, other):
        other = _extract_value(other)
        return operator.truediv(self.value, other)

    def __rtruediv__(self, other):
        other = _extract_value(other)
        return operator.truediv(other, self.value)

    def __itruediv__(self, other):
        other = _extract_value(other)
        self.value = operator.truediv(self.value, other)
        return self

    def __neg__(self):
        return operator.neg(self.value)
    def __pos__(self):
        return operator.pos(self.value)
    def __abs__(self):
        return operator.abs(self.value)

    def __pow__(self, other, modulus = None):
        other = _extract_value(other)
        if modulus:
            modulus = _extract_value(modulus)
        if modulus:
            return pow(self.value, other, modulus)
        else:
            return pow(self.value, other)

    def __ipow__(self, other, modulus = None):
        self.value = self.__pow__(other, modulus)
        return self

    def __rpow__(self, other):
        return self.__pow__(other, self.value)

    def __complex__(self):
        return complex(self.value)
    def __long__(self):
        return long(self.value)
    def __int__(self):
        return int(self.value)
    def __float__(self):
        return float(self.value)

    def __eq__(self, other):
        return operator.eq(self.value, _extract_value(other))
    def __lt__(self, other):
        return operator.lt(self.value, _extract_value(other))
    def __gt__(self, other):
        return operator.gt(self.value, _extract_value(other))
    def __ne__(self, other):
        return operator.ne(self.value, _extract_value(other))
    def __le__(self, other):
        return operator.le(self.value, _extract_value(other))
    def __ge__(self, other):
        return operator.ge(self.value, _extract_value(other))

    def __ceil__(self):
        return math.ceil(self.value)

    def __floor__(self):
        return math.floor(self.value)

    def __round__(self, n = None):
        if n:
            return round(self.value, n)
        else:
            return round(self.value)

    def __trunc__(self):
        return math.trunc(self.value)



class DoubleProperty(LibaudioverseProperty, numbers.Real, _BooleanMixin):
    r"""Proxy to a double property."""

    def __init__(self, handle, slot):
        super(DoubleProperty, self).__init__(handle = handle, slot = slot, getter = _lav.node_get_double_property, setter = _lav.node_set_double_property, converter = float)


    def __add__(self, other):
        other = _extract_value(other)
        return operator.add(self.value, other)

    def __radd__(self, other):
        other = _extract_value(other)
        return operator.add(other, self.value)

    def __iadd__(self, other):
        other = _extract_value(other)
        self.value = operator.add(self.value, other)
        return self

    def __sub__(self, other):
        other = _extract_value(other)
        return operator.sub(self.value, other)

    def __rsub__(self, other):
        other = _extract_value(other)
        return operator.sub(other, self.value)

    def __isub__(self, other):
        other = _extract_value(other)
        self.value = operator.sub(self.value, other)
        return self

    def __mul__(self, other):
        other = _extract_value(other)
        return operator.mul(self.value, other)

    def __rmul__(self, other):
        other = _extract_value(other)
        return operator.mul(other, self.value)

    def __imul__(self, other):
        other = _extract_value(other)
        self.value = operator.mul(self.value, other)
        return self

    def __floordiv__(self, other):
        other = _extract_value(other)
        return operator.floordiv(self.value, other)

    def __rfloordiv__(self, other):
        other = _extract_value(other)
        return operator.floordiv(other, self.value)

    def __ifloordiv__(self, other):
        other = _extract_value(other)
        self.value = operator.floordiv(self.value, other)
        return self

    def __mod__(self, other):
        other = _extract_value(other)
        return operator.mod(self.value, other)

    def __rmod__(self, other):
        other = _extract_value(other)
        return operator.mod(other, self.value)

    def __imod__(self, other):
        other = _extract_value(other)
        self.value = operator.mod(self.value, other)
        return self

    def __divmod__(self, other):
        other = _extract_value(other)
        return operator.divmod(self.value, other)

    def __rdivmod__(self, other):
        other = _extract_value(other)
        return operator.divmod(other, self.value)

    def __idivmod__(self, other):
        other = _extract_value(other)
        self.value = operator.divmod(self.value, other)
        return self

    def __div__(self, other):
        other = _extract_value(other)
        return operator.div(self.value, other)

    def __rdiv__(self, other):
        other = _extract_value(other)
        return operator.div(other, self.value)

    def __idiv__(self, other):
        other = _extract_value(other)
        self.value = operator.div(self.value, other)
        return self

    def __truediv__(self, other):
        other = _extract_value(other)
        return operator.truediv(self.value, other)

    def __rtruediv__(self, other):
        other = _extract_value(other)
        return operator.truediv(other, self.value)

    def __itruediv__(self, other):
        other = _extract_value(other)
        self.value = operator.truediv(self.value, other)
        return self

    def __neg__(self):
        return operator.neg(self.value)
    def __pos__(self):
        return operator.pos(self.value)
    def __abs__(self):
        return operator.abs(self.value)

    def __pow__(self, other, modulus = None):
        other = _extract_value(other)
        if modulus:
            modulus = _extract_value(modulus)
        if modulus:
            return pow(self.value, other, modulus)
        else:
            return pow(self.value, other)

    def __ipow__(self, other, modulus = None):
        self.value = self.__pow__(other, modulus)
        return self

    def __rpow__(self, other):
        return self.__pow__(other, self.value)

    def __complex__(self):
        return complex(self.value)
    def __long__(self):
        return long(self.value)
    def __int__(self):
        return int(self.value)
    def __float__(self):
        return float(self.value)

    def __eq__(self, other):
        return operator.eq(self.value, _extract_value(other))
    def __lt__(self, other):
        return operator.lt(self.value, _extract_value(other))
    def __gt__(self, other):
        return operator.gt(self.value, _extract_value(other))
    def __ne__(self, other):
        return operator.ne(self.value, _extract_value(other))
    def __le__(self, other):
        return operator.le(self.value, _extract_value(other))
    def __ge__(self, other):
        return operator.ge(self.value, _extract_value(other))

    def __ceil__(self):
        return math.ceil(self.value)

    def __floor__(self):
        return math.floor(self.value)

    def __round__(self, n = None):
        if n:
            return round(self.value, n)
        else:
            return round(self.value)

    def __trunc__(self):
        return math.trunc(self.value)


class StringProperty(LibaudioverseProperty, _BooleanMixin):
    r"""Proxy to a string property."""

    def __init__(self, handle, slot):
        super(StringProperty, self).__init__(handle = handle, slot = slot, getter = _lav.node_get_string_property, setter = _lav.node_set_string_property)

class BufferProperty(LibaudioverseProperty, _BooleanMixin):
    r"""Proxy to a buffer property.
    
    It is safe to set this property to None."""
    
    def __init__(self, handle, slot):
        #no getter and setter. This is custom.
        self._handle = handle
        self._slot = slot

    @property
    def value(self):
        handle = _lav.node_get_buffer_property(self._handle, self._slot)
        if handle:
            return _resurrect(handle)
        else:
            return None

    @value.setter
    def value(self, val):
        if val is None or isinstance(val, Buffer):
            _lav.node_set_buffer_property(self._handle, self._slot, val)
        else:
            raise ValueError("Expected a Buffer or None.")

class VectorProperty(LibaudioverseProperty):
    r"""class to act as a base for  float3 and float6 properties.
    
    This class knows how to marshal anything that is a collections.sized and will error if length constraints are not met."""

    def __init__(self, handle, slot, getter, setter, length):
        super(VectorProperty, self).__init__(handle = handle, slot = slot, getter = getter, setter =setter)
        self._length = length

    #Override setter:
    @LibaudioverseProperty.value.setter
    def value(self, val):
        if not isinstance(val, collections.Sized):
            raise ValueError("Expected a collections.sized subclass")
        if len(val) != self._length:
            raise ValueError("Expected a {}-element list".format(self._length))
        self._setter(self._handle, self._slot, *val)

class Float3Property(VectorProperty):
    r"""Represents a float3 property."""
    
    def __init__(self, handle, slot):
        super(Float3Property, self).__init__(handle = handle, slot = slot, getter =_lav.node_get_float3_property, setter = _lav.node_set_float3_property, length = 3)

class Float6Property(VectorProperty):
    r"""Represents a float6 property."""
    
    def __init__(self, handle, slot):
        super(Float6Property, self).__init__(handle = handle, slot = slot, getter =_lav.node_get_float6_property, setter =_lav.node_set_float6_property, length = 6)

#Array properties.
#This is a base class because we have 2, but they have to lock their parent node.
class ArrayProperty(LibaudioverseProperty):
    r"""Base class for all array properties."""

    def __init__(self, handle, slot, reader, replacer, length, lock):
        self._handle = handle
        self._slot = slot
        self._reader=reader
        self._replacer=replacer
        self._length = length
        self._lock = lock

    @property
    def value(self):
        r"""The array, as a tuple."""
        with self._lock:
            length = self._length(self._handle, self._slot)
            accum = [None]*length
            for i in six.moves.range(length):
                accum[i] = self._reader(self._handle, self._slot, i)
        return tuple(accum)

    @value.setter
    def value(self, val):
        self._replacer(self._handle, self._slot, len(val), val)

class IntArrayProperty(ArrayProperty):
    r"""Represents an int array property."""
    def __init__(self, handle, slot, lock):
        super(IntArrayProperty, self).__init__(handle = handle, slot = slot, lock = lock, reader = _lav.node_read_int_array_property,
            replacer =_lav.node_replace_int_array_property, length = _lav.node_get_int_array_property_length)

class FloatArrayProperty(ArrayProperty):
    r"""Represents a float array property."""

    def __init__(self, handle, slot, lock):
        super(FloatArrayProperty, self).__init__(handle = handle, slot = slot, lock = lock,
            reader =_lav.node_read_float_array_property,
            replacer = _lav.node_replace_float_array_property,
            length = _lav.node_get_float_array_property_length
        )

#This is the class hierarchy.
#GenericNode is at the bottom, and we should never see one; and GenericObject should hold most implementation.
class GenericNode(_HandleComparer):
    r"""Base class for all Libaudioverse nodes.
    
    All properties and functionality on this class is available to all Libaudioverse nodes without exception."""

    def __init__(self, handle):
        self.init_with_handle(handle)
        _weak_handle_lookup[self.handle] = self

    def init_with_handle(self, handle):
        with _object_states_lock:
            self.handle = handle
            if handle.handle not in _object_states:
                _object_states[handle.handle] = dict()
                self._state = _object_states[handle.handle]
                self._state['server'] = _resurrect(_lav.node_get_server(self.handle))
                self._state['callbacks'] = dict()
                self._state['input_connection_count'] =_lav.node_get_input_connection_count(self)
                self._state['output_connection_count'] = _lav.node_get_output_connection_count(self)
                self._state['lock'] = threading.Lock()
                self._state['properties'] = dict()
                self._state['property_instances'] = dict()
                self._state['properties']["add"] = _libaudioverse.Lav_NODE_ADD
                self._state['properties']["channel_interpretation"] = _libaudioverse.Lav_NODE_CHANNEL_INTERPRETATION
                self._state['properties']["mul"] = _libaudioverse.Lav_NODE_MUL
                self._state['properties']["state"] = _libaudioverse.Lav_NODE_STATE
            else:
                self._state=_object_states[handle.handle]
            self._lock = self._state['lock']
            self._property_instances = dict()
            self._property_instances[_libaudioverse.Lav_NODE_ADD] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_NODE_ADD)
            self._property_instances[_libaudioverse.Lav_NODE_CHANNEL_INTERPRETATION] = EnumProperty(handle = self.handle, slot = _libaudioverse.Lav_NODE_CHANNEL_INTERPRETATION, enum = ChannelInterpretations)
            self._property_instances[_libaudioverse.Lav_NODE_MUL] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_NODE_MUL)
            self._property_instances[_libaudioverse.Lav_NODE_STATE] = EnumProperty(handle = self.handle, slot = _libaudioverse.Lav_NODE_STATE, enum = NodeStates)

    def get_property_names(self):
        r"""Get the names of all properties on this node."""
        return self._state['properties'].keys()

    @property
    def server(self):
        """Get the server."""
        return self._state['server']

    def connect(self, *args):
        r"""Form a connection between this node and another object.
        
        This function has 3 valid signatures:
        
        node.connect(output, other_node, input): Connect output to the specified input of other_node.
        node.connect(output, property): Connect the specified output to the specified property on another node.  The property must be a float or double property.
        node.connect(output, server): Connect the specified output to the server.
        
        Any node which is connected directly or indirectly to the server will remain alive even if your program lets go of it.
        For more details on the subject of node lifetimes, see the Libaudioverse manual.
        """
        if len(args) == 3:
            _lav.node_connect(self, args[0], args[1], args[2])
        elif len(args) == 2 and isinstance(args[1], Server):
            _lav.node_connect_server(self, args[0])
        elif len(args) == 2 and isinstance(args[1], AutomatedProperty):
            property = args[1]
            other = property._handle
            slot = property._slot
            _lav.node_connect_property(self, args[0], other, slot)
        else:
            raise ValueError("Couldn't understand arguments. See docstring for details on allowed combinations.")

    def disconnect(self, *args):
        r"""Disconnect from other nodes.
        
        Eventually, this function will support all signatures of connect.  At the moment, we support:
        
        node.disconnect(output): disconnect all connections involving the specified output.
        node.disconnect(output, other, input): Disconnect the specific connection made with node.connect(output, other, input).
        
        This function does not allow key word arguments for the same reason connect doesn't.
"""
        if len(args) == 1:
            _lav.node_disconnect(self, args[0], None, 0)
        elif len(args) == 3:
            _lav.node_disconnect(self, args[0], args[1], args[2])
        else:
            raise ValueError("You must pass 1 or 3 arguments. See the docstring for details.")

    def isolate(self):
        r"""Disconnect all outputs."""
        _lav.node_isolate(self)


    @property
    def add(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

After mul is applied, we add the value to which this property is set to the node's result."""
        return self._property_instances[_libaudioverse.Lav_NODE_ADD]

    @add.setter
    def add(self, value):
        self.add.value=value


    @property
    def channel_interpretation(self):   
        """Type: int

Range: :any:`ChannelInterpretations`

Default value: :any:`ChannelInterpretations.speakers`

How to treat channel count mismatches.
The default is to apply mixing matrices when possible.

If set to :class:`ChannelInterpretationSpeakers`, mixing matrices are applied to inputs.
Otherwise, when set to :class:`ChannelInterpretationDiscrete`, they are not.

This property is almost never needed."""
        return self._property_instances[_libaudioverse.Lav_NODE_CHANNEL_INTERPRETATION]

    @channel_interpretation.setter
    def channel_interpretation(self, value):
        self.channel_interpretation.value=value


    @property
    def mul(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 1.0

After this node processes, the value to which mul is set is used as a multiplier on the result.
The most notable effect of this is to change the node's volume.
A variety of other uses exist, however, especially as regards to nodes which are connected to properties.
Mul is applied before add."""
        return self._property_instances[_libaudioverse.Lav_NODE_MUL]

    @mul.setter
    def mul(self, value):
        self.mul.value=value


    @property
    def state(self):   
        """Type: int

Range: :any:`NodeStates`

Default value: :any:`NodeStates.playing`

The node's state.  See the basics section in the Libaudioverse manual for details.
The default is usually what you want."""
        return self._property_instances[_libaudioverse.Lav_NODE_STATE]

    @state.setter
    def state(self, value):
        self.state.value=value


    def reset(self):
        r"""Perform the node-specific reset operation.
        
        This directly wraps Lav_nodeReset."""
        _lav.node_reset(self)

_types_to_classes[ObjectTypes.generic_node] = GenericNode

class AdditiveSawNode(GenericNode):
    r"""The most accurate, least featureful, and slowest saw oscillator.

This oscillator uses additive synthesis to produce saw waves.
The efficiency therefore depends on the frequency.
Sweeping this oscillator will perform poorly if you do not set the harmonics to a nonzero value.

This oscillator is slightly under the range -1 to 1.
Of the additive oscillators, the sawtooth wave is the worst in this respect.
For this reason, it is probably not suitable as a control signal.
This is not fixable using additive synthesis and is a frequency dependent effect.

This node has no inputs.

Outputs:

=====  ========  ===========
index  channels  description
=====  ========  ===========
0      1         A saw wave.
=====  ========  ===========
"""

    def __init__(self, server):
        super(AdditiveSawNode, self).__init__(_lav.create_additive_saw_node(server))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(AdditiveSawNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["frequency"] = _libaudioverse.Lav_OSCILLATOR_FREQUENCY
                self._state['properties']["frequency_multiplier"] = _libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER
                self._state['properties']["harmonics"] = _libaudioverse.Lav_SAW_HARMONICS
                self._state['properties']["phase"] = _libaudioverse.Lav_OSCILLATOR_PHASE
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_FREQUENCY)
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER)
            self._property_instances[_libaudioverse.Lav_SAW_HARMONICS] = IntProperty(handle = self.handle, slot = _libaudioverse.Lav_SAW_HARMONICS)
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_PHASE] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_PHASE)


    @property
    def frequency(self):   
        """Type: float

Range: [0, INFINITY]

Default value: 440.0

The frequency of the saw wave, in hertz."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY]

    @frequency.setter
    def frequency(self, value):
        self.frequency.value=value



    @property
    def frequency_multiplier(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 1.0

An additional multiplicative factor applied to the frequency of the oscillator.

This is useful for creating instruments, as the notes of the standard musical scale fall on frequency multiples of a reference pitch, rather than a linear increase."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER]

    @frequency_multiplier.setter
    def frequency_multiplier(self, value):
        self.frequency_multiplier.value=value



    @property
    def phase(self):   
        """Type: float

Range: [0.0, 1.0]

Default value: 0.0

The phase of the saw wave.
This is measured in periods, not in radians."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_PHASE]

    @phase.setter
    def phase(self, value):
        self.phase.value=value



    @property
    def harmonics(self):   
        """Type: int

Range: [0, MAX_INT]

Default value: 0

The number of harmonics.
0 requests automatic adjustment.
Use a nonzero value if you intend to sweep the saw wave.

While this property has no max value, any combination of frequency and harmonics that leads to aliasing will alias.
To avoid this, make sure that ``frequency*harmonics`` never goes over half your chosen sampling rate."""
        return self._property_instances[_libaudioverse.Lav_SAW_HARMONICS]

    @harmonics.setter
    def harmonics(self, value):
        self.harmonics.value=value





_types_to_classes[ObjectTypes.additive_saw_node] = AdditiveSawNode
class AdditiveSquareNode(GenericNode):
    r"""The most accurate, least featureful, and slowest square oscillator.

This oscillator uses additive synthesis to produce square waves.
The efficiency therefore depends on the frequency.
Sweeping this oscillator will perform poorly if you do not set the harmonics to a nonzero value.

This oscillator is slightly under the range -1 to 1.
For this reason, it is probably not suitable as a control signal.
This is not fixable using additive synthesis and is a frequency dependent effect.

This node has no inputs.

Outputs:

=====  ========  ==============
index  channels  description   
=====  ========  ==============
0      1         A square wave.
=====  ========  ==============
"""

    def __init__(self, server):
        super(AdditiveSquareNode, self).__init__(_lav.create_additive_square_node(server))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(AdditiveSquareNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["frequency"] = _libaudioverse.Lav_OSCILLATOR_FREQUENCY
                self._state['properties']["frequency_multiplier"] = _libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER
                self._state['properties']["harmonics"] = _libaudioverse.Lav_SQUARE_HARMONICS
                self._state['properties']["phase"] = _libaudioverse.Lav_OSCILLATOR_PHASE
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_FREQUENCY)
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER)
            self._property_instances[_libaudioverse.Lav_SQUARE_HARMONICS] = IntProperty(handle = self.handle, slot = _libaudioverse.Lav_SQUARE_HARMONICS)
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_PHASE] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_PHASE)


    @property
    def frequency(self):   
        """Type: float

Range: [0, INFINITY]

Default value: 440.0

The frequency of the square wave, in hertz."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY]

    @frequency.setter
    def frequency(self, value):
        self.frequency.value=value



    @property
    def frequency_multiplier(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 1.0

An additional multiplicative factor applied to the frequency of the oscillator.

This is useful for creating instruments, as the notes of the standard musical scale fall on frequency multiples of a reference pitch, rather than a linear increase."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER]

    @frequency_multiplier.setter
    def frequency_multiplier(self, value):
        self.frequency_multiplier.value=value



    @property
    def phase(self):   
        """Type: float

Range: [0.0, 1.0]

Default value: 0.0

The phase of the square wave.
This is measured in periods, not in radians."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_PHASE]

    @phase.setter
    def phase(self, value):
        self.phase.value=value



    @property
    def harmonics(self):   
        """Type: int

Range: [0, MAX_INT]

Default value: 0

The number of harmonics.
0 requests automatic adjustment.
Use a nonzero value if you intend to sweep the square wave.

While this property has no max value, any combination of frequency and harmonics that leads to aliasing will alias.
To avoid this, make sure that ``2*frequency*(2*harmonics-1)`` never goes over half your chosen sampling rate."""
        return self._property_instances[_libaudioverse.Lav_SQUARE_HARMONICS]

    @harmonics.setter
    def harmonics(self, value):
        self.harmonics.value=value





_types_to_classes[ObjectTypes.additive_square_node] = AdditiveSquareNode
class AdditiveTriangleNode(GenericNode):
    r"""The most accurate, least featureful, and slowest triangle oscillator.

This oscillator uses additive synthesis to produce triangle waves.
The efficiency therefore depends on the frequency.
Sweeping this oscillator will perform poorly if you do not set the harmonics to a nonzero value.

This oscillator is slightly under the range -1 to 1.
Calibration scripts show that the worst case is -0.9 to 0.9, with the error increasing as frequency increases.
For this reason, it is probably not suitable as a control signal.
This is not fixable using additive synthesis and is a frequency dependent effect.

This node has no inputs.

Outputs:

=====  ========  ================
index  channels  description     
=====  ========  ================
0      1         A triangle wave.
=====  ========  ================
"""

    def __init__(self, server):
        super(AdditiveTriangleNode, self).__init__(_lav.create_additive_triangle_node(server))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(AdditiveTriangleNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["frequency"] = _libaudioverse.Lav_OSCILLATOR_FREQUENCY
                self._state['properties']["frequency_multiplier"] = _libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER
                self._state['properties']["harmonics"] = _libaudioverse.Lav_TRIANGLE_HARMONICS
                self._state['properties']["phase"] = _libaudioverse.Lav_OSCILLATOR_PHASE
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_FREQUENCY)
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER)
            self._property_instances[_libaudioverse.Lav_TRIANGLE_HARMONICS] = IntProperty(handle = self.handle, slot = _libaudioverse.Lav_TRIANGLE_HARMONICS)
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_PHASE] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_PHASE)


    @property
    def frequency(self):   
        """Type: float

Range: [0, INFINITY]

Default value: 440.0

The frequency of the triangle wave, in hertz."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY]

    @frequency.setter
    def frequency(self, value):
        self.frequency.value=value



    @property
    def frequency_multiplier(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 1.0

An additional multiplicative factor applied to the frequency of the oscillator.

This is useful for creating instruments, as the notes of the standard musical scale fall on frequency multiples of a reference pitch, rather than a linear increase."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER]

    @frequency_multiplier.setter
    def frequency_multiplier(self, value):
        self.frequency_multiplier.value=value



    @property
    def phase(self):   
        """Type: float

Range: [0.0, 1.0]

Default value: 0.0

The phase of the triangle wave.
This is measured in periods, not in radians."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_PHASE]

    @phase.setter
    def phase(self, value):
        self.phase.value=value



    @property
    def harmonics(self):   
        """Type: int

Range: [0, MAX_INT]

Default value: 0

The number of harmonics.
0 requests automatic adjustment.
Use a nonzero value if you intend to sweep the triangle wave.

While this property has no max value, any combination of frequency and harmonics that leads to aliasing will alias.
To avoid this, make sure that ``2*frequency*(2*harmonics-1)`` never goes over half your chosen sampling rate."""
        return self._property_instances[_libaudioverse.Lav_TRIANGLE_HARMONICS]

    @harmonics.setter
    def harmonics(self, value):
        self.harmonics.value=value





_types_to_classes[ObjectTypes.additive_triangle_node] = AdditiveTriangleNode
class AllpassNode(GenericNode):
    r"""Implements a first-order allpass filter whose transfer function is :math:`\frac{c+Z^{-d} }{1 + cZ^{-d} }` where ``c`` is the coefficient and ``d`` the delay in samples.

This filter is useful in various reverb designs.

Inputs:

=====  ================================================  =====================
index  channels                                          description          
=====  ================================================  =====================
0      Depends on arguments to this node's constructor.  The signal to filter.
=====  ================================================  =====================

Outputs:

=====  ================================================  ====================
index  channels                                          description         
=====  ================================================  ====================
0      Depends on arguments to this node's constructor.  The filtered signal.
=====  ================================================  ====================
"""

    def __init__(self, server, channels, max_delay):
        super(AllpassNode, self).__init__(_lav.create_allpass_node(server, channels, max_delay))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(AllpassNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["coefficient"] = _libaudioverse.Lav_ALLPASS_COEFFICIENT
                self._state['properties']["delay_max"] = _libaudioverse.Lav_ALLPASS_DELAY_SAMPLES_MAX
                self._state['properties']["delay_samples"] = _libaudioverse.Lav_ALLPASS_DELAY_SAMPLES
                self._state['properties']["interpolation_time"] = _libaudioverse.Lav_ALLPASS_INTERPOLATION_TIME
            self._property_instances[_libaudioverse.Lav_ALLPASS_COEFFICIENT] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_ALLPASS_COEFFICIENT)
            self._property_instances[_libaudioverse.Lav_ALLPASS_DELAY_SAMPLES_MAX] = IntProperty(handle = self.handle, slot = _libaudioverse.Lav_ALLPASS_DELAY_SAMPLES_MAX)
            self._property_instances[_libaudioverse.Lav_ALLPASS_DELAY_SAMPLES] = IntProperty(handle = self.handle, slot = _libaudioverse.Lav_ALLPASS_DELAY_SAMPLES)
            self._property_instances[_libaudioverse.Lav_ALLPASS_INTERPOLATION_TIME] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_ALLPASS_INTERPOLATION_TIME)


    @property
    def coefficient(self):   
        """Type: float

Range: [-INFINITY, INFINITY]


The coefficient of the allpass filter's transfer function.

For those not familiar with digital signal processing, this controls how quickly the repeating echoes created by this filter decay."""
        return self._property_instances[_libaudioverse.Lav_ALLPASS_COEFFICIENT]

    @coefficient.setter
    def coefficient(self, value):
        self.coefficient.value=value



    @property
    def delay_samples(self):   
        """Type: int

Range: dynamic

Default value: 1

The delay of the delay line in samples.
The range of this property depends on the maxDelay parameter to the constructor.

Note that values less than 1 sample still introduce delay."""
        return self._property_instances[_libaudioverse.Lav_ALLPASS_DELAY_SAMPLES]

    @delay_samples.setter
    def delay_samples(self, value):
        self.delay_samples.value=value



    @property
    def delay_max(self):   
        """Type: int

This property is read-only.

The max delay as set at the node's creation time."""
        return self._property_instances[_libaudioverse.Lav_ALLPASS_DELAY_SAMPLES_MAX]




    @property
    def interpolation_time(self):   
        """Type: float

Range: [0.001, INFINITY]

Default value: 0.001

When the delay_samples property is changed, the delay line crossfades between the old position and the new one.
Essentially, this property sets how long it will take the allpass filter to settle after a delay change.
Note that for this node, it is impossible to get rid of the crossfade completely."""
        return self._property_instances[_libaudioverse.Lav_ALLPASS_INTERPOLATION_TIME]

    @interpolation_time.setter
    def interpolation_time(self, value):
        self.interpolation_time.value=value





_types_to_classes[ObjectTypes.allpass_node] = AllpassNode
class AmplitudePannerNode(GenericNode):
    r"""This panner pans for a set of regular speakers without any additional effects applied.
Additionally, it understands surround sound speaker layouts and allows for the assignment of custom speaker mappings.
The default configuration provides a stereo panner that can be used without any additional steps.
The additional function Lav_amplitudePannerNodeConfigureStandardChannelMap can set the panner to output for a variety of standard configurations, so be sure to see its documentation.

Inputs:

=====  ========  =================
index  channels  description      
=====  ========  =================
0      1         The signal to pan
=====  ========  =================

Outputs:

=====  ===============================================  =================================
index  channels                                         description                      
=====  ===============================================  =================================
0      Depends on a number of properties on this node.  The result of panning the signal.
=====  ===============================================  =================================
"""

    def __init__(self, server):
        super(AmplitudePannerNode, self).__init__(_lav.create_amplitude_panner_node(server))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(AmplitudePannerNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["azimuth"] = _libaudioverse.Lav_PANNER_AZIMUTH
                self._state['properties']["channel_map"] = _libaudioverse.Lav_PANNER_CHANNEL_MAP
                self._state['properties']["elevation"] = _libaudioverse.Lav_PANNER_ELEVATION
                self._state['properties']["should_crossfade"] = _libaudioverse.Lav_PANNER_SHOULD_CROSSFADE
            self._property_instances[_libaudioverse.Lav_PANNER_AZIMUTH] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_PANNER_AZIMUTH)
            self._property_instances[_libaudioverse.Lav_PANNER_CHANNEL_MAP] = FloatArrayProperty(handle = self.handle, slot=_libaudioverse.Lav_PANNER_CHANNEL_MAP, lock = self._lock)
            self._property_instances[_libaudioverse.Lav_PANNER_ELEVATION] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_PANNER_ELEVATION)
            self._property_instances[_libaudioverse.Lav_PANNER_SHOULD_CROSSFADE] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_PANNER_SHOULD_CROSSFADE)


    @property
    def azimuth(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

The horizontal angle of the panner in degrees.
0 is directly ahead, and positive values are clockwise."""
        return self._property_instances[_libaudioverse.Lav_PANNER_AZIMUTH]

    @azimuth.setter
    def azimuth(self, value):
        self.azimuth.value=value



    @property
    def channel_map(self):   
        """Type: float_array

Range: [-INFINITY, INFINITY]

Default value: [-90, 90]

The angles of the speakers in the order in which they are to be mapped to channels.
The first speaker will be mapped to the first channel, the second to the second, etc.
These channels are then combined and produced as the single output of the panner.

You can use floating point infinity to indicate a channel should be skipped.
This functionality is used by all of the standard channel maps to skip the center and LFE channels."""
        return self._property_instances[_libaudioverse.Lav_PANNER_CHANNEL_MAP]

    @channel_map.setter
    def channel_map(self, value):
        self.channel_map.value=value



    @property
    def elevation(self):   
        """Type: float

Range: [-90.0, 90.0]

Default value: 0.0

The vertical angle of the panner in degrees.
0 is horizontal and positive values are upwards.
Note that, for amplitude panners, this has no effect and exists only to allow swapping with the HRTF panner without changing code."""
        return self._property_instances[_libaudioverse.Lav_PANNER_ELEVATION]

    @elevation.setter
    def elevation(self, value):
        self.elevation.value=value



    @property
    def should_crossfade(self):   
        """Type: boolean


Default value: True
Whether or not to instantly move to the new position.
If crossfading is disabled, large movements of the panner will cause audible clicks.
Disabling crossfading can aid performance under heavy workloads, especially with the HRTF panner.
If crossfading is enabled, moving the panner will slowly fade it to the new position over the next block."""
        return self._property_instances[_libaudioverse.Lav_PANNER_SHOULD_CROSSFADE]

    @should_crossfade.setter
    def should_crossfade(self, value):
        self.should_crossfade.value=value



    def configure_standard_map(node, channels):
        r"""Sets the channel map and other properties on this node to match a standard configuration.
The possible standard configurations are found in the :class:`PanningStrategies` enumeration."""
        return _lav.amplitude_panner_node_configure_standard_map(node, channels)



_types_to_classes[ObjectTypes.amplitude_panner_node] = AmplitudePannerNode
class BiquadNode(GenericNode):
    r"""Implementation of a biquad filter section, as defined by the Audio EQ Cookbook by Robert Bristo-Johnson.
This node is capable of implementing almost every filter needed for basic audio effects, including equalizers.
For the specific equations used, see the Audio EQ Cookbook.
It may be found at:
http://www.musicdsp.org/files/Audio-EQ-Cookbook.txt

Inputs:

=====  ================================================  ======================
index  channels                                          description           
=====  ================================================  ======================
0      Depends on arguments to this node's constructor.  The signal to process.
=====  ================================================  ======================

Outputs:

=====  ================================================  ==================================================
index  channels                                          description                                       
=====  ================================================  ==================================================
0      Depends on arguments to this node's constructor.  The result of processing the audio via the filter.
=====  ================================================  ==================================================
"""

    def __init__(self, server, channels):
        super(BiquadNode, self).__init__(_lav.create_biquad_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(BiquadNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["dbgain"] = _libaudioverse.Lav_BIQUAD_DBGAIN
                self._state['properties']["filter_type"] = _libaudioverse.Lav_BIQUAD_FILTER_TYPE
                self._state['properties']["frequency"] = _libaudioverse.Lav_BIQUAD_FREQUENCY
                self._state['properties']["q"] = _libaudioverse.Lav_BIQUAD_Q
            self._property_instances[_libaudioverse.Lav_BIQUAD_DBGAIN] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_BIQUAD_DBGAIN)
            self._property_instances[_libaudioverse.Lav_BIQUAD_FILTER_TYPE] = EnumProperty(handle = self.handle, slot = _libaudioverse.Lav_BIQUAD_FILTER_TYPE, enum = BiquadTypes)
            self._property_instances[_libaudioverse.Lav_BIQUAD_FREQUENCY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_BIQUAD_FREQUENCY)
            self._property_instances[_libaudioverse.Lav_BIQUAD_Q] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_BIQUAD_Q)


    @property
    def dbgain(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

This property is a the gain in decibals to be used with the peaking and shelving filters.
It measures the gain that these filters apply to the part of the signal they boost."""
        return self._property_instances[_libaudioverse.Lav_BIQUAD_DBGAIN]

    @dbgain.setter
    def dbgain(self, value):
        self.dbgain.value=value



    @property
    def filter_type(self):   
        """Type: int

Range: :any:`BiquadTypes`

Default value: :any:`BiquadTypes.lowpass`

The type of the filter.
This determines the interpretations of the other properties on this node."""
        return self._property_instances[_libaudioverse.Lav_BIQUAD_FILTER_TYPE]

    @filter_type.setter
    def filter_type(self, value):
        self.filter_type.value=value



    @property
    def frequency(self):   
        """Type: float

Range: [0, INFINITY]

Default value: 2000.0

This is the frequency of interest.
What specifically this means depends on the selected filter type; for example, it is the cutoff frequency for lowpass and highpass."""
        return self._property_instances[_libaudioverse.Lav_BIQUAD_FREQUENCY]

    @frequency.setter
    def frequency(self, value):
        self.frequency.value=value



    @property
    def q(self):   
        """Type: float

Range: [0.001, INFINITY]

Default value: 0.5

Q is a mathematically complex parameter, a full description of which is beyond the scope of this manual.
Naively, Q can be interpreted as a measure of resonation.
For ``Q<=0.5``, the filter is said to be damped:
it will cut frequencies.
For Q>0.5, however, some frequencies are likely to be boosted.

Q controls the bandwidth for the bandpass and peaking filter types
For everything except the peaking filter, this property follows the normal definition of Q in the electrical engineering literature.
For more specifics, see the Audio EQ Cookbook.
It is found here:
http://www.musicdsp.org/files/Audio-EQ-Cookbook.txt"""
        return self._property_instances[_libaudioverse.Lav_BIQUAD_Q]

    @q.setter
    def q(self, value):
        self.q.value=value





_types_to_classes[ObjectTypes.biquad_node] = BiquadNode
class BlitNode(GenericNode):
    r"""Generates bandlimited impulse trains.  These sound like a buzz, but have important applications in the  alias-free synthesis of analog waveforms.

This node has no inputs.

Outputs:

=====  ========  ============================
index  channels  description                 
=====  ========  ============================
0      1         A bandlimited impulse train.
=====  ========  ============================
"""

    def __init__(self, server):
        super(BlitNode, self).__init__(_lav.create_blit_node(server))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(BlitNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["frequency"] = _libaudioverse.Lav_OSCILLATOR_FREQUENCY
                self._state['properties']["frequency_multiplier"] = _libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER
                self._state['properties']["harmonics"] = _libaudioverse.Lav_BLIT_HARMONICS
                self._state['properties']["phase"] = _libaudioverse.Lav_OSCILLATOR_PHASE
                self._state['properties']["should_normalize"] = _libaudioverse.Lav_BLIT_SHOULD_NORMALIZE
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_FREQUENCY)
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER)
            self._property_instances[_libaudioverse.Lav_BLIT_HARMONICS] = IntProperty(handle = self.handle, slot = _libaudioverse.Lav_BLIT_HARMONICS)
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_PHASE] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_PHASE)
            self._property_instances[_libaudioverse.Lav_BLIT_SHOULD_NORMALIZE] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_BLIT_SHOULD_NORMALIZE)


    @property
    def harmonics(self):   
        """Type: int

Range: [0, MAX_INT]

Default value: 0

The number of harmonics to include.
0 requests automatic adjustment.  When 0, the algorithm this node represents will include as many harmonics as it can without aliasing."""
        return self._property_instances[_libaudioverse.Lav_BLIT_HARMONICS]

    @harmonics.setter
    def harmonics(self, value):
        self.harmonics.value=value



    @property
    def should_normalize(self):   
        """Type: boolean


Default value: True
If false, the produced BLIT will have an integral of 1 over every period.
If true, the produced blit will be normalized to be between 1 and -1, and suitable for audio.
The default is true."""
        return self._property_instances[_libaudioverse.Lav_BLIT_SHOULD_NORMALIZE]

    @should_normalize.setter
    def should_normalize(self, value):
        self.should_normalize.value=value



    @property
    def frequency(self):   
        """Type: float

Range: [0, INFINITY]

Default value: 440.0

The frequency of the impulse train in HZ."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY]

    @frequency.setter
    def frequency(self, value):
        self.frequency.value=value



    @property
    def frequency_multiplier(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 1.0

An additional multiplicative factor applied to the frequency of the oscillator.

This is useful for creating instruments, as the notes of the standard musical scale fall on frequency multiples of a reference pitch, rather than a linear increase."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER]

    @frequency_multiplier.setter
    def frequency_multiplier(self, value):
        self.frequency_multiplier.value=value



    @property
    def phase(self):   
        """Type: float

Range: [0.0, 1.0]

Default value: 0.0

The phase of the impulse train.
This is measured in periods, not in radians."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_PHASE]

    @phase.setter
    def phase(self, value):
        self.phase.value=value





_types_to_classes[ObjectTypes.blit_node] = BlitNode
class BufferNode(GenericNode):
    r"""This node plays a buffer.
The output of this node will have as many channels as the buffer does, so connecting it directly to the server will have the desired effect.

This node has no inputs.

Outputs:

=====  ========================================  ========================================
index  channels                                  description                             
=====  ========================================  ========================================
0      Depends on the currently playing buffer.  The output from the buffer being played.
=====  ========================================  ========================================
"""

    def __init__(self, server):
        super(BufferNode, self).__init__(_lav.create_buffer_node(server))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(BufferNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["buffer"] = _libaudioverse.Lav_BUFFER_BUFFER
                self._state['properties']["ended_count"] = _libaudioverse.Lav_BUFFER_ENDED_COUNT
                self._state['properties']["looping"] = _libaudioverse.Lav_BUFFER_LOOPING
                self._state['properties']["position"] = _libaudioverse.Lav_BUFFER_POSITION
                self._state['properties']["rate"] = _libaudioverse.Lav_BUFFER_RATE
            self._property_instances[_libaudioverse.Lav_BUFFER_BUFFER] = BufferProperty(handle = self.handle, slot = _libaudioverse.Lav_BUFFER_BUFFER)
            self._property_instances[_libaudioverse.Lav_BUFFER_ENDED_COUNT] = IntProperty(handle = self.handle, slot = _libaudioverse.Lav_BUFFER_ENDED_COUNT)
            self._property_instances[_libaudioverse.Lav_BUFFER_LOOPING] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_BUFFER_LOOPING)
            self._property_instances[_libaudioverse.Lav_BUFFER_POSITION] = DoubleProperty(handle = self.handle, slot = _libaudioverse.Lav_BUFFER_POSITION)
            self._property_instances[_libaudioverse.Lav_BUFFER_RATE] = DoubleProperty(handle = self.handle, slot = _libaudioverse.Lav_BUFFER_RATE)


    @property
    def buffer(self):   
        """Type: buffer



The currently playing buffer.
Setting this property will reset position."""
        return self._property_instances[_libaudioverse.Lav_BUFFER_BUFFER]

    @buffer.setter
    def buffer(self, value):
        self.buffer.value=value



    @property
    def ended_count(self):   
        """Type: int

Range: [0, MAX_INT]

Default value: 0

Increments every time the buffer reaches it's end.
If the buffer is not looping, this can be used to determine when the buffer is ended, without using the callback.
if the buffer is configured to loop, the counter will count up every time the end of a loop is reached.
You can write to this property to reset it."""
        return self._property_instances[_libaudioverse.Lav_BUFFER_ENDED_COUNT]

    @ended_count.setter
    def ended_count(self, value):
        self.ended_count.value=value



    @property
    def looping(self):   
        """Type: boolean


Default value: False
If true, this node continues playing the same buffer from the beginning after it reaches the end."""
        return self._property_instances[_libaudioverse.Lav_BUFFER_LOOPING]

    @looping.setter
    def looping(self, value):
        self.looping.value=value



    @property
    def position(self):   
        """Type: double

Range: dynamic

Default value: 0.0

The position of playback, in seconds.
The range of this property corresponds to the total duration of the buffer."""
        return self._property_instances[_libaudioverse.Lav_BUFFER_POSITION]

    @position.setter
    def position(self, value):
        self.position.value=value



    @property
    def rate(self):   
        """Type: double

Range: [0, INFINITY]

Default value: 1.0

A multiplier that applies to playback rate.
1.0 is identity.
Values less than 1.0 cause a decrease in pitch and values greater than 1.0 cause an increase in pitch."""
        return self._property_instances[_libaudioverse.Lav_BUFFER_RATE]

    @rate.setter
    def rate(self, value):
        self.rate.value=value




    def get_end_callback(self):
        r"""Get the end callback.
        
        This is a feature of the Python bindings and is not available in the C API.  See the setter for specific documentation on this callback."""
        with self._lock:
            cb = self._state['callbacks'].get("end", None)
            if cb is None:
                return None
            else:
                return cb[0]

    def set_end_callback(self, callback, additional_args = None, additional_kwargs = None):
        r"""Set the end callback.

Additional_args and additional_kwargs are passed to the callback in addition to any arguments from Libaudioverse.  Note that Libaudioverse always uses positional arguments.

C callback signature: `void  (LavHandle  nodeHandle, void *   userdata)`

Called outside the audio threads every time the buffer reaches the end of the audio data.

Callback parameters:

nodeHandle
  The node which called this callback.

userdata
  The userdata parameter as passed to the setter for this callback.

"""
        with self._lock:
            if callback is None:
                #delete the key, clear the callback with Libaudioverse.
                _lav.buffer_node_set_end_callback(self.handle, None, None)
                del self._state['callbacks']['end']
                return
            if additional_args is None:
                additionnal_args = ()
            if additional_kwargs is None:
                additional_kwargs = dict()
            wrapper = _CallbackWrapper(self, callback, additional_args, additional_kwargs)
            ctypes_callback = _libaudioverse.LavParameterlessCallback(wrapper)
            _lav.buffer_node_set_end_callback(self.handle, ctypes_callback, None)
            #if we get here, we hold both objects; we succeeded in setting because no exception was thrown.
            #As this is just for GC and the getter, we don't deal with the overhead of an object, and just use tuples.
            self._state['callbacks']["end"] = (callback, wrapper, ctypes_callback)

_types_to_classes[ObjectTypes.buffer_node] = BufferNode
class BufferTimelineNode(GenericNode):
    r"""Represents timelines of buffers.

This node provides the ability to schedule buffers to play at any specific time in the future.
This node supports pitch bending scheduled buffers.
There is no limit to the number of buffers which may be scheduled at any given time, and polyphony is supported.

This node has no inputs.

Outputs:

=====  ================================================  ===============================
index  channels                                          description                    
=====  ================================================  ===============================
0      Depends on arguments to this node's constructor.  The sum of all playing buffers.
=====  ================================================  ===============================
"""

    def __init__(self, server, channels):
        super(BufferTimelineNode, self).__init__(_lav.create_buffer_timeline_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(BufferTimelineNode, self).init_with_handle(handle)


    def schedule_buffer(node, buffer, time, pitch_bend):
        r"""Schedule a buffer, optionally with pitch bend.
The time is relative to now."""
        return _lav.buffer_timeline_node_schedule_buffer(node, buffer, time, pitch_bend)



_types_to_classes[ObjectTypes.buffer_timeline_node] = BufferTimelineNode
class ChannelMergerNode(GenericNode):
    r"""Libaudioverse inputs and outputs transport multiple channels of audio, which is usually the desired behavior.
This node, coupled with the :class:`ChannelSplitterNode` , allows advanced applications to manipulate the individual audio channels directly.
The usual workflow is as follows: feed the output of a node through a :class:`ChannelSplitterNode`,
modify the channels individually, and then merge them with this node.

The number of inputs to this node depends on parameters to its constructor.

Outputs:

=====  ================================================  =========================================
index  channels                                          description                              
=====  ================================================  =========================================
0      Depends on arguments to this node's constructor.  The result of merging the input channels.
=====  ================================================  =========================================
"""

    def __init__(self, server, channels):
        super(ChannelMergerNode, self).__init__(_lav.create_channel_merger_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(ChannelMergerNode, self).init_with_handle(handle)




_types_to_classes[ObjectTypes.channel_merger_node] = ChannelMergerNode
class ChannelSplitterNode(GenericNode):
    r"""Libaudioverse inputs and outputs transport multiple channels of audio, which is usually the desired behavior.
This node, coupled with the :class:`ChannelMergerNode`, allows advanced applications to manipulate the individual audio channels directly.
The usual workflow is as follows: feed the output of a node through this node,
modify the channels individually, and then merge them with a :class:`ChannelMergerNode`.

Inputs:

=====  ================================================  ============================================
index  channels                                          description                                 
=====  ================================================  ============================================
0      Depends on arguments to this node's constructor.  The signal to split into component channels.
=====  ================================================  ============================================

The number of outputs from this node depends on parameters to its constructor.
"""

    def __init__(self, server, channels):
        super(ChannelSplitterNode, self).__init__(_lav.create_channel_splitter_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(ChannelSplitterNode, self).init_with_handle(handle)




_types_to_classes[ObjectTypes.channel_splitter_node] = ChannelSplitterNode
class ConvolverNode(GenericNode):
    r"""A simple convolver.

This implements convolution directly, without use of the FFT.

Inputs:

=====  ================================================  ===========================
index  channels                                          description                
=====  ================================================  ===========================
0      Depends on arguments to this node's constructor.  The signal to be convolved.
=====  ================================================  ===========================

Outputs:

=====  ================================================  =====================
index  channels                                          description          
=====  ================================================  =====================
0      Depends on arguments to this node's constructor.  The convolved signal.
=====  ================================================  =====================
"""

    def __init__(self, server, channels):
        super(ConvolverNode, self).__init__(_lav.create_convolver_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(ConvolverNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["impulse_response"] = _libaudioverse.Lav_CONVOLVER_IMPULSE_RESPONSE
            self._property_instances[_libaudioverse.Lav_CONVOLVER_IMPULSE_RESPONSE] = FloatArrayProperty(handle = self.handle, slot=_libaudioverse.Lav_CONVOLVER_IMPULSE_RESPONSE, lock = self._lock)


    @property
    def impulse_response(self):   
        """Type: float_array

Range: [-INFINITY, INFINITY]

Default value: [1.0]

The impulse response to convolve the input with."""
        return self._property_instances[_libaudioverse.Lav_CONVOLVER_IMPULSE_RESPONSE]

    @impulse_response.setter
    def impulse_response(self, value):
        self.impulse_response.value=value





_types_to_classes[ObjectTypes.convolver_node] = ConvolverNode
class CrossfaderNode(GenericNode):
    r"""A crossfader is a node  which allows for selection of exactly one input.
The selection can be changed by crossfading, a technique whereby the currently selected input is slowly faded out and the new one faded in.

By using crossfades of no duration, this node can also be made to function as a switch or selector, selecting an input from among the connected nodes.
This particular case is optimized, and special support is implemented via allowing you to write directly to the ``current_input`` property.

This crossfader has a configurable number of inputs.
All inputs and the single output have the same channel count.
These are both configurable via parameters to the constructor.

The number of inputs to this node depends on parameters to its constructor.

Outputs:

=====  ======================================================  ============================
index  channels                                                description                 
=====  ======================================================  ============================
0      Depends on the channel count given to the constructor.  The output of the crossfade.
=====  ======================================================  ============================
"""

    def __init__(self, server, channels, inputs):
        super(CrossfaderNode, self).__init__(_lav.create_crossfader_node(server, channels, inputs))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(CrossfaderNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["current_input"] = _libaudioverse.Lav_CROSSFADER_CURRENT_INPUT
                self._state['properties']["is_crossfading"] = _libaudioverse.Lav_CROSSFADER_IS_CROSSFADING
                self._state['properties']["target_input"] = _libaudioverse.Lav_CROSSFADER_TARGET_INPUT
            self._property_instances[_libaudioverse.Lav_CROSSFADER_CURRENT_INPUT] = IntProperty(handle = self.handle, slot = _libaudioverse.Lav_CROSSFADER_CURRENT_INPUT)
            self._property_instances[_libaudioverse.Lav_CROSSFADER_IS_CROSSFADING] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_CROSSFADER_IS_CROSSFADING)
            self._property_instances[_libaudioverse.Lav_CROSSFADER_TARGET_INPUT] = IntProperty(handle = self.handle, slot = _libaudioverse.Lav_CROSSFADER_TARGET_INPUT)


    @property
    def current_input(self):   
        """Type: int

Range: dynamic

Default value: 0

The currently active input.

Writing to this property is equivalent to crossfading with a time of 0.
Note that the output is a combination of the current and target inputs while crossfading."""
        return self._property_instances[_libaudioverse.Lav_CROSSFADER_CURRENT_INPUT]

    @current_input.setter
    def current_input(self, value):
        self.current_input.value=value



    @property
    def is_crossfading(self):   
        """Type: boolean


Default value: False
True if we are crossfading, otherwise false."""
        return self._property_instances[_libaudioverse.Lav_CROSSFADER_IS_CROSSFADING]

    @is_crossfading.setter
    def is_crossfading(self, value):
        self.is_crossfading.value=value



    @property
    def target_input(self):   
        """Type: int

This property is read-only.

The input which the current crossfade is headed for.

When not crossfading, this property is meaningless."""
        return self._property_instances[_libaudioverse.Lav_CROSSFADER_TARGET_INPUT]




    def crossfade(node, duration, input):
        r"""Begin a crossfade.

if a crossfade is currently inn progress, it finishes immediately and fires the event.

Using a duration of 0 is an instantaneous crossfade, equivalent to writing directly to the current_input property.
Crossfades of duration 0 do not fire the finished event."""
        return _lav.crossfader_node_crossfade(node, duration, input)


    def get_finished_callback(self):
        r"""Get the finished callback.
        
        This is a feature of the Python bindings and is not available in the C API.  See the setter for specific documentation on this callback."""
        with self._lock:
            cb = self._state['callbacks'].get("finished", None)
            if cb is None:
                return None
            else:
                return cb[0]

    def set_finished_callback(self, callback, additional_args = None, additional_kwargs = None):
        r"""Set the finished callback.

Additional_args and additional_kwargs are passed to the callback in addition to any arguments from Libaudioverse.  Note that Libaudioverse always uses positional arguments.

C callback signature: `void  (LavHandle  nodeHandle, void *   userdata)`

Called outside the audio thread when the currently scheduled crossfade finishes.

Callback parameters:

nodeHandle
  The node which called this callback.

userdata
  The userdata parameter as passed to the setter for this callback.

"""
        with self._lock:
            if callback is None:
                #delete the key, clear the callback with Libaudioverse.
                _lav.crossfader_node_set_finished_callback(self.handle, None, None)
                del self._state['callbacks']['finished']
                return
            if additional_args is None:
                additionnal_args = ()
            if additional_kwargs is None:
                additional_kwargs = dict()
            wrapper = _CallbackWrapper(self, callback, additional_args, additional_kwargs)
            ctypes_callback = _libaudioverse.LavParameterlessCallback(wrapper)
            _lav.crossfader_node_set_finished_callback(self.handle, ctypes_callback, None)
            #if we get here, we hold both objects; we succeeded in setting because no exception was thrown.
            #As this is just for GC and the getter, we don't deal with the overhead of an object, and just use tuples.
            self._state['callbacks']["finished"] = (callback, wrapper, ctypes_callback)

_types_to_classes[ObjectTypes.crossfader_node] = CrossfaderNode
class CrossfadingDelayNode(GenericNode):
    r"""Implements a crossfading delay line.
Delay lines have uses in echo and reverb, as well as many more esoteric effects.

Inputs:

=====  ================================================  ====================
index  channels                                          description         
=====  ================================================  ====================
0      Depends on arguments to this node's constructor.  The signal to delay.
=====  ================================================  ====================

Outputs:

=====  ================================================  ===================
index  channels                                          description        
=====  ================================================  ===================
0      Depends on arguments to this node's constructor.  The delayed signal.
=====  ================================================  ===================
"""

    def __init__(self, server, max_delay, channels):
        super(CrossfadingDelayNode, self).__init__(_lav.create_crossfading_delay_node(server, max_delay, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(CrossfadingDelayNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["delay"] = _libaudioverse.Lav_DELAY_DELAY
                self._state['properties']["delay_max"] = _libaudioverse.Lav_DELAY_DELAY_MAX
                self._state['properties']["feedback"] = _libaudioverse.Lav_DELAY_FEEDBACK
                self._state['properties']["interpolation_time"] = _libaudioverse.Lav_DELAY_INTERPOLATION_TIME
            self._property_instances[_libaudioverse.Lav_DELAY_DELAY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_DELAY_DELAY)
            self._property_instances[_libaudioverse.Lav_DELAY_DELAY_MAX] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_DELAY_DELAY_MAX)
            self._property_instances[_libaudioverse.Lav_DELAY_FEEDBACK] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_DELAY_FEEDBACK)
            self._property_instances[_libaudioverse.Lav_DELAY_INTERPOLATION_TIME] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_DELAY_INTERPOLATION_TIME)


    @property
    def delay(self):   
        """Type: float

Range: dynamic

Default value: 0.0

The delay of the delay line in seconds.
The range of this property depends on the maxDelay parameter to the constructor.

Note that values less than 1 sample still introduce delay."""
        return self._property_instances[_libaudioverse.Lav_DELAY_DELAY]

    @delay.setter
    def delay(self, value):
        self.delay.value=value



    @property
    def delay_max(self):   
        """Type: float

This property is read-only.

The max delay as set at the node's creation time."""
        return self._property_instances[_libaudioverse.Lav_DELAY_DELAY_MAX]




    @property
    def feedback(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

The feedback coefficient.
The output of the delay line is fed back into the delay line, multiplied by this coefficient.
Setting feedback to small values can make echoes, comb filters, and a variety of other effects."""
        return self._property_instances[_libaudioverse.Lav_DELAY_FEEDBACK]

    @feedback.setter
    def feedback(self, value):
        self.feedback.value=value



    @property
    def interpolation_time(self):   
        """Type: float

Range: [0.001, INFINITY]

Default value: 0.001

When the delay property is changed, the delay line crossfades between the old position and the new one.
This property sets how long this crossfade will take.
Note that for this node, it is impossible to get rid of the crossfade completely."""
        return self._property_instances[_libaudioverse.Lav_DELAY_INTERPOLATION_TIME]

    @interpolation_time.setter
    def interpolation_time(self, value):
        self.interpolation_time.value=value





_types_to_classes[ObjectTypes.crossfading_delay_node] = CrossfadingDelayNode
class DcBlockerNode(GenericNode):
    r"""A DC blocker.
This is a first-order filter, the best possible within numerical limits.
It consists of a zero at DC, and a pole as close to DC as we can put it.
For any sampling rate, this node is the best first-order section for DC removal possible.

Inputs:

=====  ================================================  ======================
index  channels                                          description           
=====  ================================================  ======================
0      Depends on arguments to this node's constructor.  A signal with some DC.
=====  ================================================  ======================

Outputs:

=====  ================================================  =======================================================
index  channels                                          description                                            
=====  ================================================  =======================================================
0      Depends on arguments to this node's constructor.  The same signal with DC cut using a first-order filter.
=====  ================================================  =======================================================
"""

    def __init__(self, server, channels):
        super(DcBlockerNode, self).__init__(_lav.create_dc_blocker_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(DcBlockerNode, self).init_with_handle(handle)




_types_to_classes[ObjectTypes.dc_blocker_node] = DcBlockerNode
class DoppleringDelayNode(GenericNode):
    r"""Implements a dopplering delay line, an interpolated delay line that intensionally bends pitch when the delay changes.
Delay lines have uses in echo and reverb, as well as many more esoteric effects.

Inputs:

=====  ================================================  ====================
index  channels                                          description         
=====  ================================================  ====================
0      Depends on arguments to this node's constructor.  The signal to delay.
=====  ================================================  ====================

Outputs:

=====  ================================================  ===================
index  channels                                          description        
=====  ================================================  ===================
0      Depends on arguments to this node's constructor.  The delayed signal.
=====  ================================================  ===================
"""

    def __init__(self, server, max_delay, channels):
        super(DoppleringDelayNode, self).__init__(_lav.create_dopplering_delay_node(server, max_delay, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(DoppleringDelayNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["delay"] = _libaudioverse.Lav_DELAY_DELAY
                self._state['properties']["delay_max"] = _libaudioverse.Lav_DELAY_DELAY_MAX
                self._state['properties']["interpolation_time"] = _libaudioverse.Lav_DELAY_INTERPOLATION_TIME
            self._property_instances[_libaudioverse.Lav_DELAY_DELAY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_DELAY_DELAY)
            self._property_instances[_libaudioverse.Lav_DELAY_DELAY_MAX] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_DELAY_DELAY_MAX)
            self._property_instances[_libaudioverse.Lav_DELAY_INTERPOLATION_TIME] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_DELAY_INTERPOLATION_TIME)


    @property
    def delay(self):   
        """Type: float

Range: dynamic

Default value: 0.0

The delay of the delay line in seconds.
The range of this property depends on the maxDelay parameter to the constructor.

Note that values less than 1 sample still introduce delay."""
        return self._property_instances[_libaudioverse.Lav_DELAY_DELAY]

    @delay.setter
    def delay(self, value):
        self.delay.value=value



    @property
    def delay_max(self):   
        """Type: float

This property is read-only.

The max delay as set at the node's creation time."""
        return self._property_instances[_libaudioverse.Lav_DELAY_DELAY_MAX]




    @property
    def interpolation_time(self):   
        """Type: float

Range: [0.001, INFINITY]

Default value: 0.01

When the delay property is changed, the delay line moves the delay to the new position.
This property sets how long this  will take.
Note that for this node, it is impossible to get rid of the crossfade completely.

On this delay line, the interpolation time is the total duration of a pitch bend caused by moving the delay."""
        return self._property_instances[_libaudioverse.Lav_DELAY_INTERPOLATION_TIME]

    @interpolation_time.setter
    def interpolation_time(self, value):
        self.interpolation_time.value=value





_types_to_classes[ObjectTypes.dopplering_delay_node] = DoppleringDelayNode
class EnvironmentNode(GenericNode):
    r"""This is the entry point to the 3D simulation capabilities.
Environment nodes hold the information needed to pan sources, as well as acting as an aggregate output for all sources that use this environment.


Note that the various properties for default values do not affect already created sources.
It is best to configure these first.
Any functionality to change a property on all sources needs to be implemented by the app, and is not offered by Libaudioverse.

This node has no inputs.

Outputs:

=====  ========================================  =================================
index  channels                                  description                      
=====  ========================================  =================================
0      Depends on the output_channels property.  The output of the 3D environment.
=====  ========================================  =================================
"""

    def __init__(self, server, hrtf_path):
        super(EnvironmentNode, self).__init__(_lav.create_environment_node(server, hrtf_path))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(EnvironmentNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["default_reverb_distance"] = _libaudioverse.Lav_ENVIRONMENT_REVERB_DISTANCE
                self._state['properties']["default_size"] = _libaudioverse.Lav_ENVIRONMENT_DEFAULT_SIZE
                self._state['properties']["distance_model"] = _libaudioverse.Lav_ENVIRONMENT_DISTANCE_MODEL
                self._state['properties']["max_distance"] = _libaudioverse.Lav_ENVIRONMENT_MAX_DISTANCE
                self._state['properties']["max_reverb_level"] = _libaudioverse.Lav_ENVIRONMENT_MAX_REVERB_LEVEL
                self._state['properties']["min_reverb_level"] = _libaudioverse.Lav_ENVIRONMENT_MIN_REVERB_LEVEL
                self._state['properties']["orientation"] = _libaudioverse.Lav_ENVIRONMENT_ORIENTATION
                self._state['properties']["output_channels"] = _libaudioverse.Lav_ENVIRONMENT_OUTPUT_CHANNELS
                self._state['properties']["panning_strategy"] = _libaudioverse.Lav_ENVIRONMENT_PANNING_STRATEGY
                self._state['properties']["position"] = _libaudioverse.Lav_ENVIRONMENT_POSITION
            self._property_instances[_libaudioverse.Lav_ENVIRONMENT_REVERB_DISTANCE] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_ENVIRONMENT_REVERB_DISTANCE)
            self._property_instances[_libaudioverse.Lav_ENVIRONMENT_DEFAULT_SIZE] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_ENVIRONMENT_DEFAULT_SIZE)
            self._property_instances[_libaudioverse.Lav_ENVIRONMENT_DISTANCE_MODEL] = EnumProperty(handle = self.handle, slot = _libaudioverse.Lav_ENVIRONMENT_DISTANCE_MODEL, enum = DistanceModels)
            self._property_instances[_libaudioverse.Lav_ENVIRONMENT_MAX_DISTANCE] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_ENVIRONMENT_MAX_DISTANCE)
            self._property_instances[_libaudioverse.Lav_ENVIRONMENT_MAX_REVERB_LEVEL] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_ENVIRONMENT_MAX_REVERB_LEVEL)
            self._property_instances[_libaudioverse.Lav_ENVIRONMENT_MIN_REVERB_LEVEL] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_ENVIRONMENT_MIN_REVERB_LEVEL)
            self._property_instances[_libaudioverse.Lav_ENVIRONMENT_ORIENTATION] = Float6Property(handle = self.handle, slot = _libaudioverse.Lav_ENVIRONMENT_ORIENTATION)
            self._property_instances[_libaudioverse.Lav_ENVIRONMENT_OUTPUT_CHANNELS] = IntProperty(handle = self.handle, slot = _libaudioverse.Lav_ENVIRONMENT_OUTPUT_CHANNELS)
            self._property_instances[_libaudioverse.Lav_ENVIRONMENT_PANNING_STRATEGY] = EnumProperty(handle = self.handle, slot = _libaudioverse.Lav_ENVIRONMENT_PANNING_STRATEGY, enum = PanningStrategies)
            self._property_instances[_libaudioverse.Lav_ENVIRONMENT_POSITION] = Float3Property(handle = self.handle, slot = _libaudioverse.Lav_ENVIRONMENT_POSITION)


    @property
    def default_size(self):   
        """Type: float

Range: [0.0, INFINITY]

Default value: 0.0

The default size for new sources.
Sources aare approximated as spheres, with 0 being the special case of a point source.
Size is used to determine the listener's distance from a source."""
        return self._property_instances[_libaudioverse.Lav_ENVIRONMENT_DEFAULT_SIZE]

    @default_size.setter
    def default_size(self, value):
        self.default_size.value=value



    @property
    def distance_model(self):   
        """Type: int

Range: :any:`DistanceModels`

Default value: :any:`DistanceModels.linear`

Distance models control how quickly sources get quieter as they move away from the listener.

By default, sources are configured to delegate to the environment when looking for values to use for the distance model parameters.
This behavior may be changed by setting ``Lav_SOURCE_CONTROL_DISTANCE_MODEL`` to true."""
        return self._property_instances[_libaudioverse.Lav_ENVIRONMENT_DISTANCE_MODEL]

    @distance_model.setter
    def distance_model(self, value):
        self.distance_model.value=value



    @property
    def max_distance(self):   
        """Type: float

Range: [0.0, INFINITY]

Default value: 150.0

The maximum distance at which a source is audible.
Consider this property to be in meters.

By default, sources are configured to delegate to the environment when looking for values to use for the distance model parameters.
This behavior may be changed by setting ``Lav_SOURCE_CONTROL_DISTANCE_MODEL`` to true."""
        return self._property_instances[_libaudioverse.Lav_ENVIRONMENT_MAX_DISTANCE]

    @max_distance.setter
    def max_distance(self, value):
        self.max_distance.value=value



    @property
    def max_reverb_level(self):   
        """Type: float

Range: [0.0, 1.0]

Default value: 0.6

The maximum amount of audio to be diverted to reverb sends, if any.

Behavior is undefined if this property is ever less than Lav_ENVIRONMENT_MIN_REVERB_LEVEL.

By default, sources look to their environmlent for the value of this property.
If you wish to set it on a per-source basis, set ``Lav_SOURCE_CONTROL_REVERB`` to true on the source."""
        return self._property_instances[_libaudioverse.Lav_ENVIRONMENT_MAX_REVERB_LEVEL]

    @max_reverb_level.setter
    def max_reverb_level(self, value):
        self.max_reverb_level.value=value



    @property
    def min_reverb_level(self):   
        """Type: float

Range: [0.0, 1.0]

Default value: 0.15

The minimum reverb level allowed.

if a send is configured to be a reverb send, this is the minimum amount of audio that will be diverted to it.

Behavior is undefined if this property is ever greater than the value of Lav_ENVIRONMENT_MAX_REVERB_LEVEL.

By default, sources look to their environmlent for the value of this property.
If you wish to set it on a per-source basis, set ``Lav_SOURCE_CONTROL_REVERB`` to true on the source."""
        return self._property_instances[_libaudioverse.Lav_ENVIRONMENT_MIN_REVERB_LEVEL]

    @min_reverb_level.setter
    def min_reverb_level(self, value):
        self.min_reverb_level.value=value



    @property
    def orientation(self):   
        """Type: float6


Default value: [0.0, 0.0, -1.0, 0.0, 1.0, 0.0]

The orientation of the listener.
The first three elements are a vector representing the direction in which the listener is looking
and the second 3 a vector representing the direction in which a rod pointing out of the top of the listener's head would be pointing

This property packs these vectors because they must never be modified separately.
Additionally, they should both be unit vectors and must also be orthoganal.

the default situates the listener such that positive x is right, positive y is up, and positive z is behind the listener.
The setting (0, 1, 0, 0, 0, 1) will situate the listener such that
positive x is right and positive y is forward.
For those not familiar with trigonometry and who wish to consider positive x east and positivve y north, the following formula
will turn the listener to face a scertain direction specified in radians clockwise of north:
(sin(theta), cos(theta), 0, 0, 0, 1).
As usual, note that radians=degrees*PI/180."""
        return self._property_instances[_libaudioverse.Lav_ENVIRONMENT_ORIENTATION]

    @orientation.setter
    def orientation(self, value):
        self.orientation.value=value



    @property
    def output_channels(self):   
        """Type: int

Range: [0, 8]

Default value: 2

Environments are not smart enough to determine the number of channels their output needs to have.
If you are using something greater than stereo, i.e. 5.1, you need to change this property.
The specific issue solved by this property is the case in which one source is set to something different than all others,
or where the app changes the panning strategies of sources after creation.

Values besides 2, 4, 6, or 8 do not usually have much meaning."""
        return self._property_instances[_libaudioverse.Lav_ENVIRONMENT_OUTPUT_CHANNELS]

    @output_channels.setter
    def output_channels(self, value):
        self.output_channels.value=value



    @property
    def panning_strategy(self):   
        """Type: int

Range: :any:`PanningStrategies`

Default value: :any:`PanningStrategies.stereo`

The panning strategy for any source configured to delegate to the environment.
All new sources delegate to the environment by default.

If you want to change this property for a specific source, set ``Lav_SOURCE_CONTROL_PANNING`` on the source to true."""
        return self._property_instances[_libaudioverse.Lav_ENVIRONMENT_PANNING_STRATEGY]

    @panning_strategy.setter
    def panning_strategy(self, value):
        self.panning_strategy.value=value



    @property
    def position(self):   
        """Type: float3


Default value: [0.0, 0.0, 0.0]

The position of the listener, in world coordinates."""
        return self._property_instances[_libaudioverse.Lav_ENVIRONMENT_POSITION]

    @position.setter
    def position(self, value):
        self.position.value=value



    @property
    def default_reverb_distance(self):   
        """Type: float

Range: [0.0, INFINITY]

Default value: 75.0

The distance at which a source will be heard only in the reverb.

See documentation on the :class:`SourceNode` node for a specific explanation.
By default, sources get the value of this property from the environment.
To control this property on a per-source basis, set ``Lav_SOURCE_CONTROL_REVERB`` to true on the source."""
        return self._property_instances[_libaudioverse.Lav_ENVIRONMENT_REVERB_DISTANCE]

    @default_reverb_distance.setter
    def default_reverb_distance(self, value):
        self.default_reverb_distance.value=value



    def add_effect_send(node, channels, is_reverb, connect_by_default):
        r"""Add an effect send.

Effect sends are aggregates of all sources configured to make use of them.
This function's return value is the index of the newly created effecct send.

The world gains an additional output for every added effect send.
This output aggregates all audio of sources configured to send to it, including the panning effects on those sources.
The returned index is the number of the newly created output.

Two special cases are worth noting.

First, a mono effect send includes all sources with only attenuation applied.

Second, if the effect send has 4 channels, it may be configured to be a reverb effect send with the *is_reverb* parameter.
Reverb effect sends are treated differently in terms of attenuation:
as sources move away from the listener, their dry path becomes less but the audio sent to the reverb effect send becomes greater.

No effect send can include occlusion effects."""
        return _lav.environment_node_add_effect_send(node, channels, is_reverb, connect_by_default)

    def play_async(node, buffer, x, y, z, is_dry):
        r"""Play a buffer, using the specified position and the currently set defaults on the world for distance model and panning strategy.
This is the same as creating a buffer and a source, but Libaudioverse retains control of these objects.
When the buffer finishes playing, the source is automatically disposed of."""
        return _lav.environment_node_play_async(node, buffer, x, y, z, is_dry)



_types_to_classes[ObjectTypes.environment_node] = EnvironmentNode
class FdnReverbNode(GenericNode):
    r"""An 8 delay line FDN reverberator, based off a householder reflection.

This reverb takes as its input and outputs ats its output quadraphonic audio.
Panning effects will still be observed at the output with some bias.
If a stereo signal is fed into the reverb and the reverb is likewise connected to a stereo output, the input signal's volume will effectively be halved.

Inputs:

=====  ========  ==============================
index  channels  description                   
=====  ========  ==============================
0      4         The signal to apply reverb to.
=====  ========  ==============================

Outputs:

=====  ========  ===============================
index  channels  description                    
=====  ========  ===============================
0      4         The signal with reverb applied.
=====  ========  ===============================
"""

    def __init__(self, server):
        super(FdnReverbNode, self).__init__(_lav.create_fdn_reverb_node(server))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(FdnReverbNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["cutoff_frequency"] = _libaudioverse.Lav_FDN_REVERB_CUTOFF_FREQUENCY
                self._state['properties']["delay_modulation_depth"] = _libaudioverse.Lav_FDN_REVERB_DELAY_MODULATION_DEPTH
                self._state['properties']["delay_modulation_frequency"] = _libaudioverse.Lav_FDN_REVERB_DELAY_MODULATION_FREQUENCY
                self._state['properties']["density"] = _libaudioverse.Lav_FDN_REVERB_DENSITY
                self._state['properties']["t60"] = _libaudioverse.Lav_FDN_REVERB_T60
            self._property_instances[_libaudioverse.Lav_FDN_REVERB_CUTOFF_FREQUENCY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FDN_REVERB_CUTOFF_FREQUENCY)
            self._property_instances[_libaudioverse.Lav_FDN_REVERB_DELAY_MODULATION_DEPTH] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FDN_REVERB_DELAY_MODULATION_DEPTH)
            self._property_instances[_libaudioverse.Lav_FDN_REVERB_DELAY_MODULATION_FREQUENCY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FDN_REVERB_DELAY_MODULATION_FREQUENCY)
            self._property_instances[_libaudioverse.Lav_FDN_REVERB_DENSITY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FDN_REVERB_DENSITY)
            self._property_instances[_libaudioverse.Lav_FDN_REVERB_T60] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FDN_REVERB_T60)


    @property
    def cutoff_frequency(self):   
        """Type: float

Range: dynamic

Default value: 5000

Controls the frequencies of lowpass filters on the feedback path of the reverb.
Lowering this property leads to softer and less harsh reverb."""
        return self._property_instances[_libaudioverse.Lav_FDN_REVERB_CUTOFF_FREQUENCY]

    @cutoff_frequency.setter
    def cutoff_frequency(self, value):
        self.cutoff_frequency.value=value



    @property
    def delay_modulation_depth(self):   
        """Type: float

Range: [0.0, 1.0]

Default value: 0.0

Controls how deep the modulation of the delay lines is.
Increasing this property slightly makes the late reverb sound less metallic, while extremely high values add chorus-like effects.
This property acts as a multiplier, and the correspondance between it and physical units is intentionally left unspecified."""
        return self._property_instances[_libaudioverse.Lav_FDN_REVERB_DELAY_MODULATION_DEPTH]

    @delay_modulation_depth.setter
    def delay_modulation_depth(self, value):
        self.delay_modulation_depth.value=value



    @property
    def delay_modulation_frequency(self):   
        """Type: float

Range: [0.0, 500.0]

Default value: 10.0

Controls how fast the internal delay lines modulate."""
        return self._property_instances[_libaudioverse.Lav_FDN_REVERB_DELAY_MODULATION_FREQUENCY]

    @delay_modulation_frequency.setter
    def delay_modulation_frequency(self, value):
        self.delay_modulation_frequency.value=value



    @property
    def density(self):   
        """Type: float

Range: [0.0, 1.0]

Default value: 0.5

Controls the density of the reverb.
Extremely low values sound "grainy"; extremely high values tend to resonate."""
        return self._property_instances[_libaudioverse.Lav_FDN_REVERB_DENSITY]

    @density.setter
    def density(self, value):
        self.density.value=value



    @property
    def t60(self):   
        """Type: float

Range: [0.0, INFINITY]

Default value: 1.0

The ``t60`` is the time it takes the reverb to decay by 60 decibals."""
        return self._property_instances[_libaudioverse.Lav_FDN_REVERB_T60]

    @t60.setter
    def t60(self, value):
        self.t60.value=value





_types_to_classes[ObjectTypes.fdn_reverb_node] = FdnReverbNode
class FeedbackDelayNetworkNode(GenericNode):
    r"""Implements a feedback delay network.
This is possibly the single-most complicated node in Libaudioverse, and full documentation of it goes well beyond the manual.
Unless you know  what a  feedback delay network is and have a specific reason for using one, this node will probably not help you.

This node has `n` inputs and outputs, where `n` is the `lines` parameter to the constructor.
Each input and output pair represent the input and output of a specific delay line, respectively.

The inputs of this node are described above.

The  outputs from this node are described above.
"""

    def __init__(self, server, max_delay, channels):
        super(FeedbackDelayNetworkNode, self).__init__(_lav.create_feedback_delay_network_node(server, max_delay, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(FeedbackDelayNetworkNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["delays"] = _libaudioverse.Lav_FDN_DELAYS
                self._state['properties']["filter_frequencies"] = _libaudioverse.Lav_FDN_FILTER_FREQUENCIES
                self._state['properties']["filter_types"] = _libaudioverse.Lav_FDN_FILTER_TYPES
                self._state['properties']["matrix"] = _libaudioverse.Lav_FDN_MATRIX
                self._state['properties']["max_delay"] = _libaudioverse.Lav_FDN_MAX_DELAY
                self._state['properties']["output_gains"] = _libaudioverse.Lav_FDN_OUTPUT_GAINS
            self._property_instances[_libaudioverse.Lav_FDN_DELAYS] = FloatArrayProperty(handle = self.handle, slot=_libaudioverse.Lav_FDN_DELAYS, lock = self._lock)
            self._property_instances[_libaudioverse.Lav_FDN_FILTER_FREQUENCIES] = FloatArrayProperty(handle = self.handle, slot=_libaudioverse.Lav_FDN_FILTER_FREQUENCIES, lock = self._lock)
            self._property_instances[_libaudioverse.Lav_FDN_FILTER_TYPES] = IntArrayProperty(handle = self.handle, slot=_libaudioverse.Lav_FDN_FILTER_TYPES, lock = self._lock)
            self._property_instances[_libaudioverse.Lav_FDN_MATRIX] = FloatArrayProperty(handle = self.handle, slot=_libaudioverse.Lav_FDN_MATRIX, lock = self._lock)
            self._property_instances[_libaudioverse.Lav_FDN_MAX_DELAY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FDN_MAX_DELAY)
            self._property_instances[_libaudioverse.Lav_FDN_OUTPUT_GAINS] = FloatArrayProperty(handle = self.handle, slot=_libaudioverse.Lav_FDN_OUTPUT_GAINS, lock = self._lock)


    @property
    def delays(self):   
        """Type: float_array



The lengths of the delay lines in seconds.
This array must be ``channels`` long.
All values must be positive and no more than the maximum delay specified to the constructor."""
        return self._property_instances[_libaudioverse.Lav_FDN_DELAYS]

    @delays.setter
    def delays(self, value):
        self.delays.value=value



    @property
    def filter_frequencies(self):   
        """Type: float_array



The frequencies of the filters.
The range of this property is 0 to Nyquist, or half the sampling rate."""
        return self._property_instances[_libaudioverse.Lav_FDN_FILTER_FREQUENCIES]

    @filter_frequencies.setter
    def filter_frequencies(self, value):
        self.filter_frequencies.value=value



    @property
    def filter_types(self):   
        """Type: int_array

Range: :any:`FdnFilterTypes`


Allows insertion of filters in the feedback paths.
These filters can be individually enabled and disabled; the default is disabled."""
        return self._property_instances[_libaudioverse.Lav_FDN_FILTER_TYPES]

    @filter_types.setter
    def filter_types(self, value):
        self.filter_types.value=value



    @property
    def matrix(self):   
        """Type: float_array



The feedback matrix.

A column vector is formed by reading all delay lines.
This vector is multiplied by this matrix, and then fed back into the delay lines.

The matrix is stored in row-major order.
The supplied array must have a length equal to the square of the channels specified to the constructor."""
        return self._property_instances[_libaudioverse.Lav_FDN_MATRIX]

    @matrix.setter
    def matrix(self, value):
        self.matrix.value=value



    @property
    def max_delay(self):   
        """Type: float

This property is read-only.

The maximum delay any of the internal delay lines may be set to."""
        return self._property_instances[_libaudioverse.Lav_FDN_MAX_DELAY]




    @property
    def output_gains(self):   
        """Type: float_array



Allows control of the individual gains of the output.
These gains do not apply to the feedback path and are only for controlling relative output levels.
The array for this property allows any floating point values, and must be exactly `channels` long."""
        return self._property_instances[_libaudioverse.Lav_FDN_OUTPUT_GAINS]

    @output_gains.setter
    def output_gains(self, value):
        self.output_gains.value=value





_types_to_classes[ObjectTypes.feedback_delay_network_node] = FeedbackDelayNetworkNode
class FftConvolverNode(GenericNode):
    r"""A convolver for long impulse responses.

This convolver uses the overlap-add convolution algorithm.
It is slower than the :class:`ConvolverNode` for small impulse responses.

The difference between this node and the :class:`ConvolverNode` is the complexity of the algorithm.
This node is capable of handling impulses longer than a second, a case for which the :class:`ConvolverNode` will fail to run in realtime.

Furthermore, as the most common operation for this node is reverb, it is possible to set each channel's response separately.

Inputs:

=====  ================================================  ===========================
index  channels                                          description                
=====  ================================================  ===========================
0      Depends on arguments to this node's constructor.  The signal to be convolved.
=====  ================================================  ===========================

Outputs:

=====  ================================================  =====================
index  channels                                          description          
=====  ================================================  =====================
0      Depends on arguments to this node's constructor.  The convolved signal.
=====  ================================================  =====================
"""

    def __init__(self, server, channels):
        super(FftConvolverNode, self).__init__(_lav.create_fft_convolver_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(FftConvolverNode, self).init_with_handle(handle)


    def set_response(node, channel, length, response):
        r"""Set the response for a specific channel."""
        return _lav.fft_convolver_node_set_response(node, channel, length, response)

    def set_response_from_file(node, path, file_channel, convolver_channel):
        r"""Set the impulse response for a specific channel of this node from a file."""
        return _lav.fft_convolver_node_set_response_from_file(node, path, file_channel, convolver_channel)



_types_to_classes[ObjectTypes.fft_convolver_node] = FftConvolverNode
class FileStreamerNode(GenericNode):
    r"""Streams a file, which must be specified to the constructor and cannot be changed thereafter.

This node is a stopgap solution, and should be considered temporary.
It will likely remain for backward compatibility.
Libaudioverse plans to eventually offer a more generic streaming node that also supports web addresses; such a node will have a completely different, less buffer-like interface.

In order to stream a file, it must be passed through a resampler.
Consequentlty, the position property is slightly inaccurate and the ended property and callback are slightly delayed.

This node has no inputs.

Outputs:

=====  ====================  =========================
index  channels              description              
=====  ====================  =========================
0      Depends on the file.  The output of the stream.
=====  ====================  =========================
"""

    def __init__(self, server, path):
        super(FileStreamerNode, self).__init__(_lav.create_file_streamer_node(server, path))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(FileStreamerNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["ended"] = _libaudioverse.Lav_FILE_STREAMER_ENDED
                self._state['properties']["looping"] = _libaudioverse.Lav_FILE_STREAMER_LOOPING
                self._state['properties']["position"] = _libaudioverse.Lav_FILE_STREAMER_POSITION
            self._property_instances[_libaudioverse.Lav_FILE_STREAMER_ENDED] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_FILE_STREAMER_ENDED)
            self._property_instances[_libaudioverse.Lav_FILE_STREAMER_LOOPING] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_FILE_STREAMER_LOOPING)
            self._property_instances[_libaudioverse.Lav_FILE_STREAMER_POSITION] = DoubleProperty(handle = self.handle, slot = _libaudioverse.Lav_FILE_STREAMER_POSITION)


    @property
    def ended(self):   
        """Type: boolean

This property is read-only.

Switches from false to true once the stream has ended completely and gone silent.
This property will never go true unless looping is false."""
        return self._property_instances[_libaudioverse.Lav_FILE_STREAMER_ENDED]




    @property
    def looping(self):   
        """Type: boolean


Default value: False
If true, this node repeats the file from the beginning once it reaches the end.
Note that setting looping means that ended will never go true.
If ended is already true, it may take until the end of the next processing block for ended to properly go false once more."""
        return self._property_instances[_libaudioverse.Lav_FILE_STREAMER_LOOPING]

    @looping.setter
    def looping(self, value):
        self.looping.value=value



    @property
    def position(self):   
        """Type: double

Range: dynamic

Default value: 0.0

The position of playback, in seconds.
The range of this property corresponds to the total duration of the file.
Note that this property may be slightly inaccurate because this node has to pass data through a resampler."""
        return self._property_instances[_libaudioverse.Lav_FILE_STREAMER_POSITION]

    @position.setter
    def position(self, value):
        self.position.value=value




    def get_end_callback(self):
        r"""Get the end callback.
        
        This is a feature of the Python bindings and is not available in the C API.  See the setter for specific documentation on this callback."""
        with self._lock:
            cb = self._state['callbacks'].get("end", None)
            if cb is None:
                return None
            else:
                return cb[0]

    def set_end_callback(self, callback, additional_args = None, additional_kwargs = None):
        r"""Set the end callback.

Additional_args and additional_kwargs are passed to the callback in addition to any arguments from Libaudioverse.  Note that Libaudioverse always uses positional arguments.

C callback signature: `void  (LavHandle  nodeHandle, void *   userdata)`

Called outside the audio threads after the stream has both reached its end and gone silent.
When called, ended will be set to true,.

Callback parameters:

nodeHandle
  The node which called this callback.

userdata
  The userdata parameter as passed to the setter for this callback.

"""
        with self._lock:
            if callback is None:
                #delete the key, clear the callback with Libaudioverse.
                _lav.file_streamer_node_set_end_callback(self.handle, None, None)
                del self._state['callbacks']['end']
                return
            if additional_args is None:
                additionnal_args = ()
            if additional_kwargs is None:
                additional_kwargs = dict()
            wrapper = _CallbackWrapper(self, callback, additional_args, additional_kwargs)
            ctypes_callback = _libaudioverse.LavParameterlessCallback(wrapper)
            _lav.file_streamer_node_set_end_callback(self.handle, ctypes_callback, None)
            #if we get here, we hold both objects; we succeeded in setting because no exception was thrown.
            #As this is just for GC and the getter, we don't deal with the overhead of an object, and just use tuples.
            self._state['callbacks']["end"] = (callback, wrapper, ctypes_callback)

_types_to_classes[ObjectTypes.file_streamer_node] = FileStreamerNode
class FilteredDelayNode(GenericNode):
    r"""This node consists of a delay line with a biquad filter attached.
The output of the delay line is filtered.
The difference between this node and a delay line and filter pair is that this node will use the filtered output for the feedback.

This node is equivalent to the delay line in the Karplus-strong algorithm.

Inputs:

=====  ================================================  ======================
index  channels                                          description           
=====  ================================================  ======================
0      Depends on arguments to this node's constructor.  The signal to process.
=====  ================================================  ======================

Outputs:

=====  ================================================  =================================================================
index  channels                                          description                                                      
=====  ================================================  =================================================================
0      Depends on arguments to this node's constructor.  The result of processing the audio via the filter and delay line.
=====  ================================================  =================================================================
"""

    def __init__(self, server, max_delay, channels):
        super(FilteredDelayNode, self).__init__(_lav.create_filtered_delay_node(server, max_delay, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(FilteredDelayNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["dbgain"] = _libaudioverse.Lav_FILTERED_DELAY_DBGAIN
                self._state['properties']["delay"] = _libaudioverse.Lav_FILTERED_DELAY_DELAY
                self._state['properties']["delay_max"] = _libaudioverse.Lav_FILTERED_DELAY_DELAY_MAX
                self._state['properties']["feedback"] = _libaudioverse.Lav_FILTERED_DELAY_FEEDBACK
                self._state['properties']["filter_type"] = _libaudioverse.Lav_FILTERED_DELAY_FILTER_TYPE
                self._state['properties']["frequency"] = _libaudioverse.Lav_FILTERED_DELAY_FREQUENCY
                self._state['properties']["interpolation_time"] = _libaudioverse.Lav_FILTERED_DELAY_INTERPOLATION_TIME
                self._state['properties']["q"] = _libaudioverse.Lav_FILTERED_DELAY_Q
            self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_DBGAIN] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FILTERED_DELAY_DBGAIN)
            self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_DELAY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FILTERED_DELAY_DELAY)
            self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_DELAY_MAX] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FILTERED_DELAY_DELAY_MAX)
            self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_FEEDBACK] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FILTERED_DELAY_FEEDBACK)
            self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_FILTER_TYPE] = EnumProperty(handle = self.handle, slot = _libaudioverse.Lav_FILTERED_DELAY_FILTER_TYPE, enum = BiquadTypes)
            self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_FREQUENCY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FILTERED_DELAY_FREQUENCY)
            self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_INTERPOLATION_TIME] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FILTERED_DELAY_INTERPOLATION_TIME)
            self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_Q] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FILTERED_DELAY_Q)


    @property
    def dbgain(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

This property is a the gain in decibals to be used with the peaking and shelving filters.
It measures the gain that these filters apply to the part of the signal they boost."""
        return self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_DBGAIN]

    @dbgain.setter
    def dbgain(self, value):
        self.dbgain.value=value



    @property
    def delay(self):   
        """Type: float

Range: dynamic

Default value: 0.0

The delay of the delay line in seconds.
The range of this property depends on the maxDelay parameter to the constructor."""
        return self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_DELAY]

    @delay.setter
    def delay(self, value):
        self.delay.value=value



    @property
    def delay_max(self):   
        """Type: float

This property is read-only.

The max delay as set at the node's creation time."""
        return self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_DELAY_MAX]




    @property
    def feedback(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

The feedback coefficient.
The output of the filter is fed back into the delay line, multiplied by this coefficient."""
        return self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_FEEDBACK]

    @feedback.setter
    def feedback(self, value):
        self.feedback.value=value



    @property
    def filter_type(self):   
        """Type: int

Range: :any:`BiquadTypes`

Default value: :any:`BiquadTypes.lowpass`

The type of the filter.
This determines the interpretations of the other properties on this node."""
        return self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_FILTER_TYPE]

    @filter_type.setter
    def filter_type(self, value):
        self.filter_type.value=value



    @property
    def frequency(self):   
        """Type: float

Range: [0, INFINITY]

Default value: 2000.0

This is the frequency of interest.
What specifically this means depends on the selected filter type; for example, it is the cutoff frequency for lowpass and highpass."""
        return self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_FREQUENCY]

    @frequency.setter
    def frequency(self, value):
        self.frequency.value=value



    @property
    def interpolation_time(self):   
        """Type: float

Range: [0.001, INFINITY]

Default value: 0.001

When the delay property is changed, the delay line crossfades between the old position and the new one.
This property sets how long this crossfade will take.
Note that for this node, it is impossible to get rid of the crossfade completely."""
        return self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_INTERPOLATION_TIME]

    @interpolation_time.setter
    def interpolation_time(self, value):
        self.interpolation_time.value=value



    @property
    def q(self):   
        """Type: float

Range: [0.001, INFINITY]

Default value: 0.5

Q is a mathematically complex parameter, a full description of which is beyond the scope of this manual.
For lowpass, bandpass, and high pass filters, Q can be interpreted as a measure of resonation.
For Q<=0.5, the filter is said to be damped:
it will cut frequencies.
For Q>0.5, however, some frequencies are likely to be boosted.

Q controls the bandwidth for the bandpass and peaking filter types
as well as the slope for the shelving EQ.

For everything except the peaking filter, this property follows the normal definition of Q in the electrical engineering literature.
For more specifics, see the Audio EQ Cookbook.
It is found here:
http://www.musicdsp.org/files/Audio-EQ-Cookbook.txt"""
        return self._property_instances[_libaudioverse.Lav_FILTERED_DELAY_Q]

    @q.setter
    def q(self, value):
        self.q.value=value





_types_to_classes[ObjectTypes.filtered_delay_node] = FilteredDelayNode
class FirstOrderFilterNode(GenericNode):
    r"""A first order filter section, implementing the transfer function :math:`H(Z) = \frac{B_0 + B_1 Z^{-1} }{1+A_0 Z^{-1} }`

This filter is not your friend unless you know DSP or have a specific goal in mind.
Most applications will want  a :class:`BiquadNode` or a :class:`OnePoleFilterNode` instead.

This filter is not controlled through frequency specifications.
Instead, the position of the pole and the zero on the real axis are individually controllable with a-rate properties.
Some helper functions exist to position them for common configurations, but other filter types do most of it better.
The major advantage for this filter type is that it is incredibly inexpensive as compared to the :class:`IirNode` and supports automation of the pole and zero's position.

Inputs:

=====  ================================================  =====================
index  channels                                          description          
=====  ================================================  =====================
0      Depends on arguments to this node's constructor.  The signal to filter.
=====  ================================================  =====================

Outputs:

=====  ================================================  ====================
index  channels                                          description         
=====  ================================================  ====================
0      Depends on arguments to this node's constructor.  The filtered signal.
=====  ================================================  ====================
"""

    def __init__(self, server, channels):
        super(FirstOrderFilterNode, self).__init__(_lav.create_first_order_filter_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(FirstOrderFilterNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["pole"] = _libaudioverse.Lav_FIRST_ORDER_FILTER_POLE
                self._state['properties']["zero"] = _libaudioverse.Lav_FIRST_ORDER_FILTER_ZERO
            self._property_instances[_libaudioverse.Lav_FIRST_ORDER_FILTER_POLE] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FIRST_ORDER_FILTER_POLE)
            self._property_instances[_libaudioverse.Lav_FIRST_ORDER_FILTER_ZERO] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_FIRST_ORDER_FILTER_ZERO)


    @property
    def pole(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

The position of the pole on the real axis.

The pole may be positioned anywhere, but stable filters  usually keep all poles inside the unit circle.
For a stable filter, the value of this property should usually between -1 and 1."""
        return self._property_instances[_libaudioverse.Lav_FIRST_ORDER_FILTER_POLE]

    @pole.setter
    def pole(self, value):
        self.pole.value=value



    @property
    def zero(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

The position of the zero on the real axis."""
        return self._property_instances[_libaudioverse.Lav_FIRST_ORDER_FILTER_ZERO]

    @zero.setter
    def zero(self, value):
        self.zero.value=value



    def configure_allpass(node, frequency):
        r"""Configure this node as an allpass.
You specify the :math:`\frac{\pi}{2}` frequency.
You get a filter with a phase of :math:`\pi` at DC and 0 at Nyquist."""
        return _lav.first_order_filter_node_configure_allpass(node, frequency)

    def configure_highpass(node, frequency):
        r"""Configure the filter as a highpass with a roll-off of ``6 DB`` per octave.
This is identical to the :class:`OnePoleFilterNode` highpass configuration."""
        return _lav.first_order_filter_node_configure_highpass(node, frequency)

    def configure_lowpass(node, frequency):
        r"""Configure the filter as a first-order Butterworth lowpass.
This is equivalent to the :class:`OnePoleFilterNode` lowpass configuration."""
        return _lav.first_order_filter_node_configure_lowpass(node, frequency)



_types_to_classes[ObjectTypes.first_order_filter_node] = FirstOrderFilterNode
class GainNode(GenericNode):
    r"""This node is essentially in instantiated generic node, offering only the functionality therein.
Its purpose is to allow changing the gain or adding offset to a large collection of nodes.
One possible use is as a simple mixer: point all the nodes to be mixed at the input, set mul, and then point the output at the destination for the mixed audio.

Inputs:

=====  ================================================  =======================================
index  channels                                          description                            
=====  ================================================  =======================================
0      Depends on arguments to this node's constructor.  The signal whose gain is to be changed.
=====  ================================================  =======================================

Outputs:

=====  ================================================  =================================
index  channels                                          description                      
=====  ================================================  =================================
0      Depends on arguments to this node's constructor.  The signal with its gain changed.
=====  ================================================  =================================
"""

    def __init__(self, server, channels):
        super(GainNode, self).__init__(_lav.create_gain_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(GainNode, self).init_with_handle(handle)




_types_to_classes[ObjectTypes.gain_node] = GainNode
class GraphListenerNode(GenericNode):
    r"""This node defines a callback which is called every block.
The callback is passed pointers to the audio data passing through this node for the current block.
The effect is that this node allows observing audio passing through any location in the audio graph.

Inputs:

=====  ================================================  ==========================================================
index  channels                                          description                                               
=====  ================================================  ==========================================================
0      Depends on arguments to this node's constructor.  The audio which will be passed to the associated callback.
=====  ================================================  ==========================================================

Outputs:

=====  ================================================  ==============================================================
index  channels                                          description                                                   
=====  ================================================  ==============================================================
0      Depends on arguments to this node's constructor.  The same audio as connected to the input without modification.
=====  ================================================  ==============================================================
"""

    def __init__(self, server, channels):
        super(GraphListenerNode, self).__init__(_lav.create_graph_listener_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(GraphListenerNode, self).init_with_handle(handle)



    def get_listening_callback(self):
        r"""Get the listening callback.
        
        This is a feature of the Python bindings and is not available in the C API.  See the setter for specific documentation on this callback."""
        with self._lock:
            cb = self._state['callbacks'].get("listening", None)
            if cb is None:
                return None
            else:
                return cb[0]

    def set_listening_callback(self, callback, additional_args = None, additional_kwargs = None):
        r"""Set the listening callback.

Additional_args and additional_kwargs are passed to the callback in addition to any arguments from Libaudioverse.  Note that Libaudioverse always uses positional arguments.

C callback signature: `void  (LavHandle  nodeHandle, unsigned int  frames, unsigned int  channels, float *   buffer, void *   userdata)`

When set, audio is passed to this callback every block.
This callback is called inside the audio threads; do not block.

Callback parameters:

nodeHandle
  The node which called this callback.

frames
  The number of frames of audio being made available to client code.  This should always be the same as the server's block size.

channels
  The number of channels of audio being made available to client code.

buffer
  The data, stored in interleaved format.  The length of this buffer is ``frames*channels``.

userdata
  The userdata parameter as passed to the setter for this callback.

"""
        with self._lock:
            if callback is None:
                #delete the key, clear the callback with Libaudioverse.
                _lav.graph_listener_node_set_listening_callback(self.handle, None, None)
                del self._state['callbacks']['listening']
                return
            if additional_args is None:
                additionnal_args = ()
            if additional_kwargs is None:
                additional_kwargs = dict()
            wrapper = _CallbackWrapper(self, callback, additional_args, additional_kwargs)
            ctypes_callback = _libaudioverse.LavGraphListenerNodeListeningCallback(wrapper)
            _lav.graph_listener_node_set_listening_callback(self.handle, ctypes_callback, None)
            #if we get here, we hold both objects; we succeeded in setting because no exception was thrown.
            #As this is just for GC and the getter, we don't deal with the overhead of an object, and just use tuples.
            self._state['callbacks']["listening"] = (callback, wrapper, ctypes_callback)

_types_to_classes[ObjectTypes.graph_listener_node] = GraphListenerNode
class HardLimiterNode(GenericNode):
    r"""The input to this node is hard limited: values less than -1.0 are set to -1.0 and values above 1.0 are set to 1.0.
Use the hard limiter in order to prevent oddities with audio hardware; it should usually be the last piece in your pipeline before the server.
Note that the 3D API handles hard limiting appropriately, and you do not need to worry about this there.

Inputs:

=====  ================================================  ===================
index  channels                                          description        
=====  ================================================  ===================
0      Depends on arguments to this node's constructor.  The signal to limit
=====  ================================================  ===================

Outputs:

=====  ================================================  ============================================================================
index  channels                                          description                                                                 
=====  ================================================  ============================================================================
0      Depends on arguments to this node's constructor.  The limited signal: no sample shall have an absolute value greater than 1.0.
=====  ================================================  ============================================================================
"""

    def __init__(self, server, channels):
        super(HardLimiterNode, self).__init__(_lav.create_hard_limiter_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(HardLimiterNode, self).init_with_handle(handle)




_types_to_classes[ObjectTypes.hard_limiter_node] = HardLimiterNode
class HrtfNode(GenericNode):
    r"""This node implements an HRTF panner.
You can use either Libaudioverse's internal HRTF (The Diffuse MIT Kemar Dataset) by passing "default" as the HRTf file name,
or an HRTF of your own.

Inputs:

=====  ========  ==================
index  channels  description       
=====  ========  ==================
0      1         The signal to pan.
=====  ========  ==================

Outputs:

=====  ========  =================================
index  channels  description                      
=====  ========  =================================
0      2         The signal with the HRTF applied.
=====  ========  =================================
"""

    def __init__(self, server, hrtf_path):
        super(HrtfNode, self).__init__(_lav.create_hrtf_node(server, hrtf_path))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(HrtfNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["azimuth"] = _libaudioverse.Lav_PANNER_AZIMUTH
                self._state['properties']["elevation"] = _libaudioverse.Lav_PANNER_ELEVATION
                self._state['properties']["should_crossfade"] = _libaudioverse.Lav_PANNER_SHOULD_CROSSFADE
            self._property_instances[_libaudioverse.Lav_PANNER_AZIMUTH] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_PANNER_AZIMUTH)
            self._property_instances[_libaudioverse.Lav_PANNER_ELEVATION] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_PANNER_ELEVATION)
            self._property_instances[_libaudioverse.Lav_PANNER_SHOULD_CROSSFADE] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_PANNER_SHOULD_CROSSFADE)


    @property
    def azimuth(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

The horizontal angle of the panner in degrees.
0 is straight ahead and positive values are clockwise."""
        return self._property_instances[_libaudioverse.Lav_PANNER_AZIMUTH]

    @azimuth.setter
    def azimuth(self, value):
        self.azimuth.value=value



    @property
    def elevation(self):   
        """Type: float

Range: [-90.0, 90.0]

Default value: 0.0

The vertical angle of the panner in degrees.
0 is horizontal and positive values move upward."""
        return self._property_instances[_libaudioverse.Lav_PANNER_ELEVATION]

    @elevation.setter
    def elevation(self, value):
        self.elevation.value=value



    @property
    def should_crossfade(self):   
        """Type: boolean


Default value: True
By default, panners crossfade their output.
This property allows such functionality to be disabled.
Note that for HRTF nodes, crossfading is more important than for other panner types.
Unlike other panner types, the audio artifacts produced by disabling crossfading are noticeable, even for updates of only a few degrees."""
        return self._property_instances[_libaudioverse.Lav_PANNER_SHOULD_CROSSFADE]

    @should_crossfade.setter
    def should_crossfade(self, value):
        self.should_crossfade.value=value





_types_to_classes[ObjectTypes.hrtf_node] = HrtfNode
class IirNode(GenericNode):
    r"""Implements arbetrary IIR filters.
The only restriction on the filter is that the first element of the denominator must be nonzero.
To configure this node, use the function Lav_iirNodeSetCoefficients.

Inputs:

=====  ================================================  =====================
index  channels                                          description          
=====  ================================================  =====================
0      Depends on arguments to this node's constructor.  The signal to filter.
=====  ================================================  =====================

Outputs:

=====  ================================================  =======================================
index  channels                                          description                            
=====  ================================================  =======================================
0      Depends on arguments to this node's constructor.  The signal with the IIR filter applied.
=====  ================================================  =======================================
"""

    def __init__(self, server, channels):
        super(IirNode, self).__init__(_lav.create_iir_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(IirNode, self).init_with_handle(handle)


    def set_coefficients(node, numerator_length, numerator, denominator_length, denominator, should_clear_history):
        r"""Configure the coefficients of the IIR filter."""
        return _lav.iir_node_set_coefficients(node, numerator_length, numerator, denominator_length, denominator, should_clear_history)



_types_to_classes[ObjectTypes.iir_node] = IirNode
class LeakyIntegratorNode(GenericNode):
    r"""A leaky integrator.
Leaky integrators integrate their input signals, while leaking over time.
Introducing the leak allows for avoiding DC offset problems.
If you feed this node a signal that is zero, it will slowly decrease the output in accordance with the Lav_LEAKY_INTEGRATOR_LEAKYNESS property.

Inputs:

=====  ================================================  ======================
index  channels                                          description           
=====  ================================================  ======================
0      Depends on arguments to this node's constructor.  A signal to integrate.
=====  ================================================  ======================

Outputs:

=====  ================================================  ===========================
index  channels                                          description                
=====  ================================================  ===========================
0      Depends on arguments to this node's constructor.  The integral of the signal.
=====  ================================================  ===========================
"""

    def __init__(self, server, channels):
        super(LeakyIntegratorNode, self).__init__(_lav.create_leaky_integrator_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(LeakyIntegratorNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["leakyness"] = _libaudioverse.Lav_LEAKY_INTEGRATOR_LEAKYNESS
            self._property_instances[_libaudioverse.Lav_LEAKY_INTEGRATOR_LEAKYNESS] = DoubleProperty(handle = self.handle, slot = _libaudioverse.Lav_LEAKY_INTEGRATOR_LEAKYNESS)


    @property
    def leakyness(self):   
        """Type: double

Range: [0.0, 1.0]

Default value: 1.0

The leakyness (or time constant) of the integrator.

If you feed the leaky integrator a constant signal of 0, then this property's value is the percent decrease as observed after 1 second."""
        return self._property_instances[_libaudioverse.Lav_LEAKY_INTEGRATOR_LEAKYNESS]

    @leakyness.setter
    def leakyness(self, value):
        self.leakyness.value=value





_types_to_classes[ObjectTypes.leaky_integrator_node] = LeakyIntegratorNode
class MultipannerNode(GenericNode):
    r"""A panner which can have the algorithm it uses changed at runtime.
The use for multipanners is for applications in which we may wish to change the speaker configuration at runtime.
Capabilities include switching from HRTF to stereo and back, a useful property for games wherein the user might or might not be using headphones.

Inputs:

=====  ========  ==================
index  channels  description       
=====  ========  ==================
0      1         The signal to pan.
=====  ========  ==================

Outputs:

=====  ==============================================  ================================================================
index  channels                                        description                                                     
=====  ==============================================  ================================================================
0      Depends on the currently set panning strategy.  The signal, panned according to the configured panning strategy.
=====  ==============================================  ================================================================
"""

    def __init__(self, server, hrtf_path):
        super(MultipannerNode, self).__init__(_lav.create_multipanner_node(server, hrtf_path))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(MultipannerNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["azimuth"] = _libaudioverse.Lav_PANNER_AZIMUTH
                self._state['properties']["elevation"] = _libaudioverse.Lav_PANNER_ELEVATION
                self._state['properties']["should_crossfade"] = _libaudioverse.Lav_PANNER_SHOULD_CROSSFADE
                self._state['properties']["strategy"] = _libaudioverse.Lav_PANNER_STRATEGY
            self._property_instances[_libaudioverse.Lav_PANNER_AZIMUTH] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_PANNER_AZIMUTH)
            self._property_instances[_libaudioverse.Lav_PANNER_ELEVATION] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_PANNER_ELEVATION)
            self._property_instances[_libaudioverse.Lav_PANNER_SHOULD_CROSSFADE] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_PANNER_SHOULD_CROSSFADE)
            self._property_instances[_libaudioverse.Lav_PANNER_STRATEGY] = EnumProperty(handle = self.handle, slot = _libaudioverse.Lav_PANNER_STRATEGY, enum = PanningStrategies)


    @property
    def azimuth(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

The horizontal angle of the panner, in degrees.
0 is straight ahead and positive values are clockwise."""
        return self._property_instances[_libaudioverse.Lav_PANNER_AZIMUTH]

    @azimuth.setter
    def azimuth(self, value):
        self.azimuth.value=value



    @property
    def elevation(self):   
        """Type: float

Range: [-90.0, 90.0]

Default value: 0.0

The vertical angle of the panner, in degrees.
0 is horizontal and positive values are upward."""
        return self._property_instances[_libaudioverse.Lav_PANNER_ELEVATION]

    @elevation.setter
    def elevation(self, value):
        self.elevation.value=value



    @property
    def should_crossfade(self):   
        """Type: boolean


Default value: True
Whether or not this panner should crossfade.
Lack of crossfading introduces audible artifacts when the panner is moved.
You usually want this on."""
        return self._property_instances[_libaudioverse.Lav_PANNER_SHOULD_CROSSFADE]

    @should_crossfade.setter
    def should_crossfade(self, value):
        self.should_crossfade.value=value



    @property
    def strategy(self):   
        """Type: int

Range: :any:`PanningStrategies`

Default value: :any:`PanningStrategies.stereo`

What type of panning to use.
Possibilities include HRTF, stereo, 5.1, and 7.1 speaker configurations.
For something more nontraditional, use an amplitude panner."""
        return self._property_instances[_libaudioverse.Lav_PANNER_STRATEGY]

    @strategy.setter
    def strategy(self, value):
        self.strategy.value=value





_types_to_classes[ObjectTypes.multipanner_node] = MultipannerNode
class NoiseNode(GenericNode):
    r"""Generates any of a variety of types of noise.

This node has no inputs.

Outputs:

=====  ========  =================================
index  channels  description                      
=====  ========  =================================
0      1         The noise generated by this node.
=====  ========  =================================
"""

    def __init__(self, server):
        super(NoiseNode, self).__init__(_lav.create_noise_node(server))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(NoiseNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["noise_type"] = _libaudioverse.Lav_NOISE_NOISE_TYPE
                self._state['properties']["should_normalize"] = _libaudioverse.Lav_NOISE_SHOULD_NORMALIZE
            self._property_instances[_libaudioverse.Lav_NOISE_NOISE_TYPE] = EnumProperty(handle = self.handle, slot = _libaudioverse.Lav_NOISE_NOISE_TYPE, enum = NoiseTypes)
            self._property_instances[_libaudioverse.Lav_NOISE_SHOULD_NORMALIZE] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_NOISE_SHOULD_NORMALIZE)


    @property
    def noise_type(self):   
        """Type: int

Range: :any:`NoiseTypes`

Default value: :any:`NoiseTypes.white`

The type of noise to generate."""
        return self._property_instances[_libaudioverse.Lav_NOISE_NOISE_TYPE]

    @noise_type.setter
    def noise_type(self, value):
        self.noise_type.value=value



    @property
    def should_normalize(self):   
        """Type: boolean


Default value: False
Whether or not to normalize the output.
Some types of noise are quieter without this enabled.
Turning it on is sometimes helpful and sometimes not."""
        return self._property_instances[_libaudioverse.Lav_NOISE_SHOULD_NORMALIZE]

    @should_normalize.setter
    def should_normalize(self, value):
        self.should_normalize.value=value





_types_to_classes[ObjectTypes.noise_node] = NoiseNode
class OnePoleFilterNode(GenericNode):
    r"""A one-pole filter section, implementing the transfer function :math:`H(Z) = rac{1}{1+A_0 Z^{-1} }`

This filter is capable of implementing either a lowpass or highpass filter and is extremmely cheep.
The produced filter rolls off at about 6 DB per octave.

The default filter configuration is a lowpass at 500 HZ.
The type of the filter is controlled via the ``is_highpass`` property.
If said property is true, the filter becomes a highpass.

Note that this filter can be swept with a-rate accuracy.

Inputs:

=====  ================================================  =====================
index  channels                                          description          
=====  ================================================  =====================
0      Depends on arguments to this node's constructor.  The signal to filter.
=====  ================================================  =====================

Outputs:

=====  ================================================  ====================
index  channels                                          description         
=====  ================================================  ====================
0      Depends on arguments to this node's constructor.  The filtered signal.
=====  ================================================  ====================
"""

    def __init__(self, server, channels):
        super(OnePoleFilterNode, self).__init__(_lav.create_one_pole_filter_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(OnePoleFilterNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["frequency"] = _libaudioverse.Lav_ONE_POLE_FILTER_FREQUENCY
                self._state['properties']["is_highpass"] = _libaudioverse.Lav_ONE_POLE_FILTER_IS_HIGHPASS
            self._property_instances[_libaudioverse.Lav_ONE_POLE_FILTER_FREQUENCY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_ONE_POLE_FILTER_FREQUENCY)
            self._property_instances[_libaudioverse.Lav_ONE_POLE_FILTER_IS_HIGHPASS] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_ONE_POLE_FILTER_IS_HIGHPASS)


    @property
    def frequency(self):   
        """Type: float

Range: dynamic

Default value: 500.0

The -3 DB frequency of the filter.

The range of this property is from 0 to half the sampling rate."""
        return self._property_instances[_libaudioverse.Lav_ONE_POLE_FILTER_FREQUENCY]

    @frequency.setter
    def frequency(self, value):
        self.frequency.value=value



    @property
    def is_highpass(self):   
        """Type: boolean


Default value: False
True if the filter is a highpass.

If this property is false, the filter is a lowpass."""
        return self._property_instances[_libaudioverse.Lav_ONE_POLE_FILTER_IS_HIGHPASS]

    @is_highpass.setter
    def is_highpass(self, value):
        self.is_highpass.value=value





_types_to_classes[ObjectTypes.one_pole_filter_node] = OnePoleFilterNode
class PullNode(GenericNode):
    r"""This node calls the audio callback whenever it needs more audio.
The purpose of this node is to inject audio from an external source that Libaudioverse does not support, for example a custom network protocol.

This node has no inputs.

Outputs:

=====  ================================================  ======================================
index  channels                                          description                           
=====  ================================================  ======================================
0      Depends on arguments to this node's constructor.  The result of the configured callback.
=====  ================================================  ======================================
"""

    def __init__(self, server, sr, channels):
        super(PullNode, self).__init__(_lav.create_pull_node(server, sr, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(PullNode, self).init_with_handle(handle)



    def get_audio_callback(self):
        r"""Get the audio callback.
        
        This is a feature of the Python bindings and is not available in the C API.  See the setter for specific documentation on this callback."""
        with self._lock:
            cb = self._state['callbacks'].get("audio", None)
            if cb is None:
                return None
            else:
                return cb[0]

    def set_audio_callback(self, callback, additional_args = None, additional_kwargs = None):
        r"""Set the audio callback.

Additional_args and additional_kwargs are passed to the callback in addition to any arguments from Libaudioverse.  Note that Libaudioverse always uses positional arguments.

C callback signature: `void  (LavHandle  nodeHandle, int  frames, int  channels, float *   buffer, void *   userdata)`

Called when the node needs more audio.

Callback parameters:

nodeHandle
  The node which called this callback.

frames
  The number of frames of audio needed.  This is not guaranteed to be the same on every call.

channels
  The number of channels as set when the pull node is created.

buffer
  The destination to which audio should be written.  This is a buffer that is ``frames*channels`` long.  Write interleaved audio data to it and do not assume that it is zeroed.

userdata
  The userdata parameter as passed to the setter for this callback.

"""
        with self._lock:
            if callback is None:
                #delete the key, clear the callback with Libaudioverse.
                _lav.pull_node_set_audio_callback(self.handle, None, None)
                del self._state['callbacks']['audio']
                return
            if additional_args is None:
                additionnal_args = ()
            if additional_kwargs is None:
                additional_kwargs = dict()
            wrapper = _CallbackWrapper(self, callback, additional_args, additional_kwargs)
            ctypes_callback = _libaudioverse.LavPullNodeAudioCallback(wrapper)
            _lav.pull_node_set_audio_callback(self.handle, ctypes_callback, None)
            #if we get here, we hold both objects; we succeeded in setting because no exception was thrown.
            #As this is just for GC and the getter, we don't deal with the overhead of an object, and just use tuples.
            self._state['callbacks']["audio"] = (callback, wrapper, ctypes_callback)

_types_to_classes[ObjectTypes.pull_node] = PullNode
class PushNode(GenericNode):
    r"""The purpose of this node is the same as the pull node, but it is used in situations wherein we do not know when we are going to get audio.
Audio is queued as it is pushed to this node and then played as fast as possible.
This node can be used to avoid writing a queue of audio yourself, as it essentially implements said functionality.
If you need low latency audio or the ability to run something like the Opus encoder's
ability to cover for missing frames, you need a pull node.

This node has no inputs.

Outputs:

=====  ================================================  =============================================
index  channels                                          description                                  
=====  ================================================  =============================================
0      Depends on arguments to this node's constructor.  Either audio from the internal queue or zero.
=====  ================================================  =============================================
"""

    def __init__(self, server, sr, channels):
        super(PushNode, self).__init__(_lav.create_push_node(server, sr, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(PushNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["threshold"] = _libaudioverse.Lav_PUSH_THRESHOLD
            self._property_instances[_libaudioverse.Lav_PUSH_THRESHOLD] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_PUSH_THRESHOLD)


    @property
    def threshold(self):   
        """Type: float

Range: [0.0, INFINITY]

Default value: 0.03

When the remaining audio in the push node has a duration less than this property, the low callback is called."""
        return self._property_instances[_libaudioverse.Lav_PUSH_THRESHOLD]

    @threshold.setter
    def threshold(self, value):
        self.threshold.value=value



    def feed(node, length, frames):
        r"""Feed more audio data into the internal queue."""
        return _lav.push_node_feed(node, length, frames)


    def get_low_callback(self):
        r"""Get the low callback.
        
        This is a feature of the Python bindings and is not available in the C API.  See the setter for specific documentation on this callback."""
        with self._lock:
            cb = self._state['callbacks'].get("low", None)
            if cb is None:
                return None
            else:
                return cb[0]

    def set_low_callback(self, callback, additional_args = None, additional_kwargs = None):
        r"""Set the low callback.

Additional_args and additional_kwargs are passed to the callback in addition to any arguments from Libaudioverse.  Note that Libaudioverse always uses positional arguments.

C callback signature: `void  (LavHandle  nodeHandle, void *   userdata)`

Called once per block and outside the audio thread when there is less than the specified threshold audio remaining.

Callback parameters:

nodeHandle
  The node which called this callback.

userdata
  The userdata parameter as passed to the setter for this callback.

"""
        with self._lock:
            if callback is None:
                #delete the key, clear the callback with Libaudioverse.
                _lav.push_node_set_low_callback(self.handle, None, None)
                del self._state['callbacks']['low']
                return
            if additional_args is None:
                additionnal_args = ()
            if additional_kwargs is None:
                additional_kwargs = dict()
            wrapper = _CallbackWrapper(self, callback, additional_args, additional_kwargs)
            ctypes_callback = _libaudioverse.LavParameterlessCallback(wrapper)
            _lav.push_node_set_low_callback(self.handle, ctypes_callback, None)
            #if we get here, we hold both objects; we succeeded in setting because no exception was thrown.
            #As this is just for GC and the getter, we don't deal with the overhead of an object, and just use tuples.
            self._state['callbacks']["low"] = (callback, wrapper, ctypes_callback)
    def get_underrun_callback(self):
        r"""Get the underrun callback.
        
        This is a feature of the Python bindings and is not available in the C API.  See the setter for specific documentation on this callback."""
        with self._lock:
            cb = self._state['callbacks'].get("underrun", None)
            if cb is None:
                return None
            else:
                return cb[0]

    def set_underrun_callback(self, callback, additional_args = None, additional_kwargs = None):
        r"""Set the underrun callback.

Additional_args and additional_kwargs are passed to the callback in addition to any arguments from Libaudioverse.  Note that Libaudioverse always uses positional arguments.

C callback signature: `void  (LavHandle  nodeHandle, void *   userdata)`

Called exactly once and outside the audio thread when the node runs out of audio completely.

Callback parameters:

nodeHandle
  The node which called this callback.

userdata
  The userdata parameter as passed to the setter for this callback.

"""
        with self._lock:
            if callback is None:
                #delete the key, clear the callback with Libaudioverse.
                _lav.push_node_set_underrun_callback(self.handle, None, None)
                del self._state['callbacks']['underrun']
                return
            if additional_args is None:
                additionnal_args = ()
            if additional_kwargs is None:
                additional_kwargs = dict()
            wrapper = _CallbackWrapper(self, callback, additional_args, additional_kwargs)
            ctypes_callback = _libaudioverse.LavParameterlessCallback(wrapper)
            _lav.push_node_set_underrun_callback(self.handle, ctypes_callback, None)
            #if we get here, we hold both objects; we succeeded in setting because no exception was thrown.
            #As this is just for GC and the getter, we don't deal with the overhead of an object, and just use tuples.
            self._state['callbacks']["underrun"] = (callback, wrapper, ctypes_callback)

_types_to_classes[ObjectTypes.push_node] = PushNode
class RecorderNode(GenericNode):
    r"""Records audio to files.

The usage pattern for this node is simple:
connect something to the input, call Lav_recorderNodeStartRecording, and ensure that the node is processed.
In order to avoid potential problems with blocks of silence at the beginning of the recording, this node's default state is playing.
You should connect the output to something that will demand the recorder node's audio or change the state to always playing, usually after a call to Lav_recorderNodeStartRecording.
If you don't, no recording will take place.

Unlike most other nodes in Libaudioverse, it is important that you call Lav_recorderNodeStopRecording when done recording.
Failure to do so may lead to any of a number of surprising results.

Inputs:

=====  ================================================  =====================
index  channels                                          description          
=====  ================================================  =====================
0      Depends on arguments to this node's constructor.  The signal to record.
=====  ================================================  =====================

Outputs:

=====  ================================================  =============================
index  channels                                          description                  
=====  ================================================  =============================
0      Depends on arguments to this node's constructor.  The same as the input signal.
=====  ================================================  =============================
"""

    def __init__(self, server, channels):
        super(RecorderNode, self).__init__(_lav.create_recorder_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(RecorderNode, self).init_with_handle(handle)


    def start_recording(node, path):
        r"""Begin recording to the specified files.
The sample rate is the same as that of the server.
The channel count is the same as this node was initialized with.
The format of the file is determined from the extension: this function recognizes ".wav" and ".ogg" on all platforms."""
        return _lav.recorder_node_start_recording(node, path)

    def stop_recording(node):
        r"""Stops recording.

Be sure to call this function.
Failure to do so may lead to any of a number of undesirable problems."""
        return _lav.recorder_node_stop_recording(node)



_types_to_classes[ObjectTypes.recorder_node] = RecorderNode
class RingmodNode(GenericNode):
    r"""This node has two inputs and one output.
The two inputs will be converted to mono and then multiplied, before being sent to the output.

Inputs:

=====  ========  ==================
index  channels  description       
=====  ========  ==================
0      1         The first signal. 
1      1         The second signal.
=====  ========  ==================

Outputs:

=====  ========  =========================================================
index  channels  description                                              
=====  ========  =========================================================
0      1         The result of multiplying the two input signals together.
=====  ========  =========================================================
"""

    def __init__(self, server):
        super(RingmodNode, self).__init__(_lav.create_ringmod_node(server))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(RingmodNode, self).init_with_handle(handle)




_types_to_classes[ObjectTypes.ringmod_node] = RingmodNode
class SineNode(GenericNode):
    r"""A simple sine oscillator.

This node has no inputs.

Outputs:

=====  ========  ============
index  channels  description 
=====  ========  ============
0      1         A sine wave.
=====  ========  ============
"""

    def __init__(self, server):
        super(SineNode, self).__init__(_lav.create_sine_node(server))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(SineNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["frequency"] = _libaudioverse.Lav_OSCILLATOR_FREQUENCY
                self._state['properties']["frequency_multiplier"] = _libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER
                self._state['properties']["phase"] = _libaudioverse.Lav_OSCILLATOR_PHASE
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_FREQUENCY)
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER)
            self._property_instances[_libaudioverse.Lav_OSCILLATOR_PHASE] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_OSCILLATOR_PHASE)


    @property
    def frequency(self):   
        """Type: float

Range: [0, INFINITY]

Default value: 440.0

The frequency of the sine wave in HZ."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY]

    @frequency.setter
    def frequency(self, value):
        self.frequency.value=value



    @property
    def frequency_multiplier(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 1.0

An additional multiplicative factor applied to the frequency of the oscillator.

This is useful for creating instruments, as the notes of the standard musical scale fall on frequency multiples of a reference pitch, rather than a linear increase."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_FREQUENCY_MULTIPLIER]

    @frequency_multiplier.setter
    def frequency_multiplier(self, value):
        self.frequency_multiplier.value=value



    @property
    def phase(self):   
        """Type: float

Range: [0.0, 1.0]

Default value: 0.0

The phase of the sine node.
This is measured in periods, not in radians."""
        return self._property_instances[_libaudioverse.Lav_OSCILLATOR_PHASE]

    @phase.setter
    def phase(self, value):
        self.phase.value=value





_types_to_classes[ObjectTypes.sine_node] = SineNode
class SourceNode(GenericNode):
    r"""The source node allows the spatialization of sound that passes through it.
Sources have one input which is mono, to which a node should be connected.
The audio from the input is spatialized according both to the source's properties and those on its environment, and passed directly to the environment.
Sources have no outputs.
To hear a source, you must connect its environment to something instead.

Since the source communicates with the environment through a nonstandard mechanism, environments do not keep their sources alive.
If you are in a garbage collected language, failure to hold on to the source nodes will cause them to go silent.

Inputs:

=====  ========  ======================================
index  channels  description                           
=====  ========  ======================================
0      1         The audio to enter the 3D environment.
=====  ========  ======================================

This node has no outputs. If you want it to advance, be sure to use `foo.state = nodeStates.always_playing`.
"""

    def __init__(self, server, environment):
        super(SourceNode, self).__init__(_lav.create_source_node(server, environment))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(SourceNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["control_distance_model"] = _libaudioverse.Lav_SOURCE_CONTROL_DISTANCE_MODEL
                self._state['properties']["control_panning"] = _libaudioverse.Lav_SOURCE_CONTROL_PANNING
                self._state['properties']["control_reverb"] = _libaudioverse.Lav_SOURCE_CONTROL_REVERB
                self._state['properties']["distance_model"] = _libaudioverse.Lav_SOURCE_DISTANCE_MODEL
                self._state['properties']["head_relative"] = _libaudioverse.Lav_SOURCE_HEAD_RELATIVE
                self._state['properties']["max_distance"] = _libaudioverse.Lav_SOURCE_MAX_DISTANCE
                self._state['properties']["max_reverb_level"] = _libaudioverse.Lav_SOURCE_MAX_REVERB_LEVEL
                self._state['properties']["min_reverb_level"] = _libaudioverse.Lav_SOURCE_MIN_REVERB_LEVEL
                self._state['properties']["occlusion"] = _libaudioverse.Lav_SOURCE_OCCLUSION
                self._state['properties']["orientation"] = _libaudioverse.Lav_SOURCE_ORIENTATION
                self._state['properties']["panning_strategy"] = _libaudioverse.Lav_SOURCE_PANNING_STRATEGY
                self._state['properties']["position"] = _libaudioverse.Lav_SOURCE_POSITION
                self._state['properties']["reverb_distance"] = _libaudioverse.Lav_SOURCE_REVERB_DISTANCE
                self._state['properties']["size"] = _libaudioverse.Lav_SOURCE_SIZE
            self._property_instances[_libaudioverse.Lav_SOURCE_CONTROL_DISTANCE_MODEL] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_CONTROL_DISTANCE_MODEL)
            self._property_instances[_libaudioverse.Lav_SOURCE_CONTROL_PANNING] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_CONTROL_PANNING)
            self._property_instances[_libaudioverse.Lav_SOURCE_CONTROL_REVERB] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_CONTROL_REVERB)
            self._property_instances[_libaudioverse.Lav_SOURCE_DISTANCE_MODEL] = EnumProperty(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_DISTANCE_MODEL, enum = DistanceModels)
            self._property_instances[_libaudioverse.Lav_SOURCE_HEAD_RELATIVE] = BooleanProperty(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_HEAD_RELATIVE)
            self._property_instances[_libaudioverse.Lav_SOURCE_MAX_DISTANCE] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_MAX_DISTANCE)
            self._property_instances[_libaudioverse.Lav_SOURCE_MAX_REVERB_LEVEL] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_MAX_REVERB_LEVEL)
            self._property_instances[_libaudioverse.Lav_SOURCE_MIN_REVERB_LEVEL] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_MIN_REVERB_LEVEL)
            self._property_instances[_libaudioverse.Lav_SOURCE_OCCLUSION] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_OCCLUSION)
            self._property_instances[_libaudioverse.Lav_SOURCE_ORIENTATION] = Float6Property(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_ORIENTATION)
            self._property_instances[_libaudioverse.Lav_SOURCE_PANNING_STRATEGY] = EnumProperty(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_PANNING_STRATEGY, enum = PanningStrategies)
            self._property_instances[_libaudioverse.Lav_SOURCE_POSITION] = Float3Property(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_POSITION)
            self._property_instances[_libaudioverse.Lav_SOURCE_REVERB_DISTANCE] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_REVERB_DISTANCE)
            self._property_instances[_libaudioverse.Lav_SOURCE_SIZE] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_SOURCE_SIZE)


    @property
    def control_distance_model(self):   
        """Type: boolean


Default value: False
In order to make working with sources easier for simple applications, some properties of source objects are ignored in favor of values on the environment.
This property is used to disable this behavior for properties related to the distance model."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_CONTROL_DISTANCE_MODEL]

    @control_distance_model.setter
    def control_distance_model(self, value):
        self.control_distance_model.value=value



    @property
    def control_panning(self):   
        """Type: boolean


Default value: False
In order to make working with sources easier for simple applications, some properties of source objects are ignored in favor of values on the environment.
This property is used to disable this behavior for properties related to panning."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_CONTROL_PANNING]

    @control_panning.setter
    def control_panning(self, value):
        self.control_panning.value=value



    @property
    def control_reverb(self):   
        """Type: boolean


Default value: False
In order to make working with sources easier for simple applications, some properties of source objects are ignored in favor of values on the environment.
This property is used to disable this behavior for properties related to reverb."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_CONTROL_REVERB]

    @control_reverb.setter
    def control_reverb(self, value):
        self.control_reverb.value=value



    @property
    def distance_model(self):   
        """Type: int

Range: :any:`DistanceModels`

Default value: :any:`DistanceModels.linear`

The distance model determines how quickly sources get quieter as they move away from the listener.
The default value of this property is set from the corresponding property on the environment at source creation.
By default, sources ignore this property in favor of the value provided by their environment.  Set Lav_SOURCE_CONTROL_DISTANCE_MODEL to true to control it yourself."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_DISTANCE_MODEL]

    @distance_model.setter
    def distance_model(self, value):
        self.distance_model.value=value



    @property
    def head_relative(self):   
        """Type: boolean


Default value: False
Whether or not to consider this source's position to always be relative to the listener.

Sources which are head relative interpret their positions in the default coordinate system, relative to the listener.
Positive x is right, positive y is up, and positive z is behind the listener.
The orientation and position properties of an environment do not affect head relative sources, making them ideal for such things as footsteps and/or HUD effects that should be panned."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_HEAD_RELATIVE]

    @head_relative.setter
    def head_relative(self, value):
        self.head_relative.value=value



    @property
    def max_distance(self):   
        """Type: float

Range: [0.0, INFINITY]

Default value: 150.0

The maximum distance from the listener at which the source will be audible.
The default value of this property is set from the corresponding property on the environment at source creation.
By default, sources do not respect this property and use the corresponding value from their environment. Set Lav_SOURCE_CONTROL_DISTANCE_MODEL to true to control it yourself."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_MAX_DISTANCE]

    @max_distance.setter
    def max_distance(self, value):
        self.max_distance.value=value



    @property
    def max_reverb_level(self):   
        """Type: float

Range: [0.0, 1.0]

Default value: 0.6

The maximum amount of audio to be diverted to reverb sends, if any.

Behavior is undefined if this property is ever less than Lav_SOURCE_MIN_REVERB_LEVEL.

The default value of this property is set from the corresponding property on the environment at source creation.
By default, this property is ignored in favor of the value provided by this source's environment.  Set Lav_SOURCE_CONTROL_REVERB to true to control it yourself."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_MAX_REVERB_LEVEL]

    @max_reverb_level.setter
    def max_reverb_level(self, value):
        self.max_reverb_level.value=value



    @property
    def min_reverb_level(self):   
        """Type: float

Range: [0.0, 1.0]

Default value: 0.15

The minimum reverb level allowed.

if a send is configured to be a reverb send, this is the minimum amount of audio that will be diverted to it.

Behavior is undefined if this property is ever greater than the value you give to Lav_SOURCE_MAX_REVERB_LEVEL.

The default value of this property is set from the corresponding property on the environment at source creation.
By default, this property is ignored in favor of the value provided by this source's environment.  Set Lav_SOURCE_CONTROL_REVERB to true to control it yourself."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_MIN_REVERB_LEVEL]

    @min_reverb_level.setter
    def min_reverb_level(self, value):
        self.min_reverb_level.value=value



    @property
    def occlusion(self):   
        """Type: float

Range: [0.0, 1.0]

Default value: 0.0

A scalar representing how occluded this source is.

This property controls internal filters of the source that make occluded objects sound muffled.
A value of 1.0 is a fully occluded source, which will be all but silent; a value of 0.0 has no effect.

It is extremely difficult to map occlusion to a physical quantity.
As a consequence, this property is unitless."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_OCCLUSION]

    @occlusion.setter
    def occlusion(self, value):
        self.occlusion.value=value



    @property
    def orientation(self):   
        """Type: float6


Default value: [0.0, 0.0, -1.0, 0.0, 1.0, 0.0]

The orientation of the source.
This is not currently used.
In future, it will be used for sound cones and filters on sources facing away.
The interpretation is the same as that for the listener: the first 3 values are the direction of the front and the second 3 the direction of the top.
Note that these must both be unit vectors and that they must be orthoganal.
They are packed because, also like the listener, they must never be modified separately."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_ORIENTATION]

    @orientation.setter
    def orientation(self, value):
        self.orientation.value=value



    @property
    def panning_strategy(self):   
        """Type: int

Range: :any:`PanningStrategies`

Default value: :any:`PanningStrategies.stereo`

The strategy for the internal multipanner.
The default value of this property is set from the corresponding property on the environment at source creation.
By default, this property is ignored and sources use the value provided by their environment.  Set Lav_SOURCE_CONTROL_PANNING to true to control it yourself."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_PANNING_STRATEGY]

    @panning_strategy.setter
    def panning_strategy(self, value):
        self.panning_strategy.value=value



    @property
    def position(self):   
        """Type: float3


Default value: [0.0, 0.0, 0.0]

The position of the source in world coordinates."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_POSITION]

    @position.setter
    def position(self, value):
        self.position.value=value



    @property
    def reverb_distance(self):   
        """Type: float

Range: [0.0, INFINITY]

Default value: 75.0

The distance at which the source will only be heard through the reverb effect sends.

If this source is not feeding any effect sends configured as reverbs, this property has no effect.

For values greater than Lav_SOURCE_MAX_DISTANCE, the source will always be heard at least somewhat in the dry path.
Lav_SOURCE_DISTANCE_MODEL controls how this crossfading takes place.

The default value of this property is set from the corresponding property on the environment at source creation.
By default, sources ignore this property in favor of the value provided by their environment.  Set Lav_SOURCE_CONTROL_REVERB to true to control it yourself."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_REVERB_DISTANCE]

    @reverb_distance.setter
    def reverb_distance(self, value):
        self.reverb_distance.value=value



    @property
    def size(self):   
        """Type: float

Range: [0.0, INFINITY]

Default value: 0.0

The size of the source.
Sources are approximated as spheres.
The size is used to determine the closest point on the source to the listener, and is the radius of this sphere.
Size currently has no other effect.

The default value of this property is set from the corresponding property on the environment at source creation."""
        return self._property_instances[_libaudioverse.Lav_SOURCE_SIZE]

    @size.setter
    def size(self, value):
        self.size.value=value



    def feed_effect(node, effect):
        r"""Begin feeding the specified effect send."""
        return _lav.source_node_feed_effect(node, effect)

    def set_properties_from_environment(node):
        r"""A convenience function for working with properties on sources.
When called, this function sets the values of all properties which have corresponding properties on the environment to the values from the environment."""
        return _lav.source_node_set_properties_from_environment(node)

    def stop_feeding_effect(node, effect):
        r"""Stop feeding an effect send."""
        return _lav.source_node_stop_feeding_effect(node, effect)



_types_to_classes[ObjectTypes.source_node] = SourceNode
class ThreeBandEqNode(GenericNode):
    r"""A three band equalizer.

This node consists of a peaking filter and a highshelf filter in series, such that the frequency spectrum may be equalized in three, configurable bands.

The lowest of these bands begins at ``lowband_frequency`` and continues down to ``0 hz``.
The highest is from ``highband_frequency`` and continues until nyquist.
The middle is the remaining space between the low and high band.
If the high band begins below the low band, behavior is undefined, but will almost certainly not do what you want.
Libaudioverse does not check for this case.

The slopes that this node institutes are not perfect and cannot increase effectively beyond a certain point.
This is the least expensive of the Libaudioverse equalizers, and is sufficient for many simpler applications.

Inputs:

=====  ================================================  =======================
index  channels                                          description            
=====  ================================================  =======================
0      Depends on arguments to this node's constructor.  The signal to equalize.
=====  ================================================  =======================

Outputs:

=====  ================================================  =====================
index  channels                                          description          
=====  ================================================  =====================
0      Depends on arguments to this node's constructor.  The equalized signal.
=====  ================================================  =====================
"""

    def __init__(self, server, channels):
        super(ThreeBandEqNode, self).__init__(_lav.create_three_band_eq_node(server, channels))

    def init_with_handle(self, handle):
        with _object_states_lock:
            #our super implementation adds us, so remember if we weren't there.
            should_add_properties = handle.handle not in _object_states
            super(ThreeBandEqNode, self).init_with_handle(handle)
            if should_add_properties:
                self._state['properties']["highband_dbgain"] = _libaudioverse.Lav_THREE_BAND_EQ_HIGHBAND_DBGAIN
                self._state['properties']["highband_frequency"] = _libaudioverse.Lav_THREE_BAND_EQ_HIGHBAND_FREQUENCY
                self._state['properties']["lowband_dbgain"] = _libaudioverse.Lav_THREE_BAND_EQ_LOWBAND_DBGAIN
                self._state['properties']["lowband_frequency"] = _libaudioverse.Lav_THREE_BAND_EQ_LOWBAND_FREQUENCY
                self._state['properties']["midband_dbgain"] = _libaudioverse.Lav_THREE_BAND_EQ_MIDBAND_DBGAIN
            self._property_instances[_libaudioverse.Lav_THREE_BAND_EQ_HIGHBAND_DBGAIN] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_THREE_BAND_EQ_HIGHBAND_DBGAIN)
            self._property_instances[_libaudioverse.Lav_THREE_BAND_EQ_HIGHBAND_FREQUENCY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_THREE_BAND_EQ_HIGHBAND_FREQUENCY)
            self._property_instances[_libaudioverse.Lav_THREE_BAND_EQ_LOWBAND_DBGAIN] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_THREE_BAND_EQ_LOWBAND_DBGAIN)
            self._property_instances[_libaudioverse.Lav_THREE_BAND_EQ_LOWBAND_FREQUENCY] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_THREE_BAND_EQ_LOWBAND_FREQUENCY)
            self._property_instances[_libaudioverse.Lav_THREE_BAND_EQ_MIDBAND_DBGAIN] = FloatProperty(handle = self.handle, slot = _libaudioverse.Lav_THREE_BAND_EQ_MIDBAND_DBGAIN)


    @property
    def highband_dbgain(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

The gain to apply to the highest frequency band as decibals."""
        return self._property_instances[_libaudioverse.Lav_THREE_BAND_EQ_HIGHBAND_DBGAIN]

    @highband_dbgain.setter
    def highband_dbgain(self, value):
        self.highband_dbgain.value=value



    @property
    def highband_frequency(self):   
        """Type: float

Range: dynamic

Default value: 1000.0

The frequency that divides the middle band from the high band."""
        return self._property_instances[_libaudioverse.Lav_THREE_BAND_EQ_HIGHBAND_FREQUENCY]

    @highband_frequency.setter
    def highband_frequency(self, value):
        self.highband_frequency.value=value



    @property
    def lowband_dbgain(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

The gain of the lowest frequency band as decibals."""
        return self._property_instances[_libaudioverse.Lav_THREE_BAND_EQ_LOWBAND_DBGAIN]

    @lowband_dbgain.setter
    def lowband_dbgain(self, value):
        self.lowband_dbgain.value=value



    @property
    def lowband_frequency(self):   
        """Type: float

Range: dynamic

Default value: 300.0

The frequency that divides the low and middle bands.

This ranges from 0 to nyquist."""
        return self._property_instances[_libaudioverse.Lav_THREE_BAND_EQ_LOWBAND_FREQUENCY]

    @lowband_frequency.setter
    def lowband_frequency(self, value):
        self.lowband_frequency.value=value



    @property
    def midband_dbgain(self):   
        """Type: float

Range: [-INFINITY, INFINITY]

Default value: 0.0

The gain to apply to the middle band of the equalizer."""
        return self._property_instances[_libaudioverse.Lav_THREE_BAND_EQ_MIDBAND_DBGAIN]

    @midband_dbgain.setter
    def midband_dbgain(self, value):
        self.midband_dbgain.value=value





_types_to_classes[ObjectTypes.three_band_eq_node] = ThreeBandEqNode
