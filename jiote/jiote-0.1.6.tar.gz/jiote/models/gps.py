

class Position(object):
	__slots__ = ['lat', 'lng', 'alt']

	def __init__(self, lat, lng, alt=None):
		self.lat = lat
		self.lng = lng
		self.alt = None

