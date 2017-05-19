import ctypes
import ctypes.util
import os
import threading

libef = None
try:
	libef = ctypes.util.find_library("eventflow")
	libef = os.path.join("/usr/lib", libef)
	libef = ctypes.cdll.LoadLibrary(libef)
except:
	print("ef: Failed to initialize module: Library cannot be loaded.")
	raise

libef_config_request_callback = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_char_p, ctypes.c_void_p)
libef_data_callback = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t)

libef.ef_new_provider.argtypes = [ ctypes.c_char_p, ctypes.c_char_p, libef_data_callback, libef_config_request_callback ]
libef.ef_new_provider.restype = ctypes.c_void_p
libef.ef_new.argtypes = [ ctypes.c_char_p, ctypes.c_char_p, libef_data_callback ]
libef.ef_new.restype = ctypes.c_void_p
libef.ef_delete.argtypes = [ ctypes.c_void_p ]
libef.ef_delete.restype = None
libef.ef_send.argtypes = [ ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t ]
libef.ef_send.restype = ctypes.c_bool
libef.ef_config_push.argtypes = [ ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p ]
libef.ef_config_push.restype = ctypes.c_bool

libef.ef_config_new.argtypes = None
libef.ef_config_new.restype = ctypes.c_void_p
libef.ef_config_delete.argtypes = [ ctypes.c_void_p ]
libef.ef_config_delete.restype = None
libef.ef_config_set_address.argtypes = [ ctypes.c_void_p, ctypes.c_char_p ]
libef.ef_config_set_address.restype = None
libef.ef_config_get_address.argtypes = [ ctypes.c_void_p ]
libef.ef_config_get_address.restype = ctypes.c_char_p
libef.ef_config_set_config_provider_uuid.argtypes = [ ctypes.c_void_p, ctypes.c_char_p ]
libef.ef_config_set_config_provider_uuid.restype = None
libef.ef_config_get_config_provider_uuid.argtypes = [ ctypes.c_void_p ]
libef.ef_config_get_config_provider_uuid.restype = ctypes.c_char_p
libef.ef_config_get_connections_size.argtypes = [ ctypes.c_void_p ]
libef.ef_config_get_connections_size.restype = ctypes.c_uint
libef.ef_config_clear_connections.argtypes = [ ctypes.c_void_p ]
libef.ef_config_clear_connections.restype = None
libef.ef_config_add_connections.argtypes = [ ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p ]
libef.ef_config_add_connections.restype = None
libef.ef_config_get_connections_uuid.argtypes = [ ctypes.c_void_p, ctypes.c_uint ]
libef.ef_config_get_connections_uuid.restype = ctypes.c_char_p
libef.ef_config_get_connections_address.argtypes = [ ctypes.c_void_p, ctypes.c_uint ]
libef.ef_config_get_connections_address.restype = ctypes.c_char_p
libef.ef_config_get_connections_name_other.argtypes = [ ctypes.c_void_p, ctypes.c_uint ]
libef.ef_config_get_connections_name_other.restype = ctypes.c_char_p
libef.ef_config_get_connections_name_self.argtypes = [ ctypes.c_void_p, ctypes.c_uint ]
libef.ef_config_get_connections_name_self.restype = ctypes.c_char_p

class EventFlow:
	class Config:
		def __init__(self, ptr=None):
			if ptr != None:
				self._ptr = ptr
				self.address = libef.ef_config_get_address(self._ptr).decode("ascii")
				self.config_provider_uuid = libef.ef_config_get_config_provider_uuid(self._ptr).decode("ascii")
				self.connections = [ {
						"uuid": libef.ef_config_get_connections_uuid(self._ptr, i).decode("ascii"),
						"address": libef.ef_config_get_connections_address(self._ptr, i).decode("ascii"),
						"name_other": libef.ef_config_get_connections_name_other(self._ptr, i).decode("ascii"),
						"name_self": libef.ef_config_get_connections_name_self(self._ptr, i).decode("ascii")
					} for i in range(libef.ef_config_get_connections_size(self._ptr)) ]
			else:
				self._ptr = libef.ef_config_new()
				self.address = ""
				self.config_provider_uuid = ""
				self.connections = []
		
		def delete(self):
			libef.ef_config_delete(self._ptr)
		
		def _store_values_in_pointer(self):
			libef.ef_config_set_address(self._ptr, self.address.encode("ascii"))
			libef.ef_config_set_config_provider_uuid(self._ptr, self.config_provider_uuid.encode("ascii"))
			libef.ef_config_clear_connections(self._ptr)
			for connection in self.connections:
				try:
					libef.ef_config_add_connections(self._ptr,
						connection["uuid"].encode("ascii"),
						connection["address"].encode("ascii"),
						connection["name_other"].encode("ascii"),
						connection["name_self"].encode("ascii"))
				except (KeyError, AttributeError):
					continue
	
	def __init__(self, uuid, config_provider_address, config_request_callback=None):
		self.callbacks = {}
		self.ctypes_data_callback = self._get_data_callback() # prevent garbage collection
		if callable(config_request_callback):
			self.user_config_request_callback = config_request_callback
			self.ctypes_config_request_callback = self._get_config_request_callback() # prevent garbage collection
			self._ptr = libef.ef_new_provider(uuid.encode("ascii"), config_provider_address.encode("ascii"), self.ctypes_data_callback, self.ctypes_config_request_callback)
		else:
			self._ptr = libef.ef_new(uuid.encode("ascii"), config_provider_address.encode("ascii"), self.ctypes_data_callback)
	
	def delete(self):
		libef.ef_delete(self._ptr)
	
	def _get_data_callback(self): # makes self available
		def f(uuid, name, data, size):
			return self.data_callback(uuid, name, data, size)
		return libef_data_callback(f)
	
	def _get_config_request_callback(self): # makes self available
		def f(uuid, config):
			return self.config_request_callback(uuid, config)
		return libef_config_request_callback(f)
	
	def data_callback(self, uuid, name, data, size):
		# data = (ctypes.c_char * size).from_address(ctypes.addressof(data))
		# data2 = (ctypes.c_char * size).from_address(data.value)
		# ctypes.memmove(data2, data, size)
		# data = bytes([ data[i] for i in range(size) ]) # TODO: find better solution because data will be copied
		# print("Got data:", data[0], data[1], data[2], data[3], data, bytes(data), str(data))
		try:
			for callback in self.callbacks[name.decode("ascii")]:
				callback(uuid.decode("ascii"), name.decode("ascii"), bytes([ data[i] for i in range(size) ]))
		except KeyError:
			print("Ignoring data because no callback has been registered for:", name.decode("ascii"))
	
	def config_request_callback(self, uuid, config):
		print(">>> config_request_callback(" + str(self) + ", " + str(uuid) + ", " + str(config) + ")")
		try:
			config = EventFlow.Config(config)
			print("Self:", self, "property:")
			return_value = self.user_config_request_callback(uuid.decode("ascii"), config)
			config._store_values_in_pointer()
			return return_value if return_value != None else False
		except:
			import traceback
			traceback.print_exc()
			return False
	
	def send(self, message_uuid, name, data):
		return libef.ef_send(self._ptr, message_uuid.encode("ascii"), name.encode("ascii"), data.encode("ascii"), len(data))
	
	def config_push(self, uuid, config):
		if isinstance(config, EventFlow.Config):
			return libef.ef_config_push(self._ptr, uuid.encode("ascii"), config._ptr)
		print("ef: failed to push config: config has invalid type")
		return False
	
	def register(self, name, callback):
		try:
			self.callbacks[name].append(callback)
		except (KeyError, AttributeError):
			self.callbacks[name] = [ callback ]
	
	def unregister(self, name, callback=None):
		try:
			if callback == None:
				del self.callbacks[name]
			else:
				self.callbacks[name].remove(callback)
		except (KeyError, AttributeError, ValueError):
			pass

def config_request_callback(uuid, config):
	print("ConfigRequest: Called from userland!")
	if uuid == "00000000-6367-4efa-9383-bdf1747a8105":
		print("CONFIG: provider is asking for config!")
		config.address = "127.0.0.1:50051"
		config.connections = [{
			"uuid": "00000001-6367-4efa-9383-bdf1747a8105",
			"address": "127.0.0.1:1111",
			"name_other": "in",
			"name_self": "out"
		}]
	elif uuid == "00000001-6367-4efa-9383-bdf1747a8105":
		print("CONFIG: retriever is asking for config!")
		config.address = "127.0.0.1:1111"
		config.connections = [{
			"uuid": "00000000-6367-4efa-9383-bdf1747a8105",
			"address": "127.0.0.1:50051",
			"name_other": "in",
			"name_self": "out"
		}]
	config.config_provider_uuid = "00000000-6367-4efa-9383-bdf1747a8105"
	return True

def data_callback(uuid, name, data):
	print("DataPush: Called from userland!")
	print("Got data:", uuid, name, data)

# ef = EventFlow("00000000-6367-4efa-9383-bdf1747a8105", "127.0.0.1:50051", config_request_callback)
# ef.register("in", data_callback)
# input("Press enter to quit: ")
# ef.delete()
