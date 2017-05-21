import collections, math

class TkWorld(object):

	def __init__(self, window):
		self.window = window
		self.current = None
		self.scenes = {}
		self.options = []
		self.minmax = []

	def get_options(self):
		options = []
		for key in self.options:
			current = self.options.index(key)			
			options.append([key, getattr(self, key), *self.minmax[current]])
		return options

	def set_options(self, new):
		for key, value, min, max in new:
			if key not in self.options:
				self.options.append(key)
				self.minmax.append([min, max])
			current = self.options.index(key)
			if self.minmax[current][0] <= value <= self.minmax[current][1]:
				setattr(self, key, value)

	def transition(self, scene):
		if self.current:
			self.current.unload(self.window)
		self.current = self.scenes[scene]
		self.current.load(self.window)

	def add_scenes(self, new_scenes):
		self.scenes.update(new_scenes)
