import sys
import json

class PersistentFile:
	def __init__(self, uuid, filename="./persistence.%s.json"):
		self.filename = filename % uuid
	
	def restore(self):
		try:
			with open(self.filename) as f:
				content = json.load(f)
				return (content["output_connections"], content["forward_connections"])
		except (IOError, OSError):
			print("PersistentFile.restore() failed", file=sys.stderr)
		except KeyError:
			print("PersistentFile.restore() failed (format)", file=sys.stderr)
		return ({}, {})
	
	def save(self, output_connections, forward_connections):
		try:
			with open(self.filename, "w") as f:
				json.dump({
					"output_connections": output_connections,
					"forward_connections": forward_connections
				}, f)
		except (IOError, OSError):
			print("PersistentFile.save() failed", file=sys.stderr)
