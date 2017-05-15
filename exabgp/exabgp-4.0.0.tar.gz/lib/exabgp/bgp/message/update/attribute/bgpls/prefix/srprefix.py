# encoding: utf-8
"""
srprefix.py

Created by Evelio Vila
Copyright (c) 2014-2017 Exa Networks. All rights reserved.
"""

from struct import unpack

from exabgp.vendoring.bitstring import BitArray
from exabgp.bgp.message.update.attribute.bgpls.linkstate import LINKSTATE, LsGenericFlags

#    draft-gredler-idr-bgp-ls-segment-routing-ext-03
#    0                   1                   2                   3
#    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |               Type            |            Length             |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |     Flags       |  Algorithm  |           Reserved            |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |                       SID/Index/Label (variable)              |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

@LINKSTATE.register()
class SrPrefix(object):
	TLV = 1158

	def __init__ (self, flags, sids, sr_algo):
		self.flags = flags
		self.sids = sids
		self.sr_algo = sr_algo

	def __repr__ (self):
		return "prefix_flags: %s, sids: %s" % (self.flags, self.sids)

	@classmethod
	def unpack (cls,data,length):
		# We only support IS-IS flags for now.
		flags = LsGenericFlags.unpack(data[0],LsGenericFlags.ISIS_SR_FLAGS)
		#
		# Parse Algorithm
		sr_algo = unpack('!B',data[1])[0]
		# Move pointer 4 bytes: Flags(1) + Algorithm(1) + Reserved(2)
		data = data[4:]
     	# SID/Index/Label: according to the V and L flags, it contains
      	# either:
		# *  A 3 octet local label where the 20 rightmost bits are used for
		#	 encoding the label value.  In this case the V and L flags MUST
		#	 be set.
		#
		# *  A 4 octet index defining the offset in the SID/Label space
		# 	 advertised by this router using the encodings defined in
		#  	 Section 3.1.  In this case V and L flags MUST be unset.
		sids = []
		while data:
			if flags.flags['V'] and flags.flags['L']:
				b = BitArray(bytes=data[:3])
				sid = b.unpack('uintbe:24')[0]
				data = data[3:]
			elif (not flags.flags['V']) and (not flags.flags['L']):
				sid = unpack('!I',data[:4])[0]
				data = data[4:]
			sids.append(sid)

		return cls(flags=flags.flags, sids=sids, sr_algo=sr_algo)

	def json (self,compact=None):
		return '"sr-adj-flags": "%s", "sids": "%s", "sr-algorithm": "%s"' % (self.flags,
				self.sids, self.sr_algo)

