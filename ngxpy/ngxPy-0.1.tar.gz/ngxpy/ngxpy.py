import requests, json, ConfigParser, os

## TODOs
## 	1. Add several common ways to add authentication
##		* Basic Auth
##		* Custom Headers (X-Auth-Key/X-Auth-User)

# Defaults for .ngxpy.ini if parameters missing
safecfg = { 'schema': 'http',
			'host': '127.0.0.1',
			'port': '8080',
			'status': 'status',
			'upstreamConf': 'upstream_conf'
			}
cfg = ConfigParser.SafeConfigParser(safecfg)

class ngxpy:
	def __init__(self, schema='http', 
				host='127.0.0.1', port='8080', 
				status='status', upstreamConf='upstream_conf', 
				cfgSec=None):

		# If .ngxpy.ini exist, use those values, otherwise use function parameters
		if cfgSec:
			home = os.path.expanduser("~")
			file = '{}/.ngxpy.ini'.format(home)
			if cfg.read(file):
				self.host = self.cfgCheck(cfgSec, 'host')
				self.port = self.cfgCheck(cfgSec, 'port')
				self.status = self.cfgCheck(cfgSec, 'status')
				self.upstreamConf = self.cfgCheck(cfgSec, 'upstreamConf')
				self.schema = self.cfgCheck(cfgSec, 'schema')
			else:
				print '{} file is missing'.format(file)
				exit()
		else:
			self.host = host
			self.port = port
			self.status = status
			self.upstreamConf = upstreamConf
			self.schema = schema
		self.socket = '{}:{}'.format(self.host, self.port)
		self.api = '{}://{}/'.format(self.schema, self.socket)

	def cfgCheck(self, sec, param):
		try:
			return cfg.get(sec, param)
		except:
			pass

	class APIError(Exception):
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return self.value

	def parse_json(self, request):
		try:
			return request.json()
		except ValueError:
			return request.text

	def get(self, url, params=None):
		r = requests.get(self.api + url, params=params)
		return self.parse_json(r)

	def get_status(self):
		s = self.get(self.status)
		return s

	def get_stream_status(self):
		s = self.get_status()['stream']
		return s

	def get_upstream_conf(self, **kwargs):
		'''
		Available Keys: 
		stream=  (Select TCP/UDP server group)
		upstream=name (Mandatory)
		id=number
		remove= (Removes server from group)
		add= (Adds server to group)
		backup= (Add server as backup in group)
		down= (Marks server as down in group)
		drain= (Drains server from group)
		up= (Marks server as up in group)
		server=address
		service=name
		weight=number
		max_conns=number
		max_fails=number
		fail_timeout=time
		slow_start=time
		route=string (useful for sticky route Loadbalancer)
		'''
		u = self.get(self.upstreamConf, params=kwargs)
		return u

	# isHttp=False are tcp/udp zones and upstreams
	def get_server_zones(self, isHttp=True, zone=None):
		s = self.get_status()['server_zones']
		return s

	def get_upstreams(self, isHttp=True, upstream=None):
		s = self.get_status()['upstreams']
		return s

	def get_caches(self):
		s = self.get_status()['caches']
		return s

	def get_peer_stats(self, upstream, peer_id=None, isHttp=True):
		peers = []
		if isHttp:
			s = self.get_status()['upstreams'][upstream]['peers']
		else:
			s = self.get_stream_status()['upstreams'][upstream]['peers']
		for p in s:
			if peer_id:
				if peer_id == p['id']:
					return p
			else:
				peers.append(p)
		return peers

	def list_server_zones(self, isHttp=True):
		server_zones = []
		if isHttp:
			s = self.get_status()['server_zones']
		else:
			s = self.get_stream_status()['server_zones']
		for z in s:
			server_zones.append(z)
		return server_zones

	def list_upstreams(self, isHttp=True):
		upstreams = []
		if isHttp:
			s = self.get_status()['upstreams']
		else:
			s = self.get_stream_status()['upstreams']
		for u in s:
			upstreams.append(u)
		return upstreams

	def list_caches(self):
		caches = []
		s = self.get_status()['caches']
		for c in s:
			caches.append(c) 
		return caches

	def num_of_peers(self, upstream, isHttp=True):
		if isHttp:
			s = self.get_status()['upstreams'][upstream]['peers']
		else:
			s = self.get_stream_status()['upstreams'][upstream]['peers']
		return len(s)