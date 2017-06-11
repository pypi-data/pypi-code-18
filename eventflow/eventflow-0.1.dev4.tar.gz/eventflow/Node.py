import pydbus
import gi.repository
import threading
import sys
from .PersistentFile import PersistentFile

class Node:
	class Node0: # node version 0
		"""
			<node>
				<interface name="io.eventflow.Node0">
					<method name="ConnectionAdd">
						<arg type="s" name="output" direction="in" />
						<arg type="s" name="target_uuid" direction="in" />
						<arg type="s" name="target_input" direction="in" />
					</method>
					<method name="ConnectionDelete">
						<arg type="s" name="output" direction="in" />
						<arg type="s" name="target_uuid" direction="in" />
						<arg type="s" name="target_input" direction="in" />
					</method>
					<method name="Push">
						<arg type="s" name="input" direction="in" />
						<arg type="ay" name="data" direction="in" />
					</method>
				</interface>
			</node>
		"""
		def __init__(self, parent):
			self.parent = parent
		
		def ConnectionAdd(self, *args):
			self.parent.push_add(*args)
		
		def ConnectionDelete(self, *args):
			self.parent.push_del(*args)
		
		def Push(self, *args):
			self.parent._receive(*args)
	
	class ConnectionEndpoint:
		def __init__(self, bus, uuid, input, get_bus=True):
			self.bus = bus
			self.uuid = uuid
			self.input = input
			if get_bus:
				self.get_bus()
		
		def get_bus(self):
			if not hasattr(self, "object"):
				try:
					self.object = self.bus.get("io.eventflow.Node0_" + self.uuid)
				except gi.repository.GLib.Error:
					print("get_bus(" + self.uuid + ", " + self.input + ") failed", file=sys.stderr)
		
		def send(self, data):
			self.get_bus()
			try:
				self.object.Push(self[1], data)
			except AttributeError:
				pass
			except gi.repository.GLib.Error:
				import traceback
				traceback.print_exc()
		
		# methods needed for set-insertion
		def __hash__(self): return hash((self.uuid, self.input))
		def __eq__(self, other): return isinstance(other, Node.ConnectionEndpoint) and self.uuid == other.uuid and self.input == other.input
	
	def __init__(self, uuid, persistent=PersistentFile):
		self._uuid = uuid
		self._bus_name = "io.eventflow.Node0_" + self.uuid
		self._persistent = persistent(self.uuid)
		self._callbacks = {}
		self._output_connections, self._forward_connections = self._persistent.restore()
		self._bus = pydbus.SystemBus()
		self._bus.publish(self.bus_name, Node.Node0(self))
		self.send_thread = threading.Thread(target=self._send_thread, daemon=True)
		self.send_event = threading.Event()
		self.running = False
		self.send_queue = []
	
	def _send_thread(self):
		while self.running:
			self.send_event.wait()
			self.send_event.clear()
			send_copy = list(self.send_queue) # make copy
			for output, data in send_copy:
				try:
					for connection_endpoint in self._output_connections[output]:
						connection_endpoint.send(data)
				except KeyError:
					pass
				try:
					self.send_queue.remove((output, data))
				except ValueError:
					print("internal send queue error, this is a bug, please report this!", file=sys.stderr)
	
	def run(self):
		self.loop = gi.repository.GLib.MainLoop()
		self.running = True
		self.send_thread.start()
		try:
			self.loop.run()
		except KeyboardInterrupt:
			pass
		finally:
			self.running = False
			self.send_event.set()
			self.send_thread.join()
	
	def stop(self):
		if self.loop.is_running():
			self.loop.quit()
	
	def _alias_to_uuid(self, alias):
		"""Converts an alias to a uuid by concatening the alias to the uuid."""
		return self.uuid + "_" + alias
	
	def _connection_add(self, source_uuid, source_output, target_uuid, target_input):
		"""Pushes a connection addition to the node."""
		try:
			self._bus.get("io.eventflow.Node0_" + source_uuid).ConnectionAdd(source_output, target_uuid, target_input)
		except gi.repository.GLib.Error:
			print("_connection_add(" + ", ".join([ source_uuid, source_output, target_uuid, target_input ]) + ") failed", file=sys.stderr)
			return False
		return True
	
	def _connection_del(self, source_uuid, source_output, target_uuid, target_input):
		"""Pushes a connection removal to the node."""
		try:
			self._bus.get("io.eventflow.Node0_" + source_uuid).ConnectionDelete(source_output, target_uuid, target_input)
		except gi.repository.GLib.Error:
			print("_connection_del(" + ", ".join([ source_uuid, source_output, target_uuid, target_input ]) + ") failed", file=sys.stderr)
			return False
		return True
	
	def _persistent_save(self):
		"""Store output- and forward-connections into persistent-object."""
		self._persistent.save(self._output_connections, self._forward_connections)
	
	def _receive(self, input, data):
		"""Receives pushed data from other nodes. This function calls callbacks
		and forwards data to connected nodes."""
		try:
			self._callbacks[input](self, input, bytes(data))
		except KeyError:
			pass
		try:
			for connection_endpoint in self._forward_connections[input]:
				connection_endpoint.send(data)
		except KeyError:
			pass
	
	@property
	def uuid(self):
		return self._uuid
	
	@property
	def bus_name(self):
		return self._bus_name
	
	def register(self, input, callback):
		"""Registers a callback for a given input. Calling this multiple times
		with the same input will overwrite the callback."""
		self._callbacks[input] = callback
	
	def unregister(self, input):
		"""Unregisters a callback for a given input."""
		try:
			del self._callbacks[input]
		except KeyError:
			pass
	
	def push_add(self, output, target_alias, target_input):
		"""Connection: self (output) -> target"""
		target_uuid = self._alias_to_uuid(target_alias)
		try:
			self._output_connections[output].add(Node.ConnectionEndpoint(self._bus, target_uuid, target_input))
		except (KeyError, AttributeError):
			self._output_connections[output] = { Node.ConnectionEndpoint(self._bus, target_uuid, target_input) }
		self._persistent_save()
	
	def push_del(self, output, target_alias, target_input):
		"""Connection: self (output) -> target"""
		target_uuid = self._alias_to_uuid(target_alias)
		try:
			self._output_connections[output].discard(
				Node.ConnectionEndpoint(self._bus, target_uuid, target_input, get_bus=False))
			if len(self._output_connections[output]) == 0:
				del self._output_connections[output]
			self._persistent_save()
		except (KeyError, AttributeError):
			pass
	
	def subscribe_add(self, source_alias, source_output, input):
		"""Connection: source -> self"""
		source_uuid = self._alias_to_uuid(source_alias)
		self._connection_add(source_uuid, source_output, self.uuid, input)
	
	def subscribe_del(self, source_alias, source_output, input):
		"""Connection: source -> self"""
		source_uuid = self._alias_to_uuid(source_alias)
		self._connection_del(source_uuid, source_output, self.uuid, input)
	
	def connect(self, source_alias, source_output, target_alias, target_input):
		"""Connection: source -> target
		Connect two child nodes with each other (one direction per call)."""
		source_uuid = self._alias_to_uuid(source_alias)
		target_uuid = self._alias_to_uuid(target_alias)
		self._connection_add(source_uuid, source_output, target_uuid, target_input)
	
	def disconnect(self, source_alias, source_output, target_alias, target_input):
		"""Connection: source -> target
		Disconnect two child nodes from each other (one direction per call)."""
		source_uuid = self._alias_to_uuid(source_alias)
		target_uuid = self._alias_to_uuid(target_alias)
		self._connection_del(source_uuid, source_output, target_uuid, target_input)
	
	def forward_add(self, input, target_alias, target_input):
		"""Connection: self (input) -> target"""
		target_uuid = self._alias_to_uuid(target_alias)
		try:
			self._forward_connections[input].add(Node.ConnectionEndpoint(self._bus, target_uuid, target_input))
		except (KeyError, AttributeError):
			self._forward_connections[input] = { Node.ConnectionEndpoint(self._bus, target_uuid, target_input) }
		self._persistent_save()
	
	def forward_del(self, input, target_alias, target_input):
		"""Connection: self (input) -> target"""
		target_uuid = self._alias_to_uuid(target_alias)
		try:
			self._forward_connections[input].discard(
				Node.ConnectionEndpoint(self._bus, target_uuid, target_input, get_bus=False))
			if len(self._forward_connections[input]) == 0:
				del self._forward_connections[input]
			self._persistent_save()
		except (KeyError, AttributeError):
			pass
	
	def push(self, output, data):
		"""Push data through output (will be sent to nodes connected to this output)."""
		self.send_queue.append((output, data))
		self.send_event.set()
